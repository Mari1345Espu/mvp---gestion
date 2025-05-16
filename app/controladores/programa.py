from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.programa import ProgramaBase, ProgramaCreate, Programa
from app.modelos.programa import Programa as ProgramaModelo

router = APIRouter()

@router.get("/programas/", response_model=List[esquemas.Programa])
def leer_programas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    programas = db.query(modelos.Programa).offset(skip).limit(limit).all()
    return programas

@router.get("/programas/{programa_id}", response_model=esquemas.Programa)
def leer_programa(programa_id: int, db: Session = Depends(get_db)):
    programa = db.query(modelos.Programa).filter(modelos.Programa.id == programa_id).first()
    if programa is None:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return programa

@router.post("/programas/", response_model=esquemas.Programa)
def crear_programa(programa: esquemas.ProgramaCreate, db: Session = Depends(get_db)):
    db_programa = modelos.Programa(**programa.dict())
    db.add(db_programa)
    db.commit()
    db.refresh(db_programa)
    return db_programa

@router.put("/programas/{programa_id}", response_model=esquemas.Programa)
def actualizar_programa(programa_id: int, programa: esquemas.ProgramaCreate, db: Session = Depends(get_db)):
    db_programa = db.query(modelos.Programa).filter(modelos.Programa.id == programa_id).first()
    if db_programa is None:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    for key, value in programa.dict().items():
        setattr(db_programa, key, value)
    db.commit()
    db.refresh(db_programa)
    return db_programa

@router.delete("/programas/{programa_id}", response_model=esquemas.Programa)
def eliminar_programa(programa_id: int, db: Session = Depends(get_db)):
    db_programa = db.query(modelos.Programa).filter(modelos.Programa.id == programa_id).first()
    if db_programa is None:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    db.delete(db_programa)
    db.commit()
    return db_programa
