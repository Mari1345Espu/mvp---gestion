from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.notificacion import NotificacionBase, NotificacionCreate, Notificacion
from app.modelos.notificacion import Notificacion as NotificacionModelo

router = APIRouter()

@router.get("/notificaciones/", response_model=List[esquemas.Notificacion])
def leer_notificaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notificaciones = db.query(modelos.Notificacion).offset(skip).limit(limit).all()
    return notificaciones

@router.get("/notificaciones/{notificacion_id}", response_model=esquemas.Notificacion)
def leer_notificacion(notificacion_id: int, db: Session = Depends(get_db)):
    notificacion = db.query(modelos.Notificacion).filter(modelos.Notificacion.id == notificacion_id).first()
    if notificacion is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return notificacion

@router.post("/notificaciones/", response_model=esquemas.Notificacion)
def crear_notificacion(notificacion: esquemas.NotificacionCreate, db: Session = Depends(get_db)):
    db_notificacion = modelos.Notificacion(**notificacion.dict())
    db.add(db_notificacion)
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion

@router.put("/notificaciones/{notificacion_id}", response_model=esquemas.Notificacion)
def actualizar_notificacion(notificacion_id: int, notificacion: esquemas.NotificacionCreate, db: Session = Depends(get_db)):
    db_notificacion = db.query(modelos.Notificacion).filter(modelos.Notificacion.id == notificacion_id).first()
    if db_notificacion is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    for key, value in notificacion.dict().items():
        setattr(db_notificacion, key, value)
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion

@router.delete("/notificaciones/{notificacion_id}", response_model=esquemas.Notificacion)
def eliminar_notificacion(notificacion_id: int, db: Session = Depends(get_db)):
    db_notificacion = db.query(modelos.Notificacion).filter(modelos.Notificacion.id == notificacion_id).first()
    if db_notificacion is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    db.delete(db_notificacion)
    db.commit()
    return db_notificacion
