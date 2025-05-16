from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Tarea(Base):
    __tablename__ = 'tareas'

    id = Column(Integer, primary_key=True, index=True)
    cronograma_id = Column(Integer, ForeignKey('cronogramas.id'))
    nombre = Column(String)
    descripcion = Column(Text)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    cronograma = relationship("Cronograma", back_populates="tareas")
    estado = relationship("Estado", back_populates="tareas")
    tipo_estado = relationship("TipoEstado", back_populates="tareas")
