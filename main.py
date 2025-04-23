from fastapi import FastAPI, Depends 
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db, crear_tablas
from models import Residente, Visita
from schemas import (
    ResidenteCreate,
    ResidenteSchema,
    VisitaEntrada,
    VisitaSalida,
    VisitaOut
)
from utils import generar_qr_residente, descargar_qr
from routes import residentes  # 👈 nuevo: rutas externas

# Inicializa la app
app = FastAPI()

# 🔧 Crear tablas automáticamente al iniciar
crear_tablas()

# 🔗 Agregar router de residentes
app.include_router(residentes.router)


# --------------------------------------------------------
# ✅ ENDPOINT: Inicio
# --------------------------------------------------------
@app.get("/")
def inicio():
    return {"mensaje": "¡Servidor corriendo correctamente!"}


# --------------------------------------------------------
# ✅ ENDPOINT: Crear residente simple (modo anterior)
# --------------------------------------------------------
@app.post("/crear-residente")
def crear_residente(residente: ResidenteCreate, db: Session = Depends(get_db)):
    nuevo = Residente(**residente.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    generar_qr_residente(nuevo.id)

    return {
        "mensaje": "Residente creado correctamente",
        "id": nuevo.id,
        "nombre": nuevo.nombre
    }


# --------------------------------------------------------
# ✅ ENDPOINT: Generar QR manualmente
# --------------------------------------------------------
@app.get("/generar-qr/{residente_id}")
def generar_qr(residente_id: int):
    generar_qr_residente(residente_id)
    return {"mensaje": f"QR del residente {residente_id} generado correctamente."}


# --------------------------------------------------------
# ✅ ENDPOINT: Descargar QR
# --------------------------------------------------------
@app.get("/descargar-qr/{residente_id}")
def descargar_qr_residente(residente_id: int):
    return descargar_qr(residente_id)


# --------------------------------------------------------
# ✅ ENDPOINT: Registrar visita
# --------------------------------------------------------
@app.post("/registrar-visita")
def registrar_visita(visita: VisitaEntrada, db: Session = Depends(get_db)):
    nueva_visita = Visita(**visita.dict())
    db.add(nueva_visita)
    db.commit()
    db.refresh(nueva_visita)

    return {
        "mensaje": "Visita registrada correctamente",
        "visitante": nueva_visita.nombre_visitante,
        "residente_id": nueva_visita.residente_id,
        "visita_id": nueva_visita.id
    }


# --------------------------------------------------------
# ✅ ENDPOINT: Salida de visita
# --------------------------------------------------------
@app.put("/salida-visita/{visita_id}")
def salida_visita(visita_id: int, datos_salida: VisitaSalida, db: Session = Depends(get_db)):
    visita = db.query(Visita).filter(Visita.id == visita_id).first()
    if not visita:
        return {"error": "Visita no encontrada"}

    visita.hora_salida = datos_salida.hora_salida
    db.commit()

    return {
        "mensaje": "Hora de salida registrada correctamente",
        "id": visita.id,
        "hora_salida": str(visita.hora_salida)
    }


# --------------------------------------------------------
# ✅ ENDPOINT: Ver historial de visitas
# --------------------------------------------------------
@app.get("/visitas", response_model=list[VisitaOut])
def obtener_visitas(db: Session = Depends(get_db)):
    visitas = db.query(Visita).all()
    return visitas
