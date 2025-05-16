from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class Participante(Base):
    __tablename__ = 'participantes'

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    fecha_vinculacion = Column(DateTime)
    nombre = Column(String)
    rol_id = Column(Integer, ForeignKey('roles.id'))
    facultad_id = Column(Integer, ForeignKey('facultades.id'))
    programa_id = Column(Integer, ForeignKey('programas.id'))
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="participantes")
    rol = relationship("Rol", back_populates="participantes")
    facultad = relationship("Facultad", back_populates="participantes")
    programa = relationship("Programa", back_populates="participantes")
    estado = relationship("Estado", back_populates="participantes")
    tipo_estado = relationship("TipoEstado", back_populates="participantes")
