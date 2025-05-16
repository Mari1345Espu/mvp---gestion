from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Destino(Base):
    __tablename__ = 'destinos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="destinos")
    estado = relationship("Estado", back_populates="destinos")
    tipo_estado = relationship("TipoEstado", back_populates="destinos")

