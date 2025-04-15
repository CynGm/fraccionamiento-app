from sqlalchemy import Column, Integer, String, Boolean, Date, Time, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Residente(Base):
    __tablename__ = "residentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    domicilio = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True)
    num_autos = Column(Integer, nullable=False)
    num_personas = Column(Integer, nullable=False)
    adeudo = Column(Integer, default=0)

    visitas = relationship("Visita", back_populates="residente")


class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    nombre_visitante = Column(String, nullable=False)
    motivo_visita = Column(String, nullable=True)
    fecha_visita = Column(Date, nullable=False)
    hora_entrada = Column(Time, nullable=True)
    hora_salida = Column(Time, nullable=True)
    vehiculo_placas = Column(String, nullable=True)
    preregistro = Column(Boolean, default=False)

    residente_id = Column(Integer, ForeignKey("residentes.id"))
    residente = relationship("Residente", back_populates="visitas")
