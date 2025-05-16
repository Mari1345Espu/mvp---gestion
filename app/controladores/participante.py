from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db
from app.esquemas.participante import Participante, ParticipanteCreate, ParticipanteBase
from app.modelos.participante import Participante as ParticipanteModel

router = APIRouter()

@router.get("/participantes/", response_model=List[esquemas.Participante])
def leer_participantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    participantes = db.query(modelos.Participante).offset(skip).limit(limit).all()
    return participantes

@router.get("/participantes/{participante_id}", response_model=esquemas.Participante)
def leer_participante(participante_id: int, db: Session = Depends(get_db)):
    participante = db.query(modelos.Participante).filter(modelos.Participante.id == participante_id).first()
    if participante is None:
        raise HTTPException(status_code=404, detail="Participante no encontrado")
    return participante

@router.post("/participantes/", response_model=esquemas.Participante)
def crear_participante(participante: esquemas.ParticipanteCreate, db: Session = Depends(get_db)):
    db_participante = modelos.Participante(**participante.dict())
    db.add(db_participante)
    db.commit()
    db.refresh(db_participante)
    return db_participante

@router.put("/participantes/{participante_id}", response_model=esquemas.Participante)
def actualizar_participante(participante_id: int, participante: esquemas.ParticipanteCreate, db: Session = Depends(get_db)):
    db_participante = db.query(modelos.Participante).filter(modelos.Participante.id == participante_id).first()
    if db_participante is None:
        raise HTTPException(status_code=404, detail="Participante no encontrado")
    for key, value in participante.dict().items():
        setattr(db_participante, key, value)
    db.commit()
    db.refresh(db_participante)
    return db_participante

@router.delete("/participantes/{participante_id}", response_model=esquemas.Participante)
def eliminar_participante(participante_id: int, db: Session = Depends(get_db)):
    db_participante = db.query(modelos.Participante).filter(modelos.Participante.id == participante_id).first()
    if db_participante is None:
        raise HTTPException(status_code=404, detail="Participante no encontrado")
    db.delete(db_participante)
    db.commit()
    return db_participante
