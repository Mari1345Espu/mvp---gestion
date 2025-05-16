from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class GrupoInvestigacion(Base):
    __tablename__ = 'grupos_investigacion'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime)
    lider_id = Column(Integer, ForeignKey('usuarios.id'))
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))
    categoria = Column(String)
    categoria_minciencias = Column(String)

    # Relaciones
    proyectos = relationship("Proyecto", back_populates="grupo_investigacion")
    lider = relationship("Usuario", back_populates="grupos_liderados")
    estado = relationship("Estado", back_populates="grupos_investigacion")
    tipo_estado = relationship("TipoEstado", back_populates="grupos_investigacion")
