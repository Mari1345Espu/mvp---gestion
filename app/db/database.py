from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_config
import os

config = get_config()

# Asegurarse de que el directorio de la base de datos existe
db_dir = os.path.dirname(config.DATABASE_URL.replace('sqlite:///', ''))
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Crear el engine de SQLite
engine = create_engine(
    config.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base para los modelos
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 