from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.anexo import AnexoBase, AnexoCreate, Anexo
from app.modelos.anexo import Anexo as AnexoModelo

router = APIRouter()

@router.get("/anexos/", response_model=List[esquemas.Anexo])
def leer_anexos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    anexos = db.query(modelos.Anexo).offset(skip).limit(limit).all()
    return anexos

@router.get("/anexos/{anexo_id}", response_model=esquemas.Anexo)
def leer_anexo(anexo_id: int, db: Session = Depends(get_db)):
    anexo = db.query(modelos.Anexo).filter(modelos.Anexo.id == anexo_id).first()
    if anexo is None:
        raise HTTPException(status_code=404, detail="Anexo no encontrado")
    return anexo

@router.post("/anexos/", response_model=esquemas.Anexo)
def crear_anexo(anexo: esquemas.AnexoCreate, db: Session = Depends(get_db)):
    db_anexo = modelos.Anexo(**anexo.dict())
    db.add(db_anexo)
    db.commit()
    db.refresh(db_anexo)
    return db_anexo

@router.put("/anexos/{anexo_id}", response_model=esquemas.Anexo)
def actualizar_anexo(anexo_id: int, anexo: esquemas.AnexoCreate, db: Session = Depends(get_db)):
    db_anexo = db.query(modelos.Anexo).filter(modelos.Anexo.id == anexo_id).first()
    if db_anexo is None:
        raise HTTPException(status_code=404, detail="Anexo no encontrado")
    for key, value in anexo.dict().items():
        setattr(db_anexo, key, value)
    db.commit()
    db.refresh(db_anexo)
    return db_anexo

@router.delete("/anexos/{anexo_id}", response_model=esquemas.Anexo)
def eliminar_anexo(anexo_id: int, db: Session = Depends(get_db)):
    db_anexo = db.query(modelos.Anexo).filter(modelos.Anexo.id == anexo_id).first()
    if db_anexo is None:
        raise HTTPException(status_code=404, detail="Anexo no encontrado")
    db.delete(db_anexo)
    db.commit()
    return db_anexo
