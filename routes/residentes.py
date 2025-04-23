from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Residente, Auto, Persona, Adeudo
from schemas import ResidenteCreate, ResidenteSchema

router = APIRouter()


# ✅ CREAR RESIDENTE COMPLETO
@router.post("/residentes", response_model=ResidenteSchema)
def crear_residente_completo(residente: ResidenteCreate, db: Session = Depends(get_db)):
    nuevo = Residente(
        nombre=residente.nombre,
        domicilio=residente.domicilio,
        telefono=residente.telefono,
        correo=residente.correo,
        num_autos=residente.num_autos,
        num_personas=residente.num_personas,
        adeudo=residente.adeudo
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    for auto in residente.autos:
        db.add(Auto(placas=auto.placas, modelo=auto.modelo, residente_id=nuevo.id))

    for persona in residente.personas:
        db.add(Persona(nombre=persona.nombre, parentesco=persona.parentesco, residente_id=nuevo.id))

    for adeudo in residente.adeudos:
        db.add(Adeudo(concepto=adeudo.concepto, monto=adeudo.monto, estado=adeudo.estado, residente_id=nuevo.id))

    db.commit()
    return nuevo


# ✅ CONSULTAR TODOS LOS RESIDENTES
@router.get("/residentes", response_model=list[ResidenteSchema])
def obtener_residentes(
    db: Session = Depends(get_db),
    correo: str = Query(None),
    nombre: str = Query(None)
):
    query = db.query(Residente)

    if correo:
        query = query.filter(Residente.correo.ilike(f"%{correo}%"))
    if nombre:
        query = query.filter(Residente.nombre.ilike(f"%{nombre}%"))

    return query.all()


# ✅ ACTUALIZAR RESIDENTE COMPLETO
@router.put("/residentes/{residente_id}", response_model=ResidenteSchema)
def actualizar_residente(residente_id: int, datos: ResidenteCreate, db: Session = Depends(get_db)):
    residente = db.query(Residente).filter(Residente.id == residente_id).first()
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")

    residente.nombre = datos.nombre
    residente.domicilio = datos.domicilio
    residente.telefono = datos.telefono
    residente.correo = datos.correo
    residente.num_autos = datos.num_autos
    residente.num_personas = datos.num_personas
    residente.adeudo = datos.adeudo

    # Borrar autos, personas y adeudos anteriores
    db.query(Auto).filter(Auto.residente_id == residente.id).delete()
    db.query(Persona).filter(Persona.residente_id == residente.id).delete()
    db.query(Adeudo).filter(Adeudo.residente_id == residente.id).delete()

    # Agregar nuevos
    for auto in datos.autos:
        db.add(Auto(placas=auto.placas, modelo=auto.modelo, residente_id=residente.id))

    for persona in datos.personas:
        db.add(Persona(nombre=persona.nombre, parentesco=persona.parentesco, residente_id=residente.id))

    for adeudo in datos.adeudos:
        db.add(Adeudo(concepto=adeudo.concepto, monto=adeudo.monto, estado=adeudo.estado, residente_id=residente.id))

    db.commit()
    db.refresh(residente)

    return residente

@router.delete("/residentes/{residente_id}")
def eliminar_residente(residente_id: int, db: Session = Depends(get_db)):
    residente = db.query(Residente).filter(Residente.id == residente_id).first()
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")

    # Eliminar autos, personas y adeudos primero (por seguridad)
    db.query(Auto).filter(Auto.residente_id == residente_id).delete()
    db.query(Persona).filter(Persona.residente_id == residente_id).delete()
    db.query(Adeudo).filter(Adeudo.residente_id == residente_id).delete()

    # Eliminar el residente
    db.delete(residente)
    db.commit()

    return {"mensaje": f"Residente con ID {residente_id} eliminado correctamente."}
