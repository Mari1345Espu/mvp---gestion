from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import secrets
import string
from jose import JWTError

from app.core.seguridad import (
    create_access_token, 
    verify_password, 
    get_password_hash,
    get_current_user
)
from app import modelos, esquemas
from app.db.session import get_db
from app.core.email import send_reset_password_email

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Configuración para OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token", response_model=esquemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Busca el usuario en la base de datos
    user = db.query(modelos.Usuario).filter(modelos.Usuario.correo == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos - usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos - contraseña inválida",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.rol:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario sin rol asignado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.estado or user.estado.nombre != "Activo":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear el token JWT
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.correo, "role": user.rol.nombre}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/recuperar-contraseña", response_class=HTMLResponse)
async def recuperar_contraseña_page(request: Request):
    return templates.TemplateResponse("recuperar_contraseña.html", {"request": request})

@router.post("/reset-password-request")
async def request_password_reset(email: str, db: Session = Depends(get_db)):
    user = db.query(modelos.Usuario).filter(modelos.Usuario.correo == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Generar token de reseteo
    reset_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    
    # Enviar email con el token
    await send_reset_password_email(email, reset_token)
    return {"message": "Se ha enviado un correo con instrucciones para restablecer la contraseña"}

@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str):
    return templates.TemplateResponse("cambiar_contraseña.html", {"request": request, "token": token})

@router.post("/reset-password")
async def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(modelos.Usuario).filter(
        modelos.Usuario.reset_token == token,
        modelos.Usuario.reset_token_expires > datetime.utcnow()
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )
    
    # Actualizar contraseña
    user.contraseña = get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente"}

@router.post("/logout")
async def logout(current_user: modelos.Usuario = Depends(get_current_user)):
    # En una implementación real, podrías invalidar el token JWT
    # o mantener una lista negra de tokens
    return {"message": "Sesión cerrada exitosamente"}
