from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db
from app.esquemas.recurso import Recurso, RecursoCreate, RecursoBase
from app.modelos.recurso import Recurso

router = APIRouter()

@router.get("/recursos/", response_model=List[esquemas.Recurso])
def leer_recursos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recursos = db.query(modelos.Recurso).offset(skip).limit(limit).all()
    return recursos

@router.get("/recursos/{recurso_id}", response_model=esquemas.Recurso)
def leer_recurso(recurso_id: int, db: Session = Depends(get_db)):
    recurso = db.query(modelos.Recurso).filter(modelos.Recurso.id == recurso_id).first()
    if recurso is None:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return recurso

@router.post("/recursos/", response_model=esquemas.Recurso)
def crear_recurso(recurso: esquemas.RecursoCreate, db: Session = Depends(get_db)):
    db_recurso = modelos.Recurso(**recurso.dict())
    db.add(db_recurso)
    db.commit()
    db.refresh(db_recurso)
    return db_recurso

@router.put("/recursos/{recurso_id}", response_model=esquemas.Recurso)
def actualizar_recurso(recurso_id: int, recurso: esquemas.RecursoCreate, db: Session = Depends(get_db)):
    db_recurso = db.query(modelos.Recurso).filter(modelos.Recurso.id == recurso_id).first()
    if db_recurso is None:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    for key, value in recurso.dict().items():
        setattr(db_recurso, key, value)
    db.commit()
    db.refresh(db_recurso)
    return db_recurso

@router.delete("/recursos/{recurso_id}", response_model=esquemas.Recurso)
def eliminar_recurso(recurso_id: int, db: Session = Depends(get_db)):
    db_recurso = db.query(modelos.Recurso).filter(modelos.Recurso.id == recurso_id).first()
    if db_recurso is None:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    db.delete(db_recurso)
    db.commit()
    return db_recurso
