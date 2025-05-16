from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Cierre(Base):
    __tablename__ = 'cierres'

    id = Column(Integer, primary_key=True, index=True)
    fecha_cierre = Column(DateTime)
    observaciones = Column(String)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="cierre", foreign_keys=[proyecto_id])
    estado = relationship("Estado", back_populates="cierres")
    tipo_estado = relationship("TipoEstado", back_populates="cierres")
