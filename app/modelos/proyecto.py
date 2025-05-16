from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.modelos.cierre import Cierre
from app.db.base import Base

class Proyecto(Base):
    __tablename__ = 'proyectos'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    objetivos = Column(String)
    convocatoria_id = Column(Integer, ForeignKey('convocatorias.id'))
    grupo_investigacion_id = Column(Integer, ForeignKey('grupos_investigacion.id'))
    linea_investigacion_id = Column(Integer, ForeignKey('lineas_investigacion.id'))
    extension_id = Column(Integer, ForeignKey('extensiones.id'))
    estado_id = Column(Integer, ForeignKey('estados.id'))
    fecha_inicio = Column(Date)
    resumen = Column(String)
    evaluador_externo_id = Column(Integer, ForeignKey('usuarios.id'))
    concepto_evaluacion_id = Column(Integer, ForeignKey('conceptos_evaluacion.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))
    problematica = Column(String)
#    tipo_proyecto_id = Column(Integer, ForeignKey('tipos_proyecto.id'))

    # Relaciones
    convocatoria = relationship("Convocatoria", back_populates="proyectos")
    grupo_investigacion = relationship("GrupoInvestigacion", back_populates="proyectos")
    linea_investigacion = relationship("LineaInvestigacion", back_populates="proyectos")
    extension = relationship("Extension", back_populates="proyectos")
    estado = relationship("Estado", back_populates="proyectos")
    tipo_estado = relationship("TipoEstado", back_populates="proyectos")
    #tipo_proyecto = relationship("TipoProyecto", back_populates="proyectos")
    evaluador_externo = relationship("Usuario", back_populates="proyectos_evaluados")
    concepto_evaluacion = relationship("ConceptoEvaluacion", back_populates="proyectos")

    cronogramas = relationship("Cronograma", back_populates="proyecto")
    anexos = relationship("Anexo", back_populates="proyecto")
    avances = relationship("Avance", back_populates="proyecto")

    cierre = relationship("Cierre", back_populates="proyecto", uselist=False)

    destinos = relationship("Destino", back_populates="proyecto")

    evaluaciones = relationship("Evaluacion", back_populates="proyecto")

    recursos = relationship("Recurso", back_populates="proyecto")

    participantes = relationship("Participante", back_populates="proyecto")

    productos = relationship("Producto", back_populates="proyecto")

    impactos = relationship("Impacto", back_populates="proyecto")

#    seguimientos = relationship("Seguimiento", back_populates="proyecto")
