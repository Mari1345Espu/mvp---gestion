from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True, index=True)
    contraseña = Column(String)
    rol_id = Column(Integer, ForeignKey('roles.id'))
    telefono = Column(String)
    foto = Column(String)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))

    rol = relationship("Rol", back_populates="usuarios")
    estado = relationship("Estado", back_populates="usuarios")
    tipo_estado = relationship("TipoEstado", back_populates="usuarios")

    proyectos_evaluados = relationship("Proyecto", back_populates="evaluador_externo")
    auditorias = relationship("Auditoria", back_populates="usuario")

    grupos_liderados = relationship("GrupoInvestigacion", back_populates="lider")

    notificaciones = relationship("Notificacion", back_populates="usuario")
    #impactos = relationship("Impacto", back_populates="usuario")
