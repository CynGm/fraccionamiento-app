from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse, HTMLResponse
import os
import base64

from database import get_db
from models import Residente, Visita
from schemas import VisitaSchema, ResidenteSchema, ResidenteCreate
from utils import generar_qr_residente

app = FastAPI()

# ---------------------------------------------
# ENDPOINT: Inicio
# ---------------------------------------------
@app.get("/")
def inicio():
    return {"mensaje": "¡Servidor corriendo correctamente!"}


# ---------------------------------------------
# ENDPOINT: Registrar visita
# ---------------------------------------------
@app.post("/registrar-visita")
def registrar_visita(visita: VisitaSchema, db: Session = Depends(get_db)):
    nueva_visita = Visita(**visita.dict())
    db.add(nueva_visita)
    db.commit()
    db.refresh(nueva_visita)
    return {
        "mensaje": "Visita registrada correctamente",
        "id": nueva_visita.id
    }


# ---------------------------------------------
# ENDPOINT: Crear residente
# ---------------------------------------------
@app.post("/crear-residente")
def crear_residente(residente: ResidenteCreate, db: Session = Depends(get_db)):
    nuevo = Residente(**residente.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # Generar el QR una vez que se tiene el ID del nuevo residente
    generar_qr_residente(nuevo.id)

    return {
        "mensaje": "Residente creado correctamente",
        "id": nuevo.id,
        "nombre": nuevo.nombre
    }


# ---------------------------------------------
# ENDPOINT: Ver QR en navegador
# ---------------------------------------------
@app.get("/ver-qr/{residente_id}", response_class=HTMLResponse)
def ver_qr_residente(residente_id: int):
    ruta_qr = f"qr_residentes/qr_residente_{residente_id}.png"
    if not os.path.exists(ruta_qr):
        raise HTTPException(status_code=404, detail="QR no encontrado")

    with open(ruta_qr, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    html = f"""
    <html>
        <body>
            <h3>QR del residente {residente_id}</h3>
            <img src="data:image/png;base64,{encoded_string}" alt="QR Code" />
            <br><br>
            <a href="/descargar-qr/{residente_id}" download>
                <button>Descargar QR</button>
            </a>
        </body>
    </html>
    """
    return HTMLResponse(content=html)


# ---------------------------------------------
# ENDPOINT: Descargar QR directamente
# ---------------------------------------------
@app.get("/descargar-qr/{residente_id}")
def descargar_qr(residente_id: int):
    ruta_qr = f"qr_residentes/qr_residente_{residente_id}.png"
    if not os.path.exists(ruta_qr):
        raise HTTPException(status_code=404, detail="QR no encontrado")
    return FileResponse(
        ruta_qr,
        media_type="image/png",
        filename=f"qr_residente_{residente_id}.png"
    )
