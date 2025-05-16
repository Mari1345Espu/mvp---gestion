from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.seguimiento import SeguimientoBase, SeguimientoCreate, Seguimiento
from app.modelos.seguimiento import Seguimiento as SeguimientoModelo

router = APIRouter()

@router.get("/seguimientos/", response_model=List[esquemas.Seguimiento])
def leer_seguimientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    seguimientos = db.query(modelos.Seguimiento).offset(skip).limit(limit).all()
    return seguimientos

@router.get("/seguimientos/{seguimiento_id}", response_model=esquemas.Seguimiento)
def leer_seguimiento(seguimiento_id: int, db: Session = Depends(get_db)):
    seguimiento = db.query(modelos.Seguimiento).filter(modelos.Seguimiento.id == seguimiento_id).first()
    if seguimiento is None:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    return seguimiento

@router.post("/seguimientos/", response_model=esquemas.Seguimiento)
def crear_seguimiento(seguimiento: esquemas.SeguimientoCreate, db: Session = Depends(get_db)):
    db_seguimiento = modelos.Seguimiento(**seguimiento.dict())
    db.add(db_seguimiento)
    db.commit()
    db.refresh(db_seguimiento)
    return db_seguimiento

@router.put("/seguimientos/{seguimiento_id}", response_model=esquemas.Seguimiento)
def actualizar_seguimiento(seguimiento_id: int, seguimiento: esquemas.SeguimientoCreate, db: Session = Depends(get_db)):
    db_seguimiento = db.query(modelos.Seguimiento).filter(modelos.Seguimiento.id == seguimiento_id).first()
    if db_seguimiento is None:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    for key, value in seguimiento.dict().items():
        setattr(db_seguimiento, key, value)
    db.commit()
    db.refresh(db_seguimiento)
    return db_seguimiento

@router.delete("/seguimientos/{seguimiento_id}", response_model=esquemas.Seguimiento)
def eliminar_seguimiento(seguimiento_id: int, db: Session = Depends(get_db)):
    db_seguimiento = db.query(modelos.Seguimiento).filter(modelos.Seguimiento.id == seguimiento_id).first()
    if db_seguimiento is None:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    db.delete(db_seguimiento)
    db.commit()
    return db_seguimiento
