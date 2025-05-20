from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app import esquemas, modelos
from app.esquemas.usuario import Usuario, UsuarioCreate, UsuarioBase
from app.modelos.usuario import Usuario
from app.core.seguridad import get_password_hash, get_current_user
import os
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/usuarios/", response_model=List[esquemas.Usuario])
def leer_usuarios(
    skip: int = 0,
    limit: int = 100,
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    correo: Optional[str] = Query(None, description="Filtrar por correo"),
    rol_id: Optional[int] = Query(None, description="Filtrar por rol"),
    db: Session = Depends(get_db)
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

@router.get("/usuarios/{usuario_id}", response_model=esquemas.Usuario)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/usuarios/", response_model=esquemas.Usuario)
async def crear_usuario(
    nombre: str = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    contraseña: str = Form(...),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db)
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

@router.put("/usuarios/{usuario_id}", response_model=esquemas.Usuario)
def actualizar_usuario(usuario_id: int, usuario: esquemas.UsuarioCreate, db: Session = Depends(get_db)):
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
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/usuarios/{usuario_id}", response_model=esquemas.Usuario)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_usuario)
    db.commit()
    return db_usuario

@router.put("/usuarios/me", response_model=esquemas.Usuario)
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
    db.commit()
    db.refresh(current_user)
    return current_user
