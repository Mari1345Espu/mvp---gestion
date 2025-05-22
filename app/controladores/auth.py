from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
import string

from ..dependencias import get_db
from ..dependencias.auth import get_current_user
from ..modelos import Usuario
from ..esquemas.usuario import (
    Usuario as UsuarioSchema,
    UsuarioLogin,
    UsuarioRecuperarContraseña,
    UsuarioResetearContraseña,
    TokenResponse
)
from ..utilidades.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token
)

router = APIRouter(
    prefix="/auth",
    tags=["autenticación"]
)

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Inicia sesión y devuelve tokens de acceso y refresco.
    """
    user = db.query(Usuario).filter(Usuario.correo == form_data.username).first()
    if not user or not verify_password(form_data.password, user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.estado_id != 1:  # 1 = Activo
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    # Crear tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresca el token de acceso usando el token de refresco.
    """
    try:
        payload = verify_token(refresh_token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de refresco inválido"
            )

        user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado"
            )

        # Crear nuevo token de acceso
        access_token = create_access_token(data={"sub": str(user.id)})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de refresco inválido"
        )

@router.post("/recuperar-contraseña")
async def recuperar_contraseña(
    data: UsuarioRecuperarContraseña,
    db: Session = Depends(get_db)
):
    """
    Inicia el proceso de recuperación de contraseña.
    """
    user = db.query(Usuario).filter(Usuario.correo == data.correo).first()
    if not user:
        # Por seguridad, no revelamos si el correo existe o no
        return {"message": "Si el correo existe, se enviarán instrucciones"}

    # Generar token de recuperación
    token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    user.reset_token = token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=24)
    db.commit()

    # TODO: Enviar correo con el token
    # Por ahora solo devolvemos el token (en producción esto debe enviarse por correo)
    return {"message": "Se han enviado instrucciones al correo electrónico"}

@router.post("/resetear-contraseña")
async def resetear_contraseña(
    data: UsuarioResetearContraseña,
    db: Session = Depends(get_db)
):
    """
    Resetea la contraseña usando el token de recuperación.
    """
    user = db.query(Usuario).filter(Usuario.reset_token == data.token).first()
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )

    # Actualizar contraseña
    user.contraseña = get_password_hash(data.nueva_contraseña)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()

    return {"message": "Contraseña actualizada exitosamente"}

@router.post("/logout")
async def logout(
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Cierra la sesión del usuario.
    En una implementación real, podrías invalidar el token actual.
    """
    return {"message": "Sesión cerrada exitosamente"}