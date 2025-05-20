from app.db.session import engine, SessionLocal
from app.db.base import Base
from app import modelos
from sqlalchemy.orm import Session
from app.core.seguridad import get_password_hash
from datetime import datetime, timedelta

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
        import app.modelos.tipo_estado
        import app.modelos.programa
        import app.modelos.facultad
        import app.modelos.extension
        import app.modelos.tipo_proyecto

        # Crear tipos de estado
        from app.modelos.tipo_estado import TipoEstado
        if not db.query(TipoEstado).first():
            tipos_estado = [
                TipoEstado(nombre="Activo"),
                TipoEstado(nombre="Inactivo"),
                TipoEstado(nombre="Pendiente"),
                TipoEstado(nombre="Finalizado")
            ]
            db.add_all(tipos_estado)
            db.commit()
            print("Tipos de estado creados")

        # Crear estados
        from app.modelos.estado import Estado
        if not db.query(Estado).first():
            estados = [
                Estado(nombre="Activo"),
                Estado(nombre="Inactivo"),
                Estado(nombre="Pendiente"),
                Estado(nombre="Finalizado")
            ]
            db.add_all(estados)
            db.commit()
            print("Estados creados")

        # Crear roles
        from app.modelos.rol import Rol
        if not db.query(Rol).first():
            roles = [
                Rol(nombre="Administrador CTI"),
                Rol(nombre="Asesor"),
                Rol(nombre="Evaluador"),
                Rol(nombre="Líder"),
                Rol(nombre="Investigador")
            ]
            db.add_all(roles)
            db.commit()
            print("Roles creados")

        # Crear usuario admin
        from app.modelos.usuario import Usuario
        user = db.query(Usuario).filter(Usuario.correo == "admin@example.com").first()
        if not user:
            hashed_password = get_password_hash("admin123")
            new_user = Usuario(
                correo="admin@example.com",
                nombre="Administrador CTI",
                contraseña=hashed_password,
                telefono="1234567890",
                foto=None,
                rol_id=1,  # ID del rol Administrador CTI
                estado_id=1,  # Activo
                tipo_estado_id=1  # Activo
            )
            db.add(new_user)
            db.commit()
            print("Usuario admin creado con correo: admin@example.com y contraseña: admin123")
        else:
            print("Usuario admin ya existe")

        # Crear programas
        from app.modelos.programa import Programa
        if not db.query(Programa).first():
            programas = [
                Programa(
                    nombre="Ingeniería de Sistemas",
                    descripcion="Programa de Ingeniería de Sistemas",
                    estado_id=1,  # Activo
                    tipo_estado_id=1  # Activo
                ),
                Programa(
                    nombre="Ingeniería Industrial",
                    descripcion="Programa de Ingeniería Industrial",
                    estado_id=1,  # Activo
                    tipo_estado_id=1  # Activo
                )
            ]
            db.add_all(programas)
            db.commit()
            print("Programas creados")

        # Crear facultades
        from app.modelos.facultad import Facultad
        if not db.query(Facultad).first():
            facultades = [
                Facultad(
                    nombre="Facultad de Ingeniería",
                    descripcion="Facultad de Ingeniería",
                    estado_id=1,  # Activo
                    tipo_estado_id=1  # Activo
                ),
                Facultad(
                    nombre="Facultad de Ciencias",
                    descripcion="Facultad de Ciencias",
                    estado_id=1,  # Activo
                    tipo_estado_id=1  # Activo
                )
            ]
            db.add_all(facultades)
            db.commit()
            print("Facultades creadas")

        # Crear extensiones
        from app.modelos.extension import Extension
        if not db.query(Extension).first():
            extensiones = [
                Extension(
                    nombre="Extensión Fusagasugá",
                    descripcion="Extensión en Fusagasugá",
                    estado_id=1,  # Activo
                    tipo_estado_id=1  # Activo
                ),
                Extension(
                    nombre="Extensión Girardot",
                    descripcion="Extensión en Girardot",
                    estado_id=1,  # Activo
                    tipo_estado_id=1  # Activo
                )
            ]
            db.add_all(extensiones)
            db.commit()
            print("Extensiones creadas")

        # Crear tipos de proyecto
        from app.modelos.tipo_proyecto import TipoProyecto
        if not db.query(TipoProyecto).first():
            tipos_proyecto = [
                TipoProyecto(
                    nombre="Investigación",
                    descripcion="Proyecto de Investigación",
                    estado_id=1  # Activo
                ),
                TipoProyecto(
                    nombre="Extensión",
                    descripcion="Proyecto de Extensión",
                    estado_id=1  # Activo
                )
            ]
            db.add_all(tipos_proyecto)
            db.commit()
            print("Tipos de proyecto creados")

        # Crear usuarios de prueba para cada rol
        usuarios_prueba = [
            {
                "correo": "asesor@example.com",
                "nombre": "Asesor Prueba",
                "contraseña": "asesor123",
                "rol_id": 2
            },
            {
                "correo": "evaluador@example.com",
                "nombre": "Evaluador Prueba",
                "contraseña": "evaluador123",
                "rol_id": 3
            },
            {
                "correo": "lider@example.com",
                "nombre": "Líder Prueba",
                "contraseña": "lider123",
                "rol_id": 4
            },
            {
                "correo": "investigador@example.com",
                "nombre": "Investigador Prueba",
                "contraseña": "investigador123",
                "rol_id": 5
            }
        ]
        for u in usuarios_prueba:
            if not db.query(Usuario).filter(Usuario.correo == u["correo"]).first():
                db.add(Usuario(
                    correo=u["correo"],
                    nombre=u["nombre"],
                    contraseña=get_password_hash(u["contraseña"]),
                    telefono="1234567890",
                    foto=None,
                    rol_id=u["rol_id"],
                    estado_id=1,  # Activo
                    tipo_estado_id=1  # Activo
                ))
        db.commit()
        print("Usuarios de prueba creados")

    finally:
        db.close()

if __name__ == "__main__":
    init_db() 