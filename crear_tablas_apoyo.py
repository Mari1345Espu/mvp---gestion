from app.db.base import Base
from app.db.session import engine
# Importar todos los modelos para que se creen las tablas
import app.modelos
from app.core.seguridad import get_password_hash

def fill_roles(db):
    from app.modelos.rol import Rol
    if not db.query(Rol).first():
        roles = [
            Rol(nombre="Administrador CTI"),
            Rol(nombre="Líder de Grupo"),
            Rol(nombre="Investigador"),
            Rol(nombre="Evaluador")
        ]
        db.add_all(roles)
        db.commit()
        print("Roles creados")

def fill_estados(db):
    from app.modelos.estado import Estado
    if not db.query(Estado).first():
        estados = [Estado(nombre="Activo"), Estado(nombre="Inactivo")]
        db.add_all(estados)
        db.commit()
        print("Estados creados")

def fill_usuarios(db):
    from app.modelos.usuario import Usuario
    user = db.query(Usuario).filter(Usuario.correo == "admin_cti@example.com").first()
    if not user:
        hashed_password = get_password_hash("admincti123")
        new_user = Usuario(
            correo="admin_cti@example.com",
            nombre="Administrador CTI",
            contraseña=hashed_password,
            telefono="1234567890",
            foto=None,
            rol_id=1,
            estado_id=1,
            tipo_estado_id=1
        )
        db.add(new_user)
        db.commit()
        print("Usuario admin creado con correo: admin_cti@example.com y contraseña: admincti123")
    else:
        print("Usuario admin ya existe")

def fill_proyectos(db):
    from app.modelos.proyecto import Proyecto
    if not db.query(Proyecto).first():
        proyectos = [
            Proyecto(titulo="Proyecto 1", objetivos="Descripción del proyecto 1"),
            Proyecto(titulo="Proyecto 2", objetivos="Descripción del proyecto 2")
        ]
        db.add_all(proyectos)
        db.commit()
        print("Proyectos creados")

def fill_cronogramas(db):
    from app.modelos.cronograma import Cronograma
    from datetime import datetime
    if not db.query(Cronograma).first():
        cronogramas = [
            Cronograma(fecha_creacion=datetime.now(), estado_id=1, tipo_estado_id=1),
            Cronograma(fecha_creacion=datetime.now(), estado_id=1, tipo_estado_id=1)
        ]
        db.add_all(cronogramas)
        db.commit()
        print("Cronogramas creados")

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("¡Todas las tablas han sido creadas correctamente!")
