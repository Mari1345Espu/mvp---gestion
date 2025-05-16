from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class Cronograma(Base):
    __tablename__ = 'cronogramas'

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    fecha_creacion = Column(DateTime)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="cronogramas")
    estado = relationship("Estado", back_populates="cronogramas")
    tipo_estado = relationship("TipoEstado", back_populates="cronogramas")
    tareas = relationship("Tarea", back_populates="cronograma")
