from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Evaluacion(Base):
    __tablename__ = 'evaluaciones'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    fecha_evaluacion = Column(DateTime)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="evaluaciones")
    estado = relationship("Estado", back_populates="evaluaciones")
    tipo_estado = relationship("TipoEstado", back_populates="evaluaciones")
