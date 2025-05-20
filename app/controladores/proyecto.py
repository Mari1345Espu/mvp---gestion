from fastapi import APIRouter, Depends, HTTPException, Query, Request, Form, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta, date
from fastapi.responses import JSONResponse

from app import modelos
from app.db.session import get_db
from app.core.seguridad import get_current_user
from app.esquemas.proyecto import Proyecto, ProyectoCreate, ProyectoUpdate, DashboardResponse, ReporteProyecto

router = APIRouter()

@router.get("/proyectos/", response_model=List[Proyecto])
def get_proyectos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    proyectos = db.query(modelos.Proyecto).offset(skip).limit(limit).all()
    return proyectos

@router.post("/proyectos/", response_model=Proyecto)
def create_proyecto(
    proyecto: ProyectoCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    db_proyecto = modelos.Proyecto(**proyecto.dict())
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.get("/proyectos/{proyecto_id}", response_model=Proyecto)
def get_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto

@router.put("/proyectos/{proyecto_id}", response_model=Proyecto)
def update_proyecto(
    proyecto_id: int,
    proyecto: ProyectoUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    for key, value in proyecto.dict(exclude_unset=True).items():
        setattr(db_proyecto, key, value)
    
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.delete("/proyectos/{proyecto_id}")
def delete_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    db.delete(proyecto)
    db.commit()
    return {"message": "Proyecto eliminado exitosamente"}

@router.get("/proyectos/dashboard", response_model=DashboardResponse)
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

@router.get("/proyectos/reporte", response_model=ReporteProyecto)
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
