from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Form, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app import esquemas, modelos
from app.esquemas.usuario import Usuario as UsuarioSchema, UsuarioCreate, UsuarioBase
from app.core.seguridad import get_password_hash, get_current_user
import os
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import secrets
from sqlalchemy import or_

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

@router.get("/", response_model=List[UsuarioSchema])
def leer_usuarios(
    skip: int = 0,
    limit: int = 100,
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    correo: Optional[str] = Query(None, description="Filtrar por correo"),
    rol_id: Optional[int] = Query(None, description="Filtrar por rol"),
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    query = db.query(modelos.Usuario)
    if nombre:
        query = query.filter(modelos.Usuario.nombre.ilike(f"%{nombre}%"))
    if correo:
        query = query.filter(modelos.Usuario.correo.ilike(f"%{correo}%"))
    if rol_id:
        query = query.filter(modelos.Usuario.rol_id == rol_id)
    usuarios = query.offset(skip).limit(limit).all()
    return usuarios

@router.get("/{usuario_id}", response_model=UsuarioSchema)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db), current_user: modelos.Usuario = Depends(get_current_user)):
    usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioSchema)
async def crear_usuario(
    nombre: str = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    contraseña: str = Form(...),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    # Verificar si el correo ya existe
    usuario_existente = db.query(modelos.Usuario).filter(modelos.Usuario.correo == correo).first()
    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya está registrado"
        )

    # Buscar el rol de 'Investigador'
    rol_investigador = db.query(modelos.Rol).filter(modelos.Rol.nombre == "Investigador").first()
    if not rol_investigador:
        raise HTTPException(status_code=400, detail="No existe el rol 'Investigador'")
    
    hashed_password = get_password_hash(contraseña)
    foto_url = None
    if foto:
        uploads_dir = os.path.join("app", "static", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        file_ext = os.path.splitext(foto.filename)[1]
        file_name = f"{correo.replace('@','_')}{file_ext}"
        file_path = os.path.join(uploads_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(await foto.read())
        foto_url = f"/static/uploads/{file_name}"
    
    db_usuario = modelos.Usuario(
        correo=correo,
        nombre=nombre,
        contraseña=hashed_password,
        telefono=telefono,
        foto=foto_url,
        rol_id=rol_investigador.id
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.put("/{usuario_id}", response_model=UsuarioSchema)
def actualizar_usuario(usuario_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db), current_user: modelos.Usuario = Depends(get_current_user)):
    db_usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_usuario.correo = usuario.correo
    db_usuario.nombre = usuario.nombre
    db_usuario.contraseña = get_password_hash(usuario.contraseña)
    db_usuario.telefono = usuario.telefono
    db_usuario.foto = usuario.foto
    db_usuario.rol_id = getattr(usuario, 'rol_id', db_usuario.rol_id)
    db_usuario.estado_id = getattr(usuario, 'estado_id', db_usuario.estado_id)
    db_usuario.tipo_estado_id = getattr(usuario, 'tipo_estado_id', db_usuario.tipo_estado_id)
    db_usuario.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/{usuario_id}", response_model=UsuarioSchema)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db), current_user: modelos.Usuario = Depends(get_current_user)):
    db_usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_usuario)
    db.commit()
    return db_usuario

@router.put("/me", response_model=UsuarioSchema)
async def actualizar_mi_perfil(
    nombre: str = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="No autenticado")
    current_user.nombre = nombre
    current_user.correo = correo
    current_user.telefono = telefono
    if foto:
        uploads_dir = os.path.join("app", "static", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        file_ext = os.path.splitext(foto.filename)[1]
        file_name = f"{correo.replace('@','_')}{file_ext}"
        file_path = os.path.join(uploads_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(await foto.read())
        current_user.foto = f"/static/uploads/{file_name}"
    current_user.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me", response_model=UsuarioSchema)
async def get_current_user_info(
    current_user: modelos.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene la información del usuario actual
    """
    try:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No autenticado"
            )

        # Asegurarse de que el usuario tenga un rol asignado
        if not current_user.rol:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario sin rol asignado"
            )

        # Asegurarse de que todos los campos requeridos estén presentes
        if not current_user.telefono:
            current_user.telefono = ""
        if not current_user.foto:
            current_user.foto = ""
        if not current_user.estado_id:
            current_user.estado_id = 1  # Estado por defecto: Activo
        if not current_user.tipo_estado_id:
            current_user.tipo_estado_id = 1  # Tipo de estado por defecto

        # Asegurarse de que el rol_nombre esté presente
        if not current_user.rol_nombre and current_user.rol:
            current_user.rol_nombre = current_user.rol.nombre

        return current_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/registro", response_model=UsuarioSchema)
def registro_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    db_usuario = db.query(modelos.Usuario).filter(modelos.Usuario.correo == usuario.correo).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    hashed_password = get_password_hash(usuario.contraseña)
    db_usuario = modelos.Usuario(
        **usuario.dict(exclude={'contraseña'}),
        contraseña=hashed_password
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.post("/login")
def login_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    db_usuario = db.query(modelos.Usuario).filter(modelos.Usuario.correo == usuario.correo).first()
    if not db_usuario or not verify_password(usuario.contraseña, db_usuario.contraseña):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    access_token = create_access_token(data={"sub": usuario.correo})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/recuperar-contraseña")
def recuperar_contraseña(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    db_usuario = db.query(modelos.Usuario).filter(modelos.Usuario.correo == usuario.correo).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Generar token de recuperación
    reset_token = secrets.token_urlsafe(32)
    db_usuario.reset_token = reset_token
    db_usuario.reset_token_expires = datetime.utcnow() + timedelta(hours=24)
    db.commit()
    
    # Aquí deberías implementar el envío del correo con el token
    return {"message": "Se ha enviado un correo con las instrucciones para recuperar la contraseña"}

@router.post("/resetear-contraseña")
def resetear_contraseña(
    reset_data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    db_usuario = db.query(modelos.Usuario).filter(
        and_(
            modelos.Usuario.reset_token == reset_data.token,
            modelos.Usuario.reset_token_expires > datetime.utcnow()
        )
    ).first()
    
    if not db_usuario:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    
    hashed_password = get_password_hash(reset_data.nueva_contraseña)
    db_usuario.contraseña = hashed_password
    db_usuario.reset_token = None
    db_usuario.reset_token_expires = None
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente"}

@router.put("/{usuario_id}/cambiar-contraseña", response_model=UsuarioSchema)
def cambiar_contraseña(
    usuario_id: int,
    password_data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.id != usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para realizar esta acción")
    
    if not verify_password(password_data.contraseña_actual, current_user.contraseña):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    
    current_user.contraseña = get_password_hash(password_data.nueva_contraseña)
    current_user.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/buscar/{termino}", response_model=List[UsuarioSchema])
def buscar_usuarios(
    termino: str,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    usuarios = db.query(modelos.Usuario).filter(
        or_(
            modelos.Usuario.nombre.ilike(f"%{termino}%"),
            modelos.Usuario.correo.ilike(f"%{termino}%")
        )
    ).all()
    return usuarios

@router.get("/rol/{rol_id}", response_model=List[UsuarioSchema])
def read_usuarios_by_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    usuarios = db.query(modelos.Usuario).filter(modelos.Usuario.rol_id == rol_id).all()
    return usuarios
