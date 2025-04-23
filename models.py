from sqlalchemy import Column, Integer, String, Boolean, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Tabla de Residentes
class Residente(Base):
    __tablename__ = "residentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    domicilio = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True)
    num_autos = Column(Integer, nullable=False, default=0)
    num_personas = Column(Integer, nullable=False, default=0)
    adeudo = Column(Integer, nullable=False, default=0)

    visitas = relationship("Visita", back_populates="residente")
    autos = relationship("Auto", back_populates="residente", cascade="all, delete-orphan")
    personas = relationship("Persona", back_populates="residente", cascade="all, delete-orphan")
    adeudos = relationship("Adeudo", back_populates="residente", cascade="all, delete-orphan")


# Tabla de Visitas
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


# Tabla de Autos
class Auto(Base):
    __tablename__ = "autos"

    id = Column(Integer, primary_key=True)
    placas = Column(String, nullable=False)
    modelo = Column(String, nullable=True)

    residente_id = Column(Integer, ForeignKey("residentes.id"))
    residente = relationship("Residente", back_populates="autos")


# Tabla de Personas asociadas al domicilio
class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    parentesco = Column(String, nullable=False)

    residente_id = Column(Integer, ForeignKey("residentes.id"))
    residente = relationship("Residente", back_populates="personas")


# Tabla de Adeudos
class Adeudo(Base):
    __tablename__ = "adeudos"

    id = Column(Integer, primary_key=True)
    concepto = Column(String, nullable=False)
    monto = Column(Integer, nullable=False)
    estado = Column(String, nullable=False)  # Ej: Pendiente, Pagado, Vencido

    residente_id = Column(Integer, ForeignKey("residentes.id"))
    residente = relationship("Residente", back_populates="adeudos")
