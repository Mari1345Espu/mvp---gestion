from app.db.session import engine, SessionLocal
from app.db.base import Base
from app import modelos
from sqlalchemy.orm import Session
from app.core.seguridad import get_password_hash

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
        import app.modelos.anexo
        import app.modelos.auditoria
        import app.modelos.avance
        import app.modelos.cierre
        import app.modelos.conceptoevaluacion
        import app.modelos.convocatoria
        import app.modelos.destino
        import app.modelos.evaluacion
        import app.modelos.extension
        import app.modelos.facultad
        import app.modelos.grupoinvestigacion
        import app.modelos.impacto
        import app.modelos.lineainvestigacion
        import app.modelos.notificacion
        import app.modelos.participante
        import app.modelos.producto
        import app.modelos.programa
        import app.modelos.recurso
        import app.modelos.seguimiento
        import app.modelos.tarea
        import app.modelos.tipo_estado
        import app.modelos.tipo_proyecto

        # Crear roles
        from app.modelos.rol import Rol
        if not db.query(Rol).first():
            roles = [Rol(nombre="Admin"), Rol(nombre="Usuario")]
            db.add_all(roles)
            db.commit()
            print("Roles creados")

        # Crear estados
        from app.modelos.estado import Estado
        if not db.query(Estado).first():
            estados = [Estado(nombre="Activo"), Estado(nombre="Inactivo")]
            db.add_all(estados)
            db.commit()
            print("Estados creados")

        # Crear usuario inicial para login
        from app.modelos.usuario import Usuario
        user = db.query(Usuario).filter(Usuario.correo == "admin@example.com").first()
        if not user:
            hashed_password = get_password_hash("admin123")
            new_user = Usuario(
                correo="admin@example.com",
                nombre="Administrador",
                contraseña=hashed_password,
                telefono="1234567890",
                foto=None
            )
            db.add(new_user)
            db.commit()
            print("Usuario admin creado con correo: admin@example.com y contraseña: admin123")
        else:
            print("Usuario admin ya existe")

        # Crear proyectos
        from app.modelos.proyecto import Proyecto
        if not db.query(Proyecto).first():
            proyectos = [
                Proyecto(nombre="Proyecto 1", descripcion="Descripción del proyecto 1"),
                Proyecto(nombre="Proyecto 2", descripcion="Descripción del proyecto 2")
            ]
            db.add_all(proyectos)
            db.commit()
            print("Proyectos creados")

        # Crear cronogramas
        from app.modelos.cronograma import Cronograma
        if not db.query(Cronograma).first():
            cronogramas = [
                Cronograma(nombre="Cronograma 1", descripcion="Descripción del cronograma 1"),
                Cronograma(nombre="Cronograma 2", descripcion="Descripción del cronograma 2")
            ]
            db.add_all(cronogramas)
            db.commit()
            print("Cronogramas creados")

        # Crear anexos
        from app.modelos.anexo import Anexo
        if not db.query(Anexo).first():
            anexos = [
                Anexo(nombre="Anexo 1", descripcion="Descripción del anexo 1"),
                Anexo(nombre="Anexo 2", descripcion="Descripción del anexo 2")
            ]
            db.add_all(anexos)
            db.commit()
            print("Anexos creados")

        # Crear auditorias
        from app.modelos.auditoria import Auditoria
        if not db.query(Auditoria).first():
            auditorias = [
                Auditoria(nombre="Auditoria 1", descripcion="Descripción de la auditoria 1"),
                Auditoria(nombre="Auditoria 2", descripcion="Descripción de la auditoria 2")
            ]
            db.add_all(auditorias)
            db.commit()
            print("Auditorias creadas")

        # Crear avances
        from app.modelos.avance import Avance
        if not db.query(Avance).first():
            avances = [
                Avance(nombre="Avance 1", descripcion="Descripción del avance 1"),
                Avance(nombre="Avance 2", descripcion="Descripción del avance 2")
            ]
            db.add_all(avances)
            db.commit()
            print("Avances creados")

        # Crear cierres
        from app.modelos.cierre import Cierre
        if not db.query(Cierre).first():
            cierres = [
                Cierre(nombre="Cierre 1", descripcion="Descripción del cierre 1"),
                Cierre(nombre="Cierre 2", descripcion="Descripción del cierre 2")
            ]
            db.add_all(cierres)
            db.commit()
            print("Cierres creados")

        # Crear conceptos de evaluación
        from app.modelos.conceptoevaluacion import ConceptoEvaluacion
        if not db.query(ConceptoEvaluacion).first():
            conceptos = [
                ConceptoEvaluacion(nombre="Concepto 1", descripcion="Descripción del concepto 1"),
                ConceptoEvaluacion(nombre="Concepto 2", descripcion="Descripción del concepto 2")
            ]
            db.add_all(conceptos)
            db.commit()
            print("Conceptos de evaluación creados")

        # Crear convocatorias
        from app.modelos.convocatoria import Convocatoria
        if not db.query(Convocatoria).first():
            convocatorias = [
                Convocatoria(nombre="Convocatoria 1", descripcion="Descripción de la convocatoria 1"),
                Convocatoria(nombre="Convocatoria 2", descripcion="Descripción de la convocatoria 2")
            ]
            db.add_all(convocatorias)
            db.commit()
            print("Convocatorias creadas")

        # Crear destinos
        from app.modelos.destino import Destino
        if not db.query(Destino).first():
            destinos = [
                Destino(nombre="Destino 1", descripcion="Descripción del destino 1"),
                Destino(nombre="Destino 2", descripcion="Descripción del destino 2")
            ]
            db.add_all(destinos)
            db.commit()
            print("Destinos creados")

        # Crear evaluaciones
        from app.modelos.evaluacion import Evaluacion
        if not db.query(Evaluacion).first():
            evaluaciones = [
                Evaluacion(nombre="Evaluación 1", descripcion="Descripción de la evaluación 1"),
                Evaluacion(nombre="Evaluación 2", descripcion="Descripción de la evaluación 2")
            ]
            db.add_all(evaluaciones)
            db.commit()
            print("Evaluaciones creadas")

        # Crear extensiones
        from app.modelos.extension import Extension
        if not db.query(Extension).first():
            extensiones = [
                Extension(nombre="Extensión 1", descripcion="Descripción de la extensión 1"),
                Extension(nombre="Extensión 2", descripcion="Descripción de la extensión 2")
            ]
            db.add_all(extensiones)
            db.commit()
            print("Extensiones creadas")

        # Crear facultades
        from app.modelos.facultad import Facultad
        if not db.query(Facultad).first():
            facultades = [
                Facultad(nombre="Facultad 1", descripcion="Descripción de la facultad 1"),
                Facultad(nombre="Facultad 2", descripcion="Descripción de la facultad 2")
            ]
            db.add_all(facultades)
            db.commit()
            print("Facultades creadas")

        # Crear grupos de investigación
        from app.modelos.grupoinvestigacion import GrupoInvestigacion
        if not db.query(GrupoInvestigacion).first():
            grupos = [
                GrupoInvestigacion(nombre="Grupo 1", descripcion="Descripción del grupo 1"),
                GrupoInvestigacion(nombre="Grupo 2", descripcion="Descripción del grupo 2")
            ]
            db.add_all(grupos)
            db.commit()
            print("Grupos de investigación creados")

        # Crear impactos
        from app.modelos.impacto import Impacto
        if not db.query(Impacto).first():
            impactos = [
                Impacto(nombre="Impacto 1", descripcion="Descripción del impacto 1"),
                Impacto(nombre="Impacto 2", descripcion="Descripción del impacto 2")
            ]
            db.add_all(impactos)
            db.commit()
            print("Impactos creados")

        # Crear líneas de investigación
        from app.modelos.lineainvestigacion import LineaInvestigacion
        if not db.query(LineaInvestigacion).first():
            lineas = [
                LineaInvestigacion(nombre="Línea 1", descripcion="Descripción de la línea 1"),
                LineaInvestigacion(nombre="Línea 2", descripcion="Descripción de la línea 2")
            ]
            db.add_all(lineas)
            db.commit()
            print("Líneas de investigación creadas")

        # Crear notificaciones
        from app.modelos.notificacion import Notificacion
        if not db.query(Notificacion).first():
            notificaciones = [
                Notificacion(nombre="Notificación 1", descripcion="Descripción de la notificación 1"),
                Notificacion(nombre="Notificación 2", descripcion="Descripción de la notificación 2")
            ]
            db.add_all(notificaciones)
            db.commit()
            print("Notificaciones creadas")

        # Crear participantes
        from app.modelos.participante import Participante
        if not db.query(Participante).first():
            participantes = [
                Participante(nombre="Participante 1", descripcion="Descripción del participante 1"),
                Participante(nombre="Participante 2", descripcion="Descripción del participante 2")
            ]
            db.add_all(participantes)
            db.commit()
            print("Participantes creados")

        # Crear productos
        from app.modelos.producto import Producto
        if not db.query(Producto).first():
            productos = [
                Producto(nombre="Producto 1", descripcion="Descripción del producto 1"),
                Producto(nombre="Producto 2", descripcion="Descripción del producto 2")
            ]
            db.add_all(productos)
            db.commit()
            print("Productos creados")

        # Crear programas
        from app.modelos.programa import Programa
        if not db.query(Programa).first():
            programas = [
                Programa(nombre="Programa 1", descripcion="Descripción del programa 1"),
                Programa(nombre="Programa 2", descripcion="Descripción del programa 2")
            ]
            db.add_all(programas)
            db.commit()
            print("Programas creados")

        # Crear recursos
        from app.modelos.recurso import Recurso
        if not db.query(Recurso).first():
            recursos = [
                Recurso(descripcion="Recurso 1", cantidad=10),
                Recurso(descripcion="Recurso 2", cantidad=20)
            ]
            db.add_all(recursos)
            db.commit()
            print("Recursos creados")

        # Crear seguimientos
        from app.modelos.seguimiento import Seguimiento
        if not db.query(Seguimiento).first():
            seguimientos = [
                Seguimiento(nombre="Seguimiento 1", descripcion="Descripción del seguimiento 1"),
                Seguimiento(nombre="Seguimiento 2", descripcion="Descripción del seguimiento 2")
            ]
            db.add_all(seguimientos)
            db.commit()
            print("Seguimientos creados")

        # Crear tareas
        from app.modelos.tarea import Tarea
        if not db.query(Tarea).first():
            tareas = [
                Tarea(nombre="Tarea 1", descripcion="Descripción de la tarea 1"),
                Tarea(nombre="Tarea 2", descripcion="Descripción de la tarea 2")
            ]
            db.add_all(tareas)
            db.commit()
            print("Tareas creadas")

        # Crear tipos de estado
        from app.modelos.tipo_estado import TipoEstado
        if not db.query(TipoEstado).first():
            tipos_estado = [
                TipoEstado(nombre="Tipo Estado 1", descripcion="Descripción del tipo estado 1"),
                TipoEstado(nombre="Tipo Estado 2", descripcion="Descripción del tipo estado 2")
            ]
            db.add_all(tipos_estado)
            db.commit()
            print("Tipos de estado creados")

        # Crear tipos de proyecto
        from app.modelos.tipo_proyecto import TipoProyecto
        if not db.query(TipoProyecto).first():
            tipos_proyecto = [
                TipoProyecto(nombre="Tipo Proyecto 1", descripcion="Descripción del tipo proyecto 1"),
                TipoProyecto(nombre="Tipo Proyecto 2", descripcion="Descripción del tipo proyecto 2")
            ]
            db.add_all(tipos_proyecto)
            db.commit()
            print("Tipos de proyecto creados")

    finally:
        db.close()

if __name__ == "__main__":
    init_db()
