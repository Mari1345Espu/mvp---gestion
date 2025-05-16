from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Seguimiento(Base):
    __tablename__ = 'seguimientos'

    id = Column(Integer, primary_key=True, index=True)
    fecha_seguimiento = Column(DateTime)
    observaciones = Column(String)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="seguimientos")
    estado = relationship("Estado", back_populates="seguimientos")
    tipo_estado = relationship("TipoEstado", back_populates="seguimientos")
