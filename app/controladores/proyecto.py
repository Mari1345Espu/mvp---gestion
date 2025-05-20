from fastapi import APIRouter, Depends, HTTPException, Query, Request, Form, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta, date
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app import esquemas, modelos
from app.db.session import get_db
from app.esquemas.proyecto import Proyecto, ProyectoCreate, ProyectoBase
from app.modelos.proyecto import Proyecto
from app.modelos.convocatoria import Convocatoria
from app.core.seguridad import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/proyectos/", response_model=List[esquemas.Proyecto])
def leer_proyectos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    proyectos = db.query(modelos.Proyecto).offset(skip).limit(limit).all()
    return proyectos

@router.get("/proyectos/{proyecto_id}", response_model=esquemas.Proyecto)
def leer_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto

@router.post("/proyectos/", response_model=esquemas.Proyecto)
def crear_proyecto(proyecto: esquemas.ProyectoCreate, db: Session = Depends(get_db)):
    db_proyecto = modelos.Proyecto(**proyecto.dict())
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.put("/proyectos/{proyecto_id}", response_model=esquemas.Proyecto)
def actualizar_proyecto(proyecto_id: int, proyecto: esquemas.ProyectoCreate, db: Session = Depends(get_db)):
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    for key, value in proyecto.dict().items():
        setattr(db_proyecto, key, value)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.delete("/proyectos/{proyecto_id}", response_model=esquemas.Proyecto)
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    db.delete(db_proyecto)
    db.commit()
    return db_proyecto

@router.get("/proyectos/dashboard", response_model=esquemas.DashboardResponse)
async def get_dashboard(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    """Obtiene métricas y estadísticas para el dashboard"""
    
    # Total de proyectos
    total_proyectos = db.query(func.count(modelos.Proyecto.id)).scalar()
    
    # Proyectos por estado
    proyectos_por_estado = db.query(
        modelos.Estado.nombre,
        func.count(modelos.Proyecto.id)
    ).join(
        modelos.Proyecto
    ).group_by(
        modelos.Estado.nombre
    ).all()
    
    # Proyectos próximos a vencer (en los próximos 30 días)
    fecha_limite = datetime.now() + timedelta(days=30)
    proyectos_por_vencer = db.query(modelos.Proyecto).filter(
        modelos.Proyecto.fecha_fin <= fecha_limite,
        modelos.Proyecto.fecha_fin >= datetime.now()
    ).all()
    
    # Presupuesto total y gastado
    presupuesto_total = db.query(func.sum(modelos.Proyecto.presupuesto)).scalar() or 0
    gasto_total = db.query(func.sum(modelos.Recurso.monto)).scalar() or 0
    
    # Productos por tipo
    productos_por_tipo = db.query(
        modelos.TipoProducto.nombre,
        func.count(modelos.Producto.id)
    ).join(
        modelos.Producto
    ).group_by(
        modelos.TipoProducto.nombre
    ).all()
    
    # Proyectos por facultad
    proyectos_por_facultad = db.query(
        modelos.Facultad.nombre,
        func.count(modelos.Proyecto.id)
    ).join(
        modelos.Proyecto
    ).group_by(
        modelos.Facultad.nombre
    ).all()
    
    return {
        "total_proyectos": total_proyectos,
        "proyectos_por_estado": dict(proyectos_por_estado),
        "proyectos_por_vencer": len(proyectos_por_vencer),
        "presupuesto_total": presupuesto_total,
        "gasto_total": gasto_total,
        "productos_por_tipo": dict(productos_por_tipo),
        "proyectos_por_facultad": dict(proyectos_por_facultad)
    }

@router.get("/proyectos/reporte", response_model=esquemas.ReporteProyecto)
async def generar_reporte(
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    facultad_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    """Genera un reporte detallado de proyectos según los filtros especificados"""
    
    query = db.query(modelos.Proyecto)
    
    if fecha_inicio:
        query = query.filter(modelos.Proyecto.fecha_inicio >= fecha_inicio)
    if fecha_fin:
        query = query.filter(modelos.Proyecto.fecha_fin <= fecha_fin)
    if facultad_id:
        query = query.filter(modelos.Proyecto.facultad_id == facultad_id)
    if estado_id:
        query = query.filter(modelos.Proyecto.estado_id == estado_id)
    
    proyectos = query.all()
    
    # Calcular métricas
    total_proyectos = len(proyectos)
    presupuesto_total = sum(p.presupuesto for p in proyectos)
    gasto_total = sum(r.monto for p in proyectos for r in p.recursos)
    
    # Calcular avance promedio
    avance_promedio = sum(p.avance for p in proyectos) / total_proyectos if total_proyectos > 0 else 0
    
    return {
        "total_proyectos": total_proyectos,
        "presupuesto_total": presupuesto_total,
        "gasto_total": gasto_total,
        "avance_promedio": avance_promedio,
        "proyectos": proyectos
    }

@router.get("/admin/proyectos", response_class=HTMLResponse)
def listar_proyectos(request: Request, db: Session = Depends(get_db)):
    proyectos = db.query(Proyecto).all()
    convocatorias = db.query(Convocatoria).all()
    return templates.TemplateResponse("admin/proyectos.html", {"request": request, "proyectos": proyectos, "convocatorias": convocatorias})

@router.post("/admin/proyectos/crear")
def crear_proyecto(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    fecha_inicio: date = Form(...),
    fecha_fin: date = Form(...),
    convocatoria_id: int = Form(...),
    estado: str = Form(...),
    db: Session = Depends(get_db)
):
    proyecto = Proyecto(
        nombre=nombre,
        descripcion=descripcion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        convocatoria_id=convocatoria_id,
        estado=estado
    )
    db.add(proyecto)
    db.commit()
    return RedirectResponse(url="/admin/proyectos", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/proyectos/editar/{proyecto_id}")
def editar_proyecto(
    proyecto_id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    fecha_inicio: date = Form(...),
    fecha_fin: date = Form(...),
    convocatoria_id: int = Form(...),
    estado: str = Form(...),
    db: Session = Depends(get_db)
):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    if proyecto:
        proyecto.nombre = nombre
        proyecto.descripcion = descripcion
        proyecto.fecha_inicio = fecha_inicio
        proyecto.fecha_fin = fecha_fin
        proyecto.convocatoria_id = convocatoria_id
        proyecto.estado = estado
        db.commit()
    return RedirectResponse(url="/admin/proyectos", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/proyectos/eliminar/{proyecto_id}")
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    if proyecto:
        db.delete(proyecto)
        db.commit()
    return RedirectResponse(url="/admin/proyectos", status_code=status.HTTP_303_SEE_OTHER)
