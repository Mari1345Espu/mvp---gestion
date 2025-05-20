from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.convocatoria import ConvocatoriaBase, ConvocatoriaCreate, Convocatoria
from app.modelos.convocatoria import Convocatoria as ConvocatoriaModelo
from datetime import date

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/convocatorias/", response_model=List[esquemas.Convocatoria])
def leer_convocatorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    convocatorias = db.query(modelos.Convocatoria).offset(skip).limit(limit).all()
    return convocatorias

@router.get("/convocatorias/{convocatoria_id}", response_model=esquemas.Convocatoria)
def leer_convocatoria(convocatoria_id: int, db: Session = Depends(get_db)):
    convocatoria = db.query(modelos.Convocatoria).filter(modelos.Convocatoria.id == convocatoria_id).first()
    if convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    return convocatoria

@router.post("/convocatorias/", response_model=esquemas.Convocatoria)
def crear_convocatoria(convocatoria: esquemas.ConvocatoriaCreate, db: Session = Depends(get_db)):
    db_convocatoria = modelos.Convocatoria(**convocatoria.dict())
    db.add(db_convocatoria)
    db.commit()
    db.refresh(db_convocatoria)
    return db_convocatoria

@router.put("/convocatorias/{convocatoria_id}", response_model=esquemas.Convocatoria)
def actualizar_convocatoria(convocatoria_id: int, convocatoria: esquemas.ConvocatoriaCreate, db: Session = Depends(get_db)):
    db_convocatoria = db.query(modelos.Convocatoria).filter(modelos.Convocatoria.id == convocatoria_id).first()
    if db_convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    for key, value in convocatoria.dict().items():
        setattr(db_convocatoria, key, value)
    db.commit()
    db.refresh(db_convocatoria)
    return db_convocatoria

@router.delete("/convocatorias/{convocatoria_id}", response_model=esquemas.Convocatoria)
def eliminar_convocatoria(convocatoria_id: int, db: Session = Depends(get_db)):
    db_convocatoria = db.query(modelos.Convocatoria).filter(modelos.Convocatoria.id == convocatoria_id).first()
    if db_convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    db.delete(db_convocatoria)
    db.commit()
    return db_convocatoria

@router.get("/admin/convocatorias", response_class=HTMLResponse)
def listar_convocatorias(request: Request, db: Session = Depends(get_db)):
    convocatorias = db.query(Convocatoria).all()
    return templates.TemplateResponse("admin/convocatorias.html", {"request": request, "convocatorias": convocatorias})

@router.post("/admin/convocatorias/crear")
def crear_convocatoria(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    fecha_inicio: date = Form(...),
    fecha_fin: date = Form(...),
    db: Session = Depends(get_db)
):
    convocatoria = Convocatoria(
        nombre=nombre,
        descripcion=descripcion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado="Abierta"
    )
    db.add(convocatoria)
    db.commit()
    return RedirectResponse(url="/admin/convocatorias", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/convocatorias/editar/{convocatoria_id}")
def editar_convocatoria(
    convocatoria_id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    fecha_inicio: date = Form(...),
    fecha_fin: date = Form(...),
    estado: str = Form(...),
    db: Session = Depends(get_db)
):
    convocatoria = db.query(Convocatoria).filter(Convocatoria.id == convocatoria_id).first()
    if convocatoria:
        convocatoria.nombre = nombre
        convocatoria.descripcion = descripcion
        convocatoria.fecha_inicio = fecha_inicio
        convocatoria.fecha_fin = fecha_fin
        convocatoria.estado = estado
        db.commit()
    return RedirectResponse(url="/admin/convocatorias", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/convocatorias/eliminar/{convocatoria_id}")
def eliminar_convocatoria(convocatoria_id: int, db: Session = Depends(get_db)):
    convocatoria = db.query(Convocatoria).filter(Convocatoria.id == convocatoria_id).first()
    if convocatoria:
        db.delete(convocatoria)
        db.commit()
    return RedirectResponse(url="/admin/convocatorias", status_code=status.HTTP_303_SEE_OTHER)
