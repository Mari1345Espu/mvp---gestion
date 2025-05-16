from app.db.session import SessionLocal
from app.modelos.usuario import Usuario
from app.core.seguridad import get_password_hash

def create_simple_users():
    db = SessionLocal()
    try:
        # IDs fijos para roles (ajustar según la base de datos)
        roles_ids = {
            "Admin": 1,
            "Lider": 2,
            "Investigador": 3,
            "Evaluador": 4
        }

        usuarios_data = [
            {"correo": "admin_cti@example.com", "nombre": "Admin CTI", "contraseña": "admincti123", "rol_id": roles_ids["Admin"]},
            {"correo": "lider_grupo@example.com", "nombre": "Líder de Grupo", "contraseña": "lider123", "rol_id": roles_ids["Lider"]},
            {"correo": "investigador@example.com", "nombre": "Investigador", "contraseña": "invest123", "rol_id": roles_ids["Investigador"]},
            {"correo": "evaluador@example.com", "nombre": "Evaluador", "contraseña": "eval123", "rol_id": roles_ids["Evaluador"]},
        ]

        for udata in usuarios_data:
            user = db.query(Usuario).filter(Usuario.correo == udata["correo"]).first()
            if not user:
                hashed_password = get_password_hash(udata["contraseña"])
                new_user = Usuario(
                    correo=udata["correo"],
                    nombre=udata["nombre"],
                    contraseña=hashed_password,
                    rol_id=udata["rol_id"],
                    telefono="",
                    foto=None,
                    estado_id=1,  # Asumiendo 1 es activo
                    tipo_estado_id=1  # Asumiendo 1 es tipo estado válido
                )
                db.add(new_user)
                print(f"Creado usuario: {udata['nombre']} con rol ID {udata['rol_id']}")
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    create_simple_users()
