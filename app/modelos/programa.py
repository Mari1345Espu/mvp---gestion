from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Programa(Base):
    __tablename__ = 'programas'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    facultad_id = Column(Integer, ForeignKey('facultades.id'))
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    facultad = relationship("Facultad", back_populates="programas")
    participantes = relationship("Participante", back_populates="programa")
    estado = relationship("Estado", back_populates="programas")
    tipo_estado = relationship("TipoEstado", back_populates="programas")

