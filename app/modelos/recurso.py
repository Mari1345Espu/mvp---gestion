from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Recurso(Base):
    __tablename__ = 'recursos'

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    descripcion = Column(Text)
    cantidad = Column(Integer)
    fecha_solicitud = Column(DateTime)
    fecha_respuesta = Column(DateTime)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="recursos")
    estado = relationship("Estado", back_populates="recursos")
    tipo_estado = relationship("TipoEstado", back_populates="recursos")
