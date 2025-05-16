from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Convocatoria(Base):
    __tablename__ = 'convocatorias'

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    fecha_inicio_ejecucion = Column(DateTime)
    fecha_fin_ejecucion = Column(DateTime)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyectos = relationship("Proyecto", back_populates="convocatoria")
    estado = relationship("Estado", back_populates="convocatorias")
    tipo_estado = relationship("TipoEstado", back_populates="convocatorias")
