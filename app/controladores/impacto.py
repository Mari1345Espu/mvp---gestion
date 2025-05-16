from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.impacto import ImpactoBase, ImpactoCreate, Impacto
from app.modelos.impacto import Impacto as ImpactoModelo

router = APIRouter()

@router.get("/impactos/", response_model=List[esquemas.Impacto])
def leer_impactos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    impactos = db.query(modelos.Impacto).offset(skip).limit(limit).all()
    return impactos

@router.get("/impactos/{impacto_id}", response_model=esquemas.Impacto)
def leer_impacto(impacto_id: int, db: Session = Depends(get_db)):
    impacto = db.query(modelos.Impacto).filter(modelos.Impacto.id == impacto_id).first()
    if impacto is None:
        raise HTTPException(status_code=404, detail="Impacto no encontrado")
    return impacto

@router.post("/impactos/", response_model=esquemas.Impacto)
def crear_impacto(impacto: esquemas.ImpactoCreate, db: Session = Depends(get_db)):
    db_impacto = modelos.Impacto(**impacto.dict())
    db.add(db_impacto)
    db.commit()
    db.refresh(db_impacto)
    return db_impacto

@router.put("/impactos/{impacto_id}", response_model=esquemas.Impacto)
def actualizar_impacto(impacto_id: int, impacto: esquemas.ImpactoCreate, db: Session = Depends(get_db)):
    db_impacto = db.query(modelos.Impacto).filter(modelos.Impacto.id == impacto_id).first()
    if db_impacto is None:
        raise HTTPException(status_code=404, detail="Impacto no encontrado")
    for key, value in impacto.dict().items():
        setattr(db_impacto, key, value)
    db.commit()
    db.refresh(db_impacto)
    return db_impacto

@router.delete("/impactos/{impacto_id}", response_model=esquemas.Impacto)
def eliminar_impacto(impacto_id: int, db: Session = Depends(get_db)):
    db_impacto = db.query(modelos.Impacto).filter(modelos.Impacto.id == impacto_id).first()
    if db_impacto is None:
        raise HTTPException(status_code=404, detail="Impacto no encontrado")
    db.delete(db_impacto)
    db.commit()
    return db_impacto
