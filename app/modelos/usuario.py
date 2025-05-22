from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    contraseña = Column(String)
    rol_id = Column(Integer, ForeignKey('roles.id'))
    telefono = Column(String)
    foto = Column(String, nullable=True)
    estado_id = Column(Integer, ForeignKey('estados.id'), nullable=True)
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'), nullable=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    rol = relationship("Rol", back_populates="usuarios")
    estado = relationship("Estado", back_populates="usuarios")
    tipo_estado = relationship("TipoEstado", back_populates="usuarios")

    # Relaciones con proyectos
    proyectos_evaluados = relationship("Proyecto", back_populates="evaluador_externo")
    proyectos_asesorados = relationship("Proyecto", back_populates="asesor", foreign_keys="[Proyecto.asesor_id]")
    productos_aprobados = relationship("Producto", back_populates="aprobado_por")
    
    # Relaciones con grupos y auditoría
    auditorias = relationship("Auditoria", back_populates="usuario")
    grupos_liderados = relationship("GrupoInvestigacion", back_populates="lider")
    
    # Relaciones con notificaciones y evaluaciones
    notificaciones = relationship("Notificacion", back_populates="usuario")
    conceptos_evaluacion = relationship("ConceptoEvaluacion", back_populates="evaluador")
    
    # Relaciones con avances y recursos
    avances_aprobados = relationship("Avance", back_populates="aprobado_por")
    recursos_aprobados = relationship("Recurso", back_populates="aprobado_por")
    
    # Relaciones con tareas
    tareas_aprobadas = relationship("Tarea", back_populates="aprobado_por", foreign_keys="[Tarea.aprobado_por_id]")
    tareas_asignadas = relationship("Tarea", back_populates="responsable", foreign_keys="[Tarea.responsable_id]")
