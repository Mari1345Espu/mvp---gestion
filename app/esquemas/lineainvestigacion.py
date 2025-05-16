from pydantic import BaseModel

class LineaInvestigacionBase(BaseModel):
    nombre_linea: str
    descripcion: str
    estado_id: int
    tipo_estado_id: int

class LineaInvestigacionCreate(LineaInvestigacionBase):
    pass

class LineaInvestigacion(LineaInvestigacionBase):
    id: int

    class Config:
        from_attributes = True

