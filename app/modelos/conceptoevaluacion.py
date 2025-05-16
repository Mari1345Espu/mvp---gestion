from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ConceptoEvaluacion(Base):
    __tablename__ = 'conceptos_evaluacion'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(Text)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyectos = relationship("Proyecto", back_populates="concepto_evaluacion")
    estado = relationship("Estado", back_populates="conceptos_evaluacion")
    tipo_estado = relationship("TipoEstado", back_populates="conceptos_evaluacion")
