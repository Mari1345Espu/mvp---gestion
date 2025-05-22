from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from ..dependencias import get_db
from ..modelos import Usuario
from ..utilidades.auth import verify_token
from ..esquemas.usuario import Usuario as UsuarioSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UsuarioSchema:
    """
    Obtiene el usuario actual basado en el token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
        
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None:
        raise credentials_exception
        
    return UsuarioSchema.from_orm(user)

async def get_current_active_user(
    current_user: UsuarioSchema = Depends(get_current_user)
) -> UsuarioSchema:
    """
    Verifica que el usuario actual esté activo.
    """
    if current_user.estado_id != 1:  # 1 = Activo
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user

async def get_admin_user(
    current_user: UsuarioSchema = Depends(get_current_active_user)
) -> UsuarioSchema:
    """
    Verifica que el usuario actual sea administrador.
    """
    if current_user.rol_id != 1:  # 1 = Admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de administrador"
        )
    return current_user

def verify_user_permission(
    current_user: UsuarioSchema,
    target_user_id: int
) -> bool:
    """
    Verifica si el usuario actual tiene permiso para acceder a los datos del usuario objetivo.
    """
    return current_user.id == target_user_id or current_user.rol_id == 1  # Admin puede acceder a todo 