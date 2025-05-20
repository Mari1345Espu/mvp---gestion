from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.modelos.usuario import Usuario
from app.modelos.rol import Rol
from app.modelos.estado import Estado
from app.modelos.tipo_proyecto import TipoProyecto
from app.modelos.proyecto import Proyecto
from app.modelos.convocatoria import Convocatoria
from app.modelos.programa import Programa
from app.modelos.grupoinvestigacion import GrupoInvestigacion
from app.modelos.lineainvestigacion import LineaInvestigacion
from datetime import datetime, timedelta
import random
from app.core.seguridad import get_password_hash

def crear_datos_prueba():
    db = SessionLocal()
    try:
        # Crear roles si no existen
        roles_nuevos = [
            "Admin",
            "Administrador CTI",
            "Líder de Grupo",
            "Investigador",
            "Evaluador",
            "Usuario"
        ]
        for nombre_rol in roles_nuevos:
            if not db.query(Rol).filter(Rol.nombre == nombre_rol).first():
                db.add(Rol(nombre=nombre_rol))
        db.commit()

        # Crear estados
        estados = [
            Estado(nombre="En Proceso", descripcion="Proyecto en desarrollo"),
            Estado(nombre="Finalizado", descripcion="Proyecto completado"),
            Estado(nombre="Suspendido", descripcion="Proyecto temporalmente suspendido"),
            Estado(nombre="Cancelado", descripcion="Proyecto cancelado")
        ]
        for estado in estados:
            db.add(estado)
        db.commit()

        # Crear tipos de proyecto
        tipos_proyecto = [
            TipoProyecto(nombre="Investigación", descripcion="Proyecto de investigación"),
            TipoProyecto(nombre="Extensión", descripcion="Proyecto de extensión"),
            TipoProyecto(nombre="Innovación", descripcion="Proyecto de innovación")
        ]
        for tipo in tipos_proyecto:
            db.add(tipo)
        db.commit()

        # Crear convocatorias
        convocatorias = [
            Convocatoria(nombre="Convocatoria 2024-1", fecha_inicio=datetime.now(), fecha_fin=datetime.now() + timedelta(days=180)),
            Convocatoria(nombre="Convocatoria 2023-2", fecha_inicio=datetime.now() - timedelta(days=180), fecha_fin=datetime.now() - timedelta(days=30))
        ]
        for conv in convocatorias:
            db.add(conv)
        db.commit()

        # Crear programas
        programas = [
            Programa(nombre="Ingeniería de Sistemas", facultad="Facultad de Ingeniería"),
            Programa(nombre="Ingeniería Industrial", facultad="Facultad de Ingeniería"),
            Programa(nombre="Administración de Empresas", facultad="Facultad de Ciencias Económicas")
        ]
        for prog in programas:
            db.add(prog)
        db.commit()

        # Crear grupos de investigación
        grupos = [
            GrupoInvestigacion(nombre="GIDITI", descripcion="Grupo de Investigación en Desarrollo e Innovación Tecnológica"),
            GrupoInvestigacion(nombre="GICEA", descripcion="Grupo de Investigación en Ciencias Económicas y Administrativas")
        ]
        for grupo in grupos:
            db.add(grupo)
        db.commit()

        # Crear líneas de investigación
        lineas = [
            LineaInvestigacion(nombre="Inteligencia Artificial", descripcion="Investigación en IA y Machine Learning"),
            LineaInvestigacion(nombre="Desarrollo Sostenible", descripcion="Investigación en sostenibilidad y medio ambiente")
        ]
        for linea in lineas:
            db.add(linea)
        db.commit()

        # Crear usuarios de prueba
        usuarios = [
            Usuario(
                nombre="Admin CTI",
                correo="admin@ucundinamarca.edu.co",
                contraseña=get_password_hash("admin123"),
                rol_id=db.query(Rol).filter(Rol.nombre == "Administrador CTI").first().id,
                telefono="",
                foto=None
            ),
            Usuario(
                nombre="Investigador Prueba",
                correo="investigador@ucundinamarca.edu.co",
                contraseña=get_password_hash("invest123"),
                rol_id=db.query(Rol).filter(Rol.nombre == "Investigador").first().id,
                telefono="",
                foto=None
            ),
            Usuario(
                nombre="Evaluador Prueba",
                correo="evaluador@ucundinamarca.edu.co",
                contraseña=get_password_hash("eval123"),
                rol_id=db.query(Rol).filter(Rol.nombre == "Evaluador").first().id,
                telefono="",
                foto=None
            )
        ]
        for usuario in usuarios:
            db.add(usuario)
        db.commit()

        # Crear proyectos
        proyectos = []
        for i in range(10):
            proyecto = Proyecto(
                titulo=f"Proyecto de {random.choice(['Investigación', 'Extensión', 'Innovación'])} {i+1}",
                objetivos=f"Objetivos del proyecto {i+1}",
                resumen=f"Resumen del proyecto {i+1}",
                problematica=f"Problemática del proyecto {i+1}",
                fecha_inicio=datetime.now() - timedelta(days=random.randint(0, 180)),
                convocatoria_id=random.choice([c.id for c in convocatorias]),
                programa_id=random.choice([p.id for p in programas]),
                grupo_investigacion_id=random.choice([g.id for g in grupos]),
                linea_investigacion_id=random.choice([l.id for l in lineas]),
                estado_id=random.choice([e.id for e in estados]),
                tipo_proyecto_id=random.choice([t.id for t in tipos_proyecto])
            )
            proyectos.append(proyecto)
            db.add(proyecto)
        db.commit()

        print("¡Datos de prueba creados exitosamente!")
        
    except Exception as e:
        print(f"Error al crear datos de prueba: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    crear_datos_prueba() 