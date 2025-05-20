from sqlalchemy import create_engine
from app.db.base import Base
from app.modelos.proyecto import Proyecto
from app.modelos.tipo_proyecto import TipoProyecto
from app.modelos.estado import Estado
from app.modelos.tipo_estado import TipoEstado
from app.modelos.seguimiento import Seguimiento
from app.modelos.usuario import Usuario
from app.modelos.rol import Rol
from app.modelos.convocatoria import Convocatoria
from app.modelos.programa import Programa
from app.modelos.grupoinvestigacion import GrupoInvestigacion
from app.modelos.lineainvestigacion import LineaInvestigacion
from app.db.crear_datos_prueba import crear_datos_prueba

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

def init_db():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Crear datos de prueba
    crear_datos_prueba()

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada y datos de prueba creados exitosamente!") 