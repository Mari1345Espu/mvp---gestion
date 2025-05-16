from app.db.session import engine, SessionLocal
from app.db.base import Base
from app import modelos
from sqlalchemy.orm import Session
from crear_tablas_apoyo import (
    fill_roles,
    fill_estados,
    fill_usuarios,
    fill_proyectos,
    fill_cronogramas,
)

def init_db():
    # Crear tablas
    Base.metadata.create_all(bind=engine)

    # Crear sesión
    db = SessionLocal()

    try:
        # Importar modelos para evitar errores de relación
        import app.modelos.rol
        import app.modelos.estado
        import app.modelos.usuario
        import app.modelos.proyecto
        import app.modelos.cronograma

        # Llenar datos iniciales
        fill_roles(db)
        fill_estados(db)
        fill_usuarios(db)
        fill_proyectos(db)
        fill_cronogramas(db)

    finally:
        db.close()

if __name__ == "__main__":
    init_db()
