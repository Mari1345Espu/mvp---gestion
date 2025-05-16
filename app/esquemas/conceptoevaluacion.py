from pydantic import BaseModel

class ConceptoEvaluacionBase(BaseModel):
    nombre: str
    descripcion: str
    estado_id: int
    tipo_estado_id: int

class ConceptoEvaluacionCreate(ConceptoEvaluacionBase):
    pass

class ConceptoEvaluacion(ConceptoEvaluacionBase):
    id: int

    class Config:
        orm_mode = True
