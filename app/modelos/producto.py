from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    nombre = Column(String)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="productos")
    estado = relationship("Estado", back_populates="productos")
    tipo_estado = relationship("TipoEstado", back_populates="productos")
