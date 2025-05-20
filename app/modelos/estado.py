from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Estado(Base):
    __tablename__ = 'estados'  
    

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    tipo = Column(String)
    

    # Relaciones
    usuarios = relationship("Usuario", back_populates="estado")
    proyectos = relationship("Proyecto", back_populates="estado")
    cronogramas = relationship("Cronograma", back_populates="estado")
    recursos = relationship("Recurso", back_populates="estado")
    participantes = relationship("Participante", back_populates="estado")
    avances = relationship("Avance", back_populates="estado")
    productos = relationship("Producto", back_populates="estado")
    tareas = relationship("Tarea", back_populates="estado")
    conceptos_evaluacion = relationship("ConceptoEvaluacion", back_populates="estado")
    anexos = relationship("Anexo", back_populates="estado")
    auditorias = relationship("Auditoria", back_populates="estado")

    cierres = relationship("Cierre", back_populates="estado")

    convocatorias = relationship("Convocatoria", back_populates="estado")

    destinos = relationship("Destino", back_populates="estado")

    evaluaciones = relationship("Evaluacion", back_populates="estado")

    extensiones = relationship("Extension", back_populates="estado")

    facultades = relationship("Facultad", back_populates="estado")

    lineas_investigacion = relationship("LineaInvestigacion", back_populates="estado")

    grupos_investigacion = relationship("GrupoInvestigacion", back_populates="estado")

    notificaciones = relationship("Notificacion", back_populates="estado")

    programas = relationship("Programa", back_populates="estado")

    impactos = relationship("Impacto", back_populates="estado")

    seguimientos = relationship("Seguimiento", back_populates="estado")

    tipos_proyecto = relationship('TipoProyecto', back_populates='estado')
    
