from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class TipoProyecto(Base):
    __tablename__ = 'tipos_proyecto'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)

    # Relaciones
    proyectos = relationship("Proyecto", back_populates="tipo_proyecto")
