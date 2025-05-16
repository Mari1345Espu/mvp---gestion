from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.estado import EstadoBase, EstadoCreate, Estado
from app.modelos.estado import Estado as EstadoModelo

router = APIRouter()

@router.get("/estados/", response_model=List[esquemas.Estado])
def leer_estados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    estados = db.query(modelos.Estado).offset(skip).limit(limit).all()
    return estados

@router.get("/estados/{estado_id}", response_model=esquemas.Estado)
def leer_estado(estado_id: int, db: Session = Depends(get_db)):
    estado = db.query(modelos.Estado).filter(modelos.Estado.id == estado_id).first()
    if estado is None:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado

@router.post("/estados/", response_model=esquemas.Estado)
def crear_estado(estado: esquemas.EstadoCreate, db: Session = Depends(get_db)):
    db_estado = modelos.Estado(nombre=estado.nombre, tipo=estado.tipo)  # Incluido el campo tipo
    db.add(db_estado)
    db.commit()
    db.refresh(db_estado)
    return db_estado

@router.put("/estados/{estado_id}", response_model=esquemas.Estado)
def actualizar_estado(estado_id: int, estado: esquemas.EstadoCreate, db: Session = Depends(get_db)):
    db_estado = db.query(modelos.Estado).filter(modelos.Estado.id == estado_id).first()
    if db_estado is None:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    db_estado.nombre = estado.nombre
    db_estado.tipo = estado.tipo  # Actualizado el campo tipo
    db.commit()
    db.refresh(db_estado)
    return db_estado

@router.delete("/estados/{estado_id}", response_model=esquemas.Estado)
def eliminar_estado(estado_id: int, db: Session = Depends(get_db)):
    db_estado = db.query(modelos.Estado).filter(modelos.Estado.id == estado_id).first()
    if db_estado is None:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    db.delete(db_estado)
    db.commit()
    return db_estado
