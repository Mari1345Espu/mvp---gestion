from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db
from app.esquemas.rol import Rol, RolCreate, RolBase
from app.modelos.rol import Rol

router = APIRouter()

@router.get("/roles/", response_model=List[esquemas.Rol])
def leer_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = db.query(modelos.Rol).offset(skip).limit(limit).all()
    return roles

@router.get("/roles/{rol_id}", response_model=esquemas.Rol)
def leer_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(modelos.Rol).filter(modelos.Rol.id == rol_id).first()
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.post("/roles/", response_model=esquemas.Rol)
def crear_rol(rol: esquemas.RolCreate, db: Session = Depends(get_db)):
    db_rol = modelos.Rol(nombre=rol.nombre)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

@router.put("/roles/{rol_id}", response_model=esquemas.Rol)
def actualizar_rol(rol_id: int, rol: esquemas.RolCreate, db: Session = Depends(get_db)):
    db_rol = db.query(modelos.Rol).filter(modelos.Rol.id == rol_id).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db_rol.nombre = rol.nombre
    db.commit()
    db.refresh(db_rol)
    return db_rol

@router.delete("/roles/{rol_id}", response_model=esquemas.Rol)
def eliminar_rol(rol_id: int, db: Session = Depends(get_db)):
    db_rol = db.query(modelos.Rol).filter(modelos.Rol.id == rol_id).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.delete(db_rol)
    db.commit()
    return db_rol
