from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class TipoEstado(Base):
    __tablename__ = 'tipos_estado'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)

    # Relaciones
    usuarios = relationship("Usuario", back_populates="tipo_estado")
    proyectos = relationship("Proyecto", back_populates="tipo_estado")
    cronogramas = relationship("Cronograma", back_populates="tipo_estado")
    recursos = relationship("Recurso", back_populates="tipo_estado")
    participantes = relationship("Participante", back_populates="tipo_estado")
    avances = relationship("Avance", back_populates="tipo_estado")
    productos = relationship("Producto", back_populates="tipo_estado")
    tareas = relationship("Tarea", back_populates="tipo_estado")
    conceptos_evaluacion = relationship("ConceptoEvaluacion", back_populates="tipo_estado")
    anexos = relationship("Anexo", back_populates="tipo_estado")
    auditorias = relationship("Auditoria", back_populates="tipo_estado")
    cierres = relationship("Cierre", back_populates="tipo_estado")
    convocatorias = relationship("Convocatoria", back_populates="tipo_estado")
    destinos = relationship("Destino", back_populates="tipo_estado")
    evaluaciones = relationship("Evaluacion", back_populates="tipo_estado")
    extensiones = relationship("Extension", back_populates="tipo_estado")
    facultades = relationship("Facultad", back_populates="tipo_estado")
    lineas_investigacion = relationship("LineaInvestigacion", back_populates="tipo_estado")
    grupos_investigacion = relationship("GrupoInvestigacion", back_populates="tipo_estado")
    notificaciones = relationship("Notificacion", back_populates="tipo_estado")
    programas = relationship("Programa", back_populates="tipo_estado")
    impactos = relationship("Impacto", back_populates="tipo_estado")
    seguimientos = relationship("Seguimiento", back_populates="tipo_estado")
