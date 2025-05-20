from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modelos.proyecto import Proyecto
from app.modelos.convocatoria import Convocatoria
from app.modelos.programa import Programa
from app.modelos.tipo_proyecto import TipoProyecto

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def biblioteca_publica(request: Request, db: Session = Depends(get_db)):
    proyectos = db.query(Proyecto).all()
    convocatorias = db.query(Convocatoria).all()
    programas = db.query(Programa).all()
    tipos = db.query(TipoProyecto).all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "proyectos": proyectos,
            "convocatorias": convocatorias,
            "programas": programas,
            "tipos": tipos
        }
    ) 