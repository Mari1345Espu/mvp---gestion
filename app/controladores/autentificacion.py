from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.seguridad import create_access_token, verify_password, get_password_hash
from app import modelos, esquemas
from app.db.session import get_db

router = APIRouter()

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
