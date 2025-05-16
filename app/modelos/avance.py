from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Avance(Base):
    __tablename__ = 'avances'

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    fecha_avance = Column(DateTime)
    descripcion = Column(Text)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="avances")
    estado = relationship("Estado", back_populates="avances")
    tipo_estado = relationship("TipoEstado", back_populates="avances")
