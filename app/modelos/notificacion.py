from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Notificacion(Base):
    __tablename__ = 'notificaciones'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    mensaje = Column(String)
    fecha_envio = Column(DateTime)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    # Relaciones
    usuario = relationship("Usuario", back_populates="notificaciones")
    estado = relationship("Estado", back_populates="notificaciones")
    tipo_estado = relationship("TipoEstado", back_populates="notificaciones")

