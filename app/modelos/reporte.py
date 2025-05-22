from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Reporte(Base):
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text)
    tipo_reporte = Column(String(50), nullable=False)  # 'diario', 'semanal', 'mensual', etc.
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    estado_id = Column(Integer, ForeignKey("estados.id"), default=1)
    tipo_estado_id = Column(Integer, ForeignKey("tipos_estado.id"), default=1)
    creado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    aprobado = Column(Boolean, default=False)
    fecha_aprobacion = Column(DateTime)
    aprobado_por_id = Column(Integer, ForeignKey("usuarios.id"))
    observaciones = Column(Text)
    archivo_url = Column(String(255))  # URL del archivo del reporte si se genera uno

    # Relaciones
    estado = relationship("Estado", foreign_keys=[estado_id])
    tipo_estado = relationship("TipoEstado", foreign_keys=[tipo_estado_id])
    creado_por = relationship("Usuario", foreign_keys=[creado_por_id])
    aprobado_por = relationship("Usuario", foreign_keys=[aprobado_por_id]) 