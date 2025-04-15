from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Residente, Visita
from schemas import VisitaSchema, ResidenteSchema

app = FastAPI()

# -------------------------------
# ENDPOINT: Inicio
# -------------------------------
@app.get("/")
def inicio():
    return {"mensaje": "¡Servidor corriendo correctamente!"}


# -------------------------------
# ENDPOINT: Registrar Residente
# -------------------------------
@app.post("/registrar-residente")
def registrar_residente(residente: ResidenteSchema, db: Session = Depends(get_db)):
    db_residente = db.query(Residente).filter(Residente.correo == residente.correo).first()
    if db_residente:
        raise HTTPException(status_code=400, detail="Este correo ya está registrado.")

    nuevo_residente = Residente(**residente.dict())
    db.add(nuevo_residente)
    db.commit()
    db.refresh(nuevo_residente)

    return {"mensaje": "Residente registrado exitosamente"}


# -------------------------------
# ENDPOINT: Registrar Visita
# -------------------------------
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

