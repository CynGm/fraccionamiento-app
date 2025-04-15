from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Ruta a la base de datos SQLite
DATABASE_URL = "sqlite:///./residencias.db"

# Crear el motor de conexión
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear la clase de sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
