from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.destino import DestinoBase, DestinoCreate, Destino
from app.modelos.destino import Destino as DestinoModelo

router = APIRouter()

@router.get("/destinos/", response_model=List[esquemas.Destino])
def leer_destinos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    destinos = db.query(modelos.Destino).offset(skip).limit(limit).all()
    return destinos

@router.get("/destinos/{destino_id}", response_model=esquemas.Destino)
def leer_destino(destino_id: int, db: Session = Depends(get_db)):
    destino = db.query(modelos.Destino).filter(modelos.Destino.id == destino_id).first()
    if destino is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    return destino

@router.post("/destinos/", response_model=esquemas.Destino)
def crear_destino(destino: esquemas.DestinoCreate, db: Session = Depends(get_db)):
    db_destino = modelos.Destino(**destino.dict())
    db.add(db_destino)
    db.commit()
    db.refresh(db_destino)
    return db_destino

@router.put("/destinos/{destino_id}", response_model=esquemas.Destino)
def actualizar_destino(destino_id: int, destino: esquemas.DestinoCreate, db: Session = Depends(get_db)):
    db_destino = db.query(modelos.Destino).filter(modelos.Destino.id == destino_id).first()
    if db_destino is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    for key, value in destino.dict().items():
        setattr(db_destino, key, value)
    db.commit()
    db.refresh(db_destino)
    return db_destino

@router.delete("/destinos/{destino_id}", response_model=esquemas.Destino)
def eliminar_destino(destino_id: int, db: Session = Depends(get_db)):
    db_destino = db.query(modelos.Destino).filter(modelos.Destino.id == destino_id).first()
    if db_destino is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    db.delete(db_destino)
    db.commit()
    return db_destino
