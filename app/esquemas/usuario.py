from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    correo: str
    nombre: constr(min_length=3, max_length=100)
    telefono: Optional[str] = None
    foto: Optional[str] = None
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1

class UsuarioCreate(UsuarioBase):
    contraseña: constr(min_length=6)
    rol_id: int

class UsuarioUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    telefono: Optional[str] = None
    foto: Optional[str] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    rol_id: Optional[int] = None

class UsuarioPasswordUpdate(BaseModel):
    contraseña_actual: str
    nueva_contraseña: constr(min_length=6)

class Usuario(UsuarioBase):
    id: int
    rol_id: int
    rol_nombre: Optional[str] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    reset_token: Optional[str] = None
    reset_token_expires: Optional[datetime] = None

    class Config:
        from_attributes = True

class UsuarioRegistro(BaseModel):
    nombre: constr(min_length=3, max_length=100)
    correo: str
    contraseña: constr(min_length=6)
    rol_id: int

class UsuarioLogin(BaseModel):
    correo: str
    contraseña: str

class UsuarioRecuperarContraseña(BaseModel):
    correo: str

class UsuarioResetearContraseña(BaseModel):
    token: str
    nueva_contraseña: constr(min_length=6)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str