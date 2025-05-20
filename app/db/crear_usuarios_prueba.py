from app.db.session import get_db
from app.modelos.usuario import Usuario
from app.modelos.rol import Rol
from app.core.seguridad import get_password_hash
from sqlalchemy.orm import Session

def crear_usuarios_prueba():
    db: Session = next(get_db())

    # Crear roles si no existen
    roles = ["Administrador", "Investigador", "Evaluador"]
    rol_objs = {}
    for nombre_rol in roles:
        rol = db.query(Rol).filter_by(nombre=nombre_rol).first()
        if not rol:
            rol = Rol(nombre=nombre_rol)
            db.add(rol)
            db.commit()
            db.refresh(rol)
        rol_objs[nombre_rol] = rol

    # Crear usuarios de prueba
    usuarios = [
        {"nombre": "Admin UDEC", "correo": "admin@udec.edu.co", "contraseña": "admin123", "rol": rol_objs["Administrador"]},
        {"nombre": "Investigador Uno", "correo": "inv1@udec.edu.co", "contraseña": "inv123", "rol": rol_objs["Investigador"]},
        {"nombre": "Evaluador Uno", "correo": "eval1@udec.edu.co", "contraseña": "eval123", "rol": rol_objs["Evaluador"]},
    ]

    for u in usuarios:
        if not db.query(Usuario).filter_by(correo=u["correo"]).first():
            usuario = Usuario(
                nombre=u["nombre"],
                correo=u["correo"],
                contraseña=get_password_hash(u["contraseña"]),
                rol_id=u["rol"].id
            )
            db.add(usuario)
            db.commit()
            print(f"Usuario creado: {u['correo']} ({u['rol'].nombre})")
        else:
            print(f"Usuario ya existe: {u['correo']}")

if __name__ == "__main__":
    crear_usuarios_prueba() 