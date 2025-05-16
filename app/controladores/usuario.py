from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app import esquemas, modelos
from app.esquemas.usuario import Usuario, UsuarioCreate, UsuarioBase
from app.modelos.usuario import Usuario
from app.core.seguridad import get_password_hash

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
def crear_usuario(usuario: esquemas.UsuarioCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(usuario.contraseña)
    db_usuario = modelos.Usuario(
        correo=usuario.correo,
        nombre=usuario.nombre,
        contraseña=hashed_password,
        telefono=usuario.telefono,
        foto=usuario.foto,
        rol_id=getattr(usuario, 'rol_id', None),
        estado_id=getattr(usuario, 'estado_id', None),
        tipo_estado_id=getattr(usuario, 'tipo_estado_id', None)
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
