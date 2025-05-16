from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Extension(Base):
    __tablename__ = 'extensiones'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(Text)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyectos = relationship("Proyecto", back_populates="extension")
    estado = relationship("Estado", back_populates="extensiones")
    tipo_estado = relationship("TipoEstado", back_populates="extensiones")
