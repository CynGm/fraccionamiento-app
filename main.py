from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Residente, Visita
from schemas import VisitaSchema, ResidenteSchema
from utils import generar_qr_residente
from fastapi.responses import FileResponse
from schemas import ResidenteSchema, VisitaSchema, ResidenteCreate


app = FastAPI()

# --------------------------------------
# ENDPOINT: Inicio
# --------------------------------------
@app.get("/")
def inicio():
    return {"mensaje": "¡Servidor corriendo correctamente!"}


# --------------------------------------
# ENDPOINT: Registrar visita
# --------------------------------------
@app.post("/registrar-visita")
def registrar_visita(visita: VisitaSchema, db: Session = Depends(get_db)):
    residente = db.query(Residente).filter(Residente.id == visita.residente_id).first()
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")

    nueva_visita = Visita(**visita.dict())
    db.add(nueva_visita)
    db.commit()
    db.refresh(nueva_visita)

    return {"mensaje": "Visita registrada exitosamente"}


# --------------------------------------
# ENDPOINT: Generar QR para residente
# --------------------------------------
@app.get("/generar-qr/{residente_id}")
def qr_residente(residente_id: int, db: Session = Depends(get_db)):
    residente = db.query(Residente).filter(Residente.id == residente_id).first()
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")

    ruta_qr = generar_qr_residente(residente)
    return FileResponse(ruta_qr, media_type="image/png", filename="qr_residente.png")

# -----------------------------------------------
# ✅ ENDPOINT: Crear residente
# -----------------------------------------------
@app.post("/crear-residente")
def crear_residente(residente: ResidenteCreate, db: Session = Depends(get_db)):
    nuevo = Residente(**residente.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # 🔽 Generar el QR una vez que se tiene el ID del nuevo residente
    generar_qr_residente(nuevo.id)

    return {
        "mensaje": "Residente creado correctamente",
        "id": nuevo.id,
        "nombre": nuevo.nombre
    }

