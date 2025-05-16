from app.db.session import SessionLocal
from app.modelos.usuario import Usuario
from app.modelos.rol import Rol
from app.core.seguridad import get_password_hash

def create_users():
    db = SessionLocal()
    try:
        # Obtener roles existentes sin importar otros modelos
        roles = {rol.nombre: rol.id for rol in db.query(Rol).all()}

        # Definir usuarios a crear con roles y contraseñas
        usuarios_data = [
            {"correo": "admin_cti@example.com", "nombre": "Admin CTI", "contraseña": "admincti123", "rol": "Admin"},
            {"correo": "lider_grupo@example.com", "nombre": "Líder de Grupo", "contraseña": "lider123", "rol": "Usuario"},
            {"correo": "investigador@example.com", "nombre": "Investigador", "contraseña": "invest123", "rol": "Usuario"},
            {"correo": "evaluador@example.com", "nombre": "Evaluador", "contraseña": "eval123", "rol": "Usuario"},
        ]

        for udata in usuarios_data:
            # Verificar si usuario ya existe
            user = db.query(Usuario).filter(Usuario.correo == udata["correo"]).first()
            if not user:
                hashed_password = get_password_hash(udata["contraseña"])
                rol_id = roles.get(udata["rol"])
                new_user = Usuario(
                    correo=udata["correo"],
                    nombre=udata["nombre"],
                    contraseña=hashed_password,
                    rol_id=rol_id,
                    telefono="",
                    foto=None,
                    estado_id=1  # Asumiendo 1 es activo
                )
                db.add(new_user)
                print(f"Creado usuario: {udata['nombre']} con rol {udata['rol']}")
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    create_users()
