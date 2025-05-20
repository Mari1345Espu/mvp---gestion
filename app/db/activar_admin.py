from app.db.session import get_db
from app.modelos.usuario import Usuario
from app.modelos.estado import Estado
from sqlalchemy.orm import Session

def activar_admin():
    db: Session = next(get_db())
    admin = db.query(Usuario).filter_by(correo="admin@udec.edu.co").first()
    if not admin:
        print("No existe el usuario admin@udec.edu.co")
        return
    estado = db.query(Estado).filter_by(nombre="Activo").first()
    if not estado:
        estado = Estado(nombre="Activo")
        db.add(estado)
        db.commit()
        db.refresh(estado)
    admin.estado_id = estado.id
    db.commit()
    print("Usuario admin@udec.edu.co activado correctamente.")

if __name__ == "__main__":
    activar_admin() 