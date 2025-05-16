from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.tipo_estado import TipoEstadoBase, TipoEstadoCreate, TipoEstado
from app.esquemas.tipo_estado import TipoEstado as TipoEstadoModelo

router = APIRouter()

@router.get("/tipos_estado/", response_model=List[esquemas.TipoEstado])
def leer_tipos_estado(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tipos_estado = db.query(modelos.TipoEstado).offset(skip).limit(limit).all()
    return tipos_estado

@router.get("/tipos_estado/{tipo_estado_id}", response_model=esquemas.TipoEstado)
def leer_tipo_estado(tipo_estado_id: int, db: Session = Depends(get_db)):
    tipo_estado = db.query(modelos.TipoEstado).filter(modelos.TipoEstado.id == tipo_estado_id).first()
    if tipo_estado is None:
        raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")
    return tipo_estado

@router.post("/tipos_estado/", response_model=esquemas.TipoEstado)
def crear_tipo_estado(tipo_estado: esquemas.TipoEstadoCreate, db: Session = Depends(get_db)):
    db_tipo_estado = modelos.TipoEstado(nombre=tipo_estado.nombre)
    db.add(db_tipo_estado)
    db.commit()
    db.refresh(db_tipo_estado)
    return db_tipo_estado

@router.put("/tipos_estado/{tipo_estado_id}", response_model=esquemas.TipoEstado)
def actualizar_tipo_estado(tipo_estado_id: int, tipo_estado: esquemas.TipoEstadoCreate, db: Session = Depends(get_db)):
    db_tipo_estado = db.query(modelos.TipoEstado).filter(modelos.TipoEstado.id == tipo_estado_id).first()
    if db_tipo_estado is None:
        raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")
    db_tipo_estado.nombre = tipo_estado.nombre
    db.commit()
    db.refresh(db_tipo_estado)
    return db_tipo_estado

@router.delete("/tipos_estado/{tipo_estado_id}", response_model=esquemas.TipoEstado)
def eliminar_tipo_estado(tipo_estado_id: int, db: Session = Depends(get_db)):
    db_tipo_estado = db.query(modelos.TipoEstado).filter(modelos.TipoEstado.id == tipo_estado_id).first()
    if db_tipo_estado is None:
        raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")
    db.delete(db_tipo_estado)
    db.commit()
    return db_tipo_estado
