from pydantic import BaseModel

class UsuarioBase(BaseModel):
    correo: str
    nombre: str
    telefono: str
    foto: str

class UsuarioCreate(UsuarioBase):
    contraseña: str

class Usuario(UsuarioBase):
    id: int
    rol_id: int
    estado_id: int
    tipo_estado_id: int
    rol_nombre: str | None = None

    class Config:
        orm_mode = True
