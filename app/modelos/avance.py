from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Avance(Base):
    __tablename__ = 'avances'

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    tarea_id = Column(Integer, ForeignKey('tareas.id'), nullable=True)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))
    aprobado = Column(Boolean, default=False)
    fecha_aprobacion = Column(DateTime, nullable=True)
    observaciones = Column(Text, nullable=True)
    aprobado_por_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    evidencias = Column(Text, nullable=True)
    porcentaje_completado = Column(Float, default=0)

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="avances")
    tarea = relationship("Tarea", back_populates="avances")
    estado = relationship("Estado", back_populates="avances")
    tipo_estado = relationship("TipoEstado", back_populates="avances")
    aprobado_por = relationship("Usuario", back_populates="avances_aprobados")
