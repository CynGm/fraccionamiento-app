from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time


# -------------------------------
# VISITAS
# -------------------------------

class VisitaEntrada(BaseModel):
    nombre_visitante: str
    motivo_visita: Optional[str] = None
    fecha_visita: date
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None
    vehiculo_placas: Optional[str] = None
    preregistro: bool = False
    residente_id: int

    model_config = {
        "from_attributes": True
    }

class VisitaSalida(BaseModel):
    id: int
    hora_salida: time

    model_config = {
        "from_attributes": True
    }

class VisitaOut(BaseModel):
    id: int
    nombre_visitante: str
    motivo_visita: Optional[str] = None
    fecha_visita: date
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None
    vehiculo_placas: Optional[str] = None
    preregistro: bool
    residente_id: int

    model_config = {
        "from_attributes": True
    }


# -------------------------------
# AUTOS
# -------------------------------

class AutoCreate(BaseModel):
    placas: str
    modelo: Optional[str] = None

class AutoOut(AutoCreate):
    id: int
    model_config = {
        "from_attributes": True
    }


# -------------------------------
# PERSONAS
# -------------------------------

class PersonaCreate(BaseModel):
    nombre: str
    parentesco: str

class PersonaOut(PersonaCreate):
    id: int
    model_config = {
        "from_attributes": True
    }


# -------------------------------
# ADEUDOS
# -------------------------------

class AdeudoCreate(BaseModel):
    concepto: str
    monto: int
    estado: str  # Ejemplo: "Pendiente", "Pagado", etc.

class AdeudoOut(AdeudoCreate):
    id: int
    model_config = {
        "from_attributes": True
    }


# -------------------------------
# RESIDENTES
# -------------------------------

class ResidenteCreate(BaseModel):
    nombre: str
    domicilio: str
    telefono: str
    correo: str
    num_autos: int
    num_personas: int
    adeudo: Optional[int] = 0

    autos: List[AutoCreate] = []
    personas: List[PersonaCreate] = []
    adeudos: List[AdeudoCreate] = []

class ResidenteSchema(BaseModel):
    id: int
    nombre: str
    domicilio: str
    telefono: str
    correo: str
    num_autos: int
    num_personas: int
    adeudo: int

    autos: List[AutoOut] = []
    personas: List[PersonaOut] = []
    adeudos: List[AdeudoOut] = []

    model_config = {
        "from_attributes": True
    }
