from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Tarea(Base):
    __tablename__ = 'tareas'

    id = Column(Integer, primary_key=True, index=True)
    cronograma_id = Column(Integer, ForeignKey('cronogramas.id'))
    nombre = Column(String)
    descripcion = Column(Text)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))
    
    # Campos para aprobación y seguimiento
    aprobado = Column(Boolean, default=False)
    fecha_aprobacion = Column(DateTime, nullable=True)
    aprobado_por_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    observaciones = Column(Text, nullable=True)
    porcentaje_avance = Column(Float, default=0)
    fecha_ultimo_avance = Column(DateTime, nullable=True)
    responsable_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)

    # Relaciones
    cronograma = relationship("Cronograma", back_populates="tareas")
    estado = relationship("Estado", back_populates="tareas")
    tipo_estado = relationship("TipoEstado", back_populates="tareas")
    aprobado_por = relationship("Usuario", back_populates="tareas_aprobadas", foreign_keys=[aprobado_por_id])
    responsable = relationship("Usuario", back_populates="tareas_asignadas", foreign_keys=[responsable_id])
    avances = relationship("Avance", back_populates="tarea")
