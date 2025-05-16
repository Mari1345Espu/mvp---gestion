from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class LineaInvestigacion(Base):
    __tablename__ = 'lineas_investigacion'

    id = Column(Integer, primary_key=True, index=True)
    nombre_linea = Column(String)
    descripcion = Column(Text)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyectos = relationship("Proyecto", back_populates="linea_investigacion")
    estado = relationship("Estado", back_populates="lineas_investigacion")
    tipo_estado = relationship("TipoEstado", back_populates="lineas_investigacion")
