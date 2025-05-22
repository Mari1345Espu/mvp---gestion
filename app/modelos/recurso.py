from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Recurso(Base):
    __tablename__ = 'recursos'

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    nombre = Column(String)
    descripcion = Column(Text)
    cantidad = Column(Float)
    unidad = Column(String)
    valor_unitario = Column(Float)
    fecha_solicitud = Column(DateTime)
    fecha_respuesta = Column(DateTime)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))
    aprobado = Column(Boolean, default=False)
    fecha_aprobacion = Column(DateTime, nullable=True)
    observaciones = Column(Text, nullable=True)
    aprobado_por_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    justificacion = Column(Text, nullable=True)

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="recursos")
    estado = relationship("Estado", back_populates="recursos")
    tipo_estado = relationship("TipoEstado", back_populates="recursos")
    aprobado_por = relationship("Usuario", back_populates="recursos_aprobados")
