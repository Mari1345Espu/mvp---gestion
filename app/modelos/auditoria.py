from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Auditoria(Base):
    __tablename__ = 'auditorias'

    id = Column(Integer, primary_key=True, index=True)
    accion = Column(String)
    tabla_afectada = Column(String)
    registro_id = Column(Integer)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    fecha_accion = Column(DateTime)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    usuario = relationship("Usuario", back_populates="auditorias")
    estado = relationship("Estado", back_populates="auditorias")
    tipo_estado = relationship("TipoEstado", back_populates="auditorias")
