from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class ConceptoEvaluacion(Base):
    __tablename__ = 'conceptos_evaluacion'

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    evaluador_id = Column(Integer, ForeignKey('usuarios.id'))
    fecha_evaluacion = Column(DateTime)
    puntaje = Column(Float)
    observaciones = Column(Text)
    recomendaciones = Column(Text, nullable=True)
    aprobado = Column(Boolean, default=False)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))
    
    # Campos para criterios de evaluación
    criterio1_puntaje = Column(Float, nullable=True)
    criterio2_puntaje = Column(Float, nullable=True)
    criterio3_puntaje = Column(Float, nullable=True)
    criterio4_puntaje = Column(Float, nullable=True)
    criterio5_puntaje = Column(Float, nullable=True)

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="concepto_evaluacion")
    evaluador = relationship("Usuario", back_populates="conceptos_evaluacion")
    estado = relationship("Estado", back_populates="conceptos_evaluacion")
    tipo_estado = relationship("TipoEstado", back_populates="conceptos_evaluacion")
