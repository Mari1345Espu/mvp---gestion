from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime, timedelta

from app import esquemas, modelos
from app.db.session import get_db
from app.core.seguridad import get_current_user

router = APIRouter()

@router.get("/reportes/rendimiento-facultades")
async def reporte_rendimiento_facultades(
    año: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    """Genera un reporte de rendimiento por facultad"""
    query = db.query(
        modelos.Facultad.nombre,
        func.count(modelos.Proyecto.id).label('total_proyectos'),
        func.avg(modelos.Proyecto.avance).label('avance_promedio'),
        func.sum(modelos.Proyecto.presupuesto).label('presupuesto_total'),
        func.sum(modelos.Recurso.monto).label('gasto_total')
    ).join(
        modelos.Proyecto
    ).outerjoin(
        modelos.Recurso
    ).group_by(
        modelos.Facultad.nombre
    )
    
    if año:
        query = query.filter(
            extract('year', modelos.Proyecto.fecha_inicio) == año
        )
    
    resultados = query.all()
    
    return [{
        "facultad": r.nombre,
        "total_proyectos": r.total_proyectos,
        "avance_promedio": float(r.avance_promedio or 0),
        "presupuesto_total": float(r.presupuesto_total or 0),
        "gasto_total": float(r.gasto_total or 0),
        "eficiencia": float(r.gasto_total or 0) / float(r.presupuesto_total or 1) * 100
    } for r in resultados]

@router.get("/reportes/impacto-investigacion")
async def reporte_impacto_investigacion(
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    """Genera un reporte de impacto de la investigación"""
    query = db.query(
        modelos.LineaInvestigacion.nombre,
        func.count(modelos.Producto.id).label('total_productos'),
        func.count(modelos.Impacto.id).label('total_impactos'),
        func.avg(modelos.Impacto.puntuacion).label('impacto_promedio')
    ).join(
        modelos.Proyecto
    ).join(
        modelos.Producto
    ).outerjoin(
        modelos.Impacto
    ).group_by(
        modelos.LineaInvestigacion.nombre
    )
    
    if fecha_inicio:
        query = query.filter(modelos.Proyecto.fecha_inicio >= fecha_inicio)
    if fecha_fin:
        query = query.filter(modelos.Proyecto.fecha_fin <= fecha_fin)
    
    resultados = query.all()
    
    return [{
        "linea_investigacion": r.nombre,
        "total_productos": r.total_productos,
        "total_impactos": r.total_impactos,
        "impacto_promedio": float(r.impacto_promedio or 0)
    } for r in resultados]

@router.get("/reportes/rendimiento-investigadores")
async def reporte_rendimiento_investigadores(
    año: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    """Genera un reporte de rendimiento de investigadores"""
    query = db.query(
        modelos.Usuario.nombre,
        func.count(modelos.Participante.id).label('total_proyectos'),
        func.count(modelos.Producto.id).label('total_productos'),
        func.avg(modelos.Proyecto.avance).label('avance_promedio')
    ).join(
        modelos.Participante
    ).join(
        modelos.Proyecto
    ).outerjoin(
        modelos.Producto
    ).group_by(
        modelos.Usuario.nombre
    )
    
    if año:
        query = query.filter(
            extract('year', modelos.Proyecto.fecha_inicio) == año
        )
    
    resultados = query.all()
    
    return [{
        "investigador": r.nombre,
        "total_proyectos": r.total_proyectos,
        "total_productos": r.total_productos,
        "avance_promedio": float(r.avance_promedio or 0)
    } for r in resultados]

@router.get("/reportes/tendencias-investigacion")
async def reporte_tendencias_investigacion(
    años: int = 5,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    """Genera un reporte de tendencias de investigación por año"""
    fecha_limite = datetime.now() - timedelta(days=365 * años)
    
    query = db.query(
        extract('year', modelos.Proyecto.fecha_inicio).label('año'),
        func.count(modelos.Proyecto.id).label('total_proyectos'),
        func.count(modelos.Producto.id).label('total_productos'),
        func.sum(modelos.Proyecto.presupuesto).label('presupuesto_total')
    ).outerjoin(
        modelos.Producto
    ).filter(
        modelos.Proyecto.fecha_inicio >= fecha_limite
    ).group_by(
        'año'
    ).order_by(
        'año'
    )
    
    resultados = query.all()
    
    return [{
        "año": int(r.año),
        "total_proyectos": r.total_proyectos,
        "total_productos": r.total_productos,
        "presupuesto_total": float(r.presupuesto_total or 0)
    } for r in resultados] 