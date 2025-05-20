from fastapi import APIRouter, Depends, HTTPException, Query, Request, Form, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta, date
from fastapi.responses import JSONResponse

from app import modelos
from app.db.session import get_db
from app.core.seguridad import get_current_user
from app.esquemas.convocatoria import Convocatoria, ConvocatoriaCreate, ConvocatoriaUpdate

router = APIRouter()

@router.get("/convocatorias/", response_model=List[Convocatoria])
def get_convocatorias(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    convocatorias = db.query(modelos.Convocatoria).offset(skip).limit(limit).all()
    return convocatorias

@router.post("/convocatorias/", response_model=Convocatoria)
def create_convocatoria(
    convocatoria: ConvocatoriaCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    db_convocatoria = modelos.Convocatoria(**convocatoria.dict())
    db.add(db_convocatoria)
    db.commit()
    db.refresh(db_convocatoria)
    return db_convocatoria

@router.get("/convocatorias/{convocatoria_id}", response_model=Convocatoria)
def get_convocatoria(
    convocatoria_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    convocatoria = db.query(modelos.Convocatoria).filter(modelos.Convocatoria.id == convocatoria_id).first()
    if convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    return convocatoria

@router.put("/convocatorias/{convocatoria_id}", response_model=Convocatoria)
def update_convocatoria(
    convocatoria_id: int,
    convocatoria: ConvocatoriaUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    db_convocatoria = db.query(modelos.Convocatoria).filter(modelos.Convocatoria.id == convocatoria_id).first()
    if db_convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    
    for key, value in convocatoria.dict(exclude_unset=True).items():
        setattr(db_convocatoria, key, value)
    
    db.commit()
    db.refresh(db_convocatoria)
    return db_convocatoria

@router.delete("/convocatorias/{convocatoria_id}")
def delete_convocatoria(
    convocatoria_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    convocatoria = db.query(modelos.Convocatoria).filter(modelos.Convocatoria.id == convocatoria_id).first()
    if convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    
    db.delete(convocatoria)
    db.commit()
    return {"message": "Convocatoria eliminada exitosamente"}
