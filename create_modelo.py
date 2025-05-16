from app.db.session import SessionLocal
from app.db.base import Base
from app.modelos import *
from sqlalchemy import create_engine
import os
from crear_tablas_apoyo import fill_roles, fill_estados, fill_usuarios, fill_proyectos, fill_cronogramas

def recreate_database():
    # Eliminar archivo de base de datos si existe (SQLite)
    db_path = "test.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Archivo {db_path} eliminado.")

    # Crear motor de base de datos
    engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})

    # Crear todas las tablas según los modelos actuales
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas según los modelos actuales.")

def init_db_from_scratch():
    recreate_database()
    db = SessionLocal()
    try:
        print("Poblando roles...")
        fill_roles(db)
        print("Poblando estados...")
        fill_estados(db)
        print("Poblando usuarios...")
        fill_usuarios(db)
        print("Poblando proyectos...")
        fill_proyectos(db)
        print("Poblando cronogramas...")
        fill_cronogramas(db)
    finally:
        db.close()

if __name__ == "__main__":
    init_db_from_scratch()
