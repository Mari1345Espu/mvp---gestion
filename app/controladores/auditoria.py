from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.auditoria import AuditoriaBase, AuditoriaCreate, Auditoria
from app.modelos.auditoria import Auditoria as AuditoriaModelo

router = APIRouter()

@router.get("/auditorias/", response_model=List[esquemas.Auditoria])
def leer_auditorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    auditorias = db.query(modelos.Auditoria).offset(skip).limit(limit).all()
    return auditorias

@router.get("/auditorias/{auditoria_id}", response_model=esquemas.Auditoria)
def leer_auditoria(auditoria_id: int, db: Session = Depends(get_db)):
    auditoria = db.query(modelos.Auditoria).filter(modelos.Auditoria.id == auditoria_id).first()
    if auditoria is None:
        raise HTTPException(status_code=404, detail="Auditoría no encontrada")
    return auditoria

@router.post("/auditorias/", response_model=esquemas.Auditoria)
def crear_auditoria(auditoria: esquemas.AuditoriaCreate, db: Session = Depends(get_db)):
    db_auditoria = modelos.Auditoria(**auditoria.dict())
    db.add(db_auditoria)
    db.commit()
    db.refresh(db_auditoria)
    return db_auditoria

@router.put("/auditorias/{auditoria_id}", response_model=esquemas.Auditoria)
def actualizar_auditoria(auditoria_id: int, auditoria: esquemas.AuditoriaCreate, db: Session = Depends(get_db)):
    db_auditoria = db.query(modelos.Auditoria).filter(modelos.Auditoria.id == auditoria_id).first()
    if db_auditoria is None:
        raise HTTPException(status_code=404, detail="Auditoría no encontrada")
    for key, value in auditoria.dict().items():
        setattr(db_auditoria, key, value)
    db.commit()
    db.refresh(db_auditoria)
    return db_auditoria

@router.delete("/auditorias/{auditoria_id}", response_model=esquemas.Auditoria)
def eliminar_auditoria(auditoria_id: int, db: Session = Depends(get_db)):
    db_auditoria = db.query(modelos.Auditoria).filter(modelos.Auditoria.id == auditoria_id).first()
    if db_auditoria is None:
        raise HTTPException(status_code=404, detail="Auditoría no encontrada")
    db.delete(db_auditoria)
    db.commit()
    return db_auditoria
