from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class TipoProyecto(Base):
    __tablename__ = 'tipos_proyecto'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    estado_id = Column(Integer, ForeignKey('estados.id'), nullable=True)
    estado = relationship('Estado', back_populates='tipos_proyecto')
    descripcion = Column(String)

    # Relaciones
    proyectos = relationship("Proyecto", back_populates="tipo_proyecto")
