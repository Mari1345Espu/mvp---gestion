from app.db.session import get_db
from app.modelos.programa import Programa
from app.modelos.extension import Extension
from app.modelos.facultad import Facultad
from app.modelos.estado import Estado
from app.modelos.tipo_proyecto import TipoProyecto
from sqlalchemy.orm import Session

def crear_datos_fijos():
    db: Session = next(get_db())

    # Obtener o crear estado 'Activo'
    estado = db.query(Estado).filter_by(nombre="Activo").first()
    if not estado:
        estado = Estado(nombre="Activo")
        db.add(estado)
        db.commit()
        db.refresh(estado)

    # Facultades
    facultades = [
        "Facultad de Ciencias Básicas e Ingeniería",
        "Facultad de Ciencias Económicas y Administrativas",
        "Facultad de Ciencias de la Salud",
        "Facultad de Ciencias Sociales, Humanidades y Educación"
    ]
    for nombre in facultades:
        if not db.query(Facultad).filter_by(nombre=nombre).first():
            db.add(Facultad(nombre=nombre, estado_id=estado.id))
    db.commit()

    # Programas
    programas = [
        "Ingeniería de Sistemas",
        "Administración de Empresas",
        "Enfermería",
        "Psicología"
    ]
    for nombre in programas:
        if not db.query(Programa).filter_by(nombre=nombre).first():
            db.add(Programa(nombre=nombre, estado_id=estado.id))
    db.commit()

    # Extensiones
    extensiones = [
        "Extensión Girardot",
        "Extensión Soacha",
        "Extensión Ubaté",
        "Extensión Chía"
    ]
    for nombre in extensiones:
        if not db.query(Extension).filter_by(nombre=nombre).first():
            db.add(Extension(nombre=nombre, estado_id=estado.id))
    db.commit()

    # Tipos de Proyecto
    tipos = [
        "Investigación",
        "Extensión",
        "Innovación"
    ]
    for nombre in tipos:
        if not db.query(TipoProyecto).filter_by(nombre=nombre).first():
            db.add(TipoProyecto(nombre=nombre, estado_id=estado.id))
    db.commit()

    print("Datos fijos insertados correctamente con estado Activo.")

if __name__ == "__main__":
    crear_datos_fijos() 