from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    nombre = Column(String)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime)
    estado_id = Column(Integer, ForeignKey('estados.id'))
    tipo_estado_id = Column(Integer, ForeignKey('tipos_estado.id'))
    
    # Campos para publicación y aprobación
    publicado = Column(Boolean, default=False)
    fecha_publicacion = Column(DateTime, nullable=True)
    destino = Column(String, nullable=True)
    evidencias = Column(Text, nullable=True)
    aprobado = Column(Boolean, default=False)
    fecha_aprobacion = Column(DateTime, nullable=True)
    observaciones = Column(Text, nullable=True)
    aprobado_por_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="productos")
    estado = relationship("Estado", back_populates="productos")
    tipo_estado = relationship("TipoEstado", back_populates="productos")
    aprobado_por = relationship("Usuario", back_populates="productos_aprobados")
