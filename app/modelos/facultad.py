from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Facultad(Base):
    __tablename__ = 'facultades'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    programas = relationship("Programa", back_populates="facultad")
    participantes = relationship("Participante", back_populates="facultad")
    estado = relationship("Estado", back_populates="facultades")
    tipo_estado = relationship("TipoEstado", back_populates="facultades")

