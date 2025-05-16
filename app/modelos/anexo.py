from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class Anexo(Base):
    __tablename__ = 'anexos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    ruta_archivo = Column(String)
    fecha_subida = Column(DateTime)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="anexos")
    estado = relationship("Estado", back_populates="anexos")
    tipo_estado = relationship("TipoEstado", back_populates="anexos")
