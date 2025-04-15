from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class VisitaSchema(BaseModel):
    nombre_visitante: str
    motivo_visita: str
    fecha_visita: date
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None
    vehiculo_placas: str
    preregistro: bool = False
    residente_id: int

    model_config = {
    "from_attributes": True
}


class ResidenteSchema(BaseModel):
    nombre: str
    domicilio: str
    telefono: str
    correo: str
    num_autos: int
    num_personas: int
    adeudo: int = 0

    model_config = {
    "from_attributes": True
}

