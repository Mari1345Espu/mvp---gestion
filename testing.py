from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Definición de las tablas
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String)
    proyectos = relationship("Proyecto", back_populates="usuario")

class Rol(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    usuarios = relationship("Usuario", back_populates="rol")

class Proyecto(Base):
    __tablename__ = 'proyectos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="proyectos")

class Estado(Base):
    __tablename__ = 'estados'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyectos = relationship("Proyecto", back_populates="estado")

class TipoEstado(Base):
    __tablename__ = 'tipos_estado'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyectos = relationship("Proyecto", back_populates="tipo_estado")

class GrupoInvestigacion(Base):
    __tablename__ = 'grupos_investigacion'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyectos = relationship("Proyecto", back_populates="grupo_investigacion")

class LineaInvestigacion(Base):
    __tablename__ = 'lineas_investigacion'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyectos = relationship("Proyecto", back_populates="linea_investigacion")

class Convocatoria(Base):
    __tablename__ = 'convocatorias'
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    proyectos = relationship("Proyecto", back_populates="convocatoria")

class Anexo(Base):
    __tablename__ = 'anexos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    proyecto = relationship("Proyecto", back_populates="anexos")

class Autenticacion(Base):
    __tablename__ = 'autenticaciones'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="autenticaciones")

class Avance(Base):
    __tablename__ = 'avances'
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    fecha = Column(DateTime)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    proyecto = relationship("Proyecto", back_populates="avances")

class Cierre(Base):
    __tablename__ = 'cierres'
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    proyecto = relationship("Proyecto", back_populates="cierres")

class ConceptoEvaluacion(Base):
    __tablename__ = 'conceptos_evaluacion'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    evaluaciones = relationship("Evaluacion", back_populates="concepto_evaluacion")

class Destino(Base):
    __tablename__ = 'destinos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyectos = relationship("Proyecto", back_populates="destino")

class Evaluacion(Base):
    __tablename__ = 'evaluaciones'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    concepto_evaluacion_id = Column(Integer, ForeignKey('conceptos_evaluacion.id'))
    concepto_evaluacion = relationship("ConceptoEvaluacion", back_populates="evaluaciones")

class Extension(Base):
    __tablename__ = 'extensiones'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyectos = relationship("Proyecto", back_populates="extension")

class Facultad(Base):
    __tablename__ = 'facultades'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    programas = relationship("Programa", back_populates="facultad")

class Impacto(Base):
    __tablename__ = 'impactos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyectos = relationship("Proyecto", back_populates="impacto")

class Notificacion(Base):
    __tablename__ = 'notificaciones'
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    mensaje = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="notificaciones")

class Participante(Base):
    __tablename__ = 'participantes'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    proyecto = relationship("Proyecto", back_populates="participantes")

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    proyecto = relationship("Proyecto", back_populates="productos")

class Programa(Base):
    __tablename__ = 'programas'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    facultad_id = Column(Integer, ForeignKey('facultades.id'))
    facultad = relationship("Facultad", back_populates="programas")

class Recurso(Base):
    __tablename__ = 'recursos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    proyecto = relationship("Proyecto", back_populates="recursos")

class Seguimiento(Base):
    __tablename__ = 'seguimientos'
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    proyecto = relationship("Proyecto", back_populates="seguimientos")

class Tarea(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    proyecto = relationship("Proyecto", back_populates="tareas")

class TipoProyecto(Base):
    __tablename__ = 'tipos_proyecto'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    proyectos = relationship("Proyecto", back_populates="tipo_proyecto")

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Función para llenar la base de datos con datos de ejemplo
def populate_db():
    db = SessionLocal()

    # Crear usuarios de ejemplo
    usuario1 = Usuario(nombre="Usuario 1", email="usuario1@example.com")
    usuario2 = Usuario(nombre="Usuario 2", email="usuario2@example.com")

    # Crear roles de ejemplo
    rol1 = Rol(nombre="Administrador")
    rol2 = Rol(nombre="Usuario")

    # Crear estados de ejemplo
    estado1 = Estado(nombre="Activo")
    estado2 = Estado(nombre="Inactivo")

    # Crear tipos de estado de ejemplo
    tipo_estado1 = TipoEstado(nombre="Tipo 1")
    tipo_estado2 = TipoEstado(nombre="Tipo 2")

    # Crear grupos de investigación de ejemplo
    grupo_investigacion1 = GrupoInvestigacion(nombre="Grupo 1")
    grupo_investigacion2 = GrupoInvestigacion(nombre="Grupo 2")

    # Crear líneas de investigación de ejemplo
    linea_investigacion1 = LineaInvestigacion(nombre="Línea 1")
    linea_investigacion2 = LineaInvestigacion(nombre="Línea 2")

    # Crear convocatorias de ejemplo
    convocatoria1 = Convocatoria(tipo="Tipo 1", fecha_inicio=datetime.now(), fecha_fin=datetime.now())
    convocatoria2 = Convocatoria(tipo="Tipo 2", fecha_inicio=datetime.now(), fecha_fin=datetime.now())

    # Crear anexos de ejemplo
    anexo1 = Anexo(nombre="Anexo 1")
    anexo2 = Anexo(nombre="Anexo 2")

    # Crear autenticaciones de ejemplo
    autenticacion1 = Autenticacion(token="Token 1")
    autenticacion2 = Autenticacion(token="Token 2")

    # Crear avances de ejemplo
    avance1 = Avance(descripcion="Avance 1", fecha=datetime.now())
    avance2 = Avance(descripcion="Avance 2", fecha=datetime.now())

    # Crear cierres de ejemplo
    cierre1 = Cierre(fecha=datetime.now())
    cierre2 = Cierre(fecha=datetime.now())

    # Crear conceptos de evaluación de ejemplo
    concepto_evaluacion1 = ConceptoEvaluacion(nombre="Concepto 1")
    concepto_evaluacion2 = ConceptoEvaluacion(nombre="Concepto 2")

    # Crear destinos de ejemplo
    destino1 = Destino(nombre="Destino 1")
    destino2 = Destino(nombre="Destino 2")

    # Crear evaluaciones de ejemplo
    evaluacion1 = Evaluacion(nombre="Evaluación 1")
    evaluacion2 = Evaluacion(nombre="Evaluación 2")

    # Crear extensiones de ejemplo
    extension1 = Extension(nombre="Extensión 1")
    extension2 = Extension(nombre="Extensión 2")

    # Crear facultades de ejemplo
    facultad1 = Facultad(nombre="Facultad 1")
    facultad2 = Facultad(nombre="Facultad 2")

    # Crear impactos de ejemplo
    impacto1 = Impacto(nombre="Impacto 1")
    impacto2 = Impacto(nombre="Impacto 2")

    # Crear notificaciones de ejemplo
    notificacion1 = Notificacion(titulo="Notificación 1", mensaje="Mensaje 1")
    notificacion2 = Notificacion(titulo="Notificación 2", mensaje="Mensaje 2")

    # Crear participantes de ejemplo
    participante1 = Participante(nombre="Participante 1")
    participante2 = Participante(nombre="Participante 2")

    # Crear productos de ejemplo
    producto1 = Producto(nombre="Producto 1")
    producto2 = Producto(nombre="Producto 2")

    # Crear programas de ejemplo
    programa1 = Programa(nombre="Programa 1")
    programa2 = Programa(nombre="Programa 2")

    # Crear recursos de ejemplo
    recurso1 = Recurso(nombre="Recurso 1")
    recurso2 = Recurso(nombre="Recurso 2")

    # Crear seguimientos de ejemplo
    seguimiento1 = Seguimiento(fecha=datetime.now())
    seguimiento2 = Seguimiento(fecha=datetime.now())

    # Crear tareas de ejemplo
    tarea1 = Tarea(nombre="Tarea 1")
    tarea2 = Tarea(nombre="Tarea 2")

    # Crear tipos de proyecto de ejemplo
    tipo_proyecto1 = TipoProyecto(nombre="Tipo Proyecto 1")
    tipo_proyecto2 = TipoProyecto(nombre="Tipo Proyecto 2")

    # Crear proyectos de ejemplo
    proyecto1 = Proyecto(nombre="Proyecto 1", descripcion="Descripción del Proyecto 1", usuario=usuario1, estado=estado1, tipo_estado=tipo_estado1, grupo_investigacion=grupo_investigacion1, linea_investigacion=linea_investigacion1, convocatoria=convocatoria1, anexos=[anexo1], autenticaciones=[autenticacion1], avances=[avance1], cierres=[cierre1], concepto_evaluacion=concepto_evaluacion1, destino=destino1, evaluaciones=[evaluacion1], extension=extension1, impacto=impacto1, notificaciones=[notificacion1], participantes=[participante1], productos=[producto1], recursos=[recurso1], seguimientos=[seguimiento1], tareas=[tarea1], tipo_proyecto=tipo_proyecto1)
    proyecto2 = Proyecto(nombre="Proyecto 2", descripcion="Descripción del Proyecto 2", usuario=usuario2, estado=estado2, tipo_estado=tipo_estado2, grupo_investigacion=grupo_investigacion2, linea_investigacion=linea_investigacion2, convocatoria=convocatoria2, anexos=[anexo2], autenticaciones=[autenticacion2], avances=[avance2], cierres=[cierre2], concepto_evaluacion=concepto_evaluacion2, destino=destino2, evaluaciones=[evaluacion2], extension=extension2, impacto=impacto2, notificaciones=[notificacion2], participantes=[participante2], productos=[producto2], recursos=[recurso2], seguimientos=[seguimiento2], tareas=[tarea2], tipo_proyecto=tipo_proyecto2)

    # Añadir a la sesión y confirmar
    db.add_all([usuario1, usuario2, rol1, rol2, estado1, estado2, tipo_estado1, tipo_estado2, grupo_investigacion1, grupo_investigacion2, linea_investigacion1, linea_investigacion2, convocatoria1, convocatoria2, anexo1, anexo2, autenticacion1, autenticacion2, avance1, avance2, cierre1, cierre2, concepto_evaluacion1, concepto_evaluacion2, destino1, destino2, evaluacion1, evaluacion2, extension1, extension2, facultad1, facultad2, impacto1, impacto2, notificacion1, notificacion2, participante1, participante2, producto1, producto2, programa1, programa2, recurso1, recurso2, seguimiento1, seguimiento2, tarea1, tarea2, tipo_proyecto1, tipo_proyecto2, proyecto1, proyecto2])
    db.commit()
    db.close()

if __name__ == "__main__":
    populate_db()
    print("Base de datos configurada y poblada con datos de ejemplo.")
