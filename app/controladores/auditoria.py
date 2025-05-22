from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime, timedelta

from app import modelos
from app.db.session import get_db
from app.esquemas.auditoria import (
    Auditoria as AuditoriaSchema,
    AuditoriaCreate,
    AuditoriaEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/auditoria",
    tags=["auditoria"]
)

@router.get("/", response_model=List[AuditoriaSchema])
def read_auditoria(
    skip: int = 0,
    limit: int = 100,
    usuario_id: Optional[int] = None,
    accion: Optional[str] = None,
    tabla: Optional[str] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver los registros de auditoría"
        )
    
    query = db.query(modelos.Auditoria)
    
    if usuario_id:
        query = query.filter(modelos.Auditoria.usuario_id == usuario_id)
    if accion:
        query = query.filter(modelos.Auditoria.accion == accion)
    if tabla:
        query = query.filter(modelos.Auditoria.tabla == tabla)
    if fecha_inicio and fecha_fin:
        query = query.filter(
            and_(
                modelos.Auditoria.fecha_creacion >= fecha_inicio,
                modelos.Auditoria.fecha_creacion <= fecha_fin
            )
        )
    if search:
        query = query.filter(
            or_(
                modelos.Auditoria.accion.ilike(f"%{search}%"),
                modelos.Auditoria.tabla.ilike(f"%{search}%"),
                modelos.Auditoria.observaciones.ilike(f"%{search}%")
            )
        )
    
    registros = query.order_by(modelos.Auditoria.fecha_creacion.desc()).offset(skip).limit(limit).all()
    return registros

@router.get("/{auditoria_id}", response_model=AuditoriaSchema)
def read_auditoria_by_id(
    auditoria_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver los registros de auditoría"
        )
    
    registro = db.query(modelos.Auditoria).filter(
        modelos.Auditoria.id == auditoria_id
    ).first()
    if registro is None:
        raise HTTPException(status_code=404, detail="Registro de auditoría no encontrado")
    return registro

@router.post("/", response_model=AuditoriaSchema)
def create_auditoria(
    request: Request,
    auditoria: AuditoriaCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    # Obtener IP y User Agent
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    
    # Crear registro de auditoría
    db_auditoria = modelos.Auditoria(
        **auditoria.dict(),
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(db_auditoria)
    db.commit()
    db.refresh(db_auditoria)
    return db_auditoria

@router.get("/estadisticas/", response_model=AuditoriaEstadisticas)
def get_estadisticas_auditoria(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas de auditoría"
        )
    
    # Total de registros
    total_registros = db.query(func.count(modelos.Auditoria.id)).scalar()
    
    # Registros por acción
    registros_por_accion = dict(
        db.query(
            modelos.Auditoria.accion,
            func.count(modelos.Auditoria.id)
        ).group_by(modelos.Auditoria.accion).all()
    )
    
    # Registros por tabla
    registros_por_tabla = dict(
        db.query(
            modelos.Auditoria.tabla,
            func.count(modelos.Auditoria.id)
        ).group_by(modelos.Auditoria.tabla).all()
    )
    
    # Registros por usuario
    registros_por_usuario = dict(
        db.query(
            modelos.Usuario.nombre,
            func.count(modelos.Auditoria.id)
        ).join(modelos.Auditoria).group_by(modelos.Usuario.nombre).all()
    )
    
    # Registros por mes
    registros_por_mes = dict(
        db.query(
            func.date_trunc('month', modelos.Auditoria.fecha_creacion).label('mes'),
            func.count(modelos.Auditoria.id)
        ).group_by('mes').all()
    )
    
    # Registros por día
    registros_por_dia = dict(
        db.query(
            func.date_trunc('day', modelos.Auditoria.fecha_creacion).label('dia'),
            func.count(modelos.Auditoria.id)
        ).group_by('dia').all()
    )
    
    # Registros por hora
    registros_por_hora = dict(
        db.query(
            extract('hour', modelos.Auditoria.fecha_creacion).label('hora'),
            func.count(modelos.Auditoria.id)
        ).group_by('hora').all()
    )
    
    # Últimas acciones
    ultimas_acciones = db.query(modelos.Auditoria).order_by(
        modelos.Auditoria.fecha_creacion.desc()
    ).limit(10).all()
    
    # Usuarios más activos
    usuarios_mas_activos = dict(
        db.query(
            modelos.Usuario.nombre,
            func.count(modelos.Auditoria.id)
        ).join(modelos.Auditoria).group_by(modelos.Usuario.nombre).order_by(
            func.count(modelos.Auditoria.id).desc()
        ).limit(5).all()
    )
    
    # Tablas más modificadas
    tablas_mas_modificadas = dict(
        db.query(
            modelos.Auditoria.tabla,
            func.count(modelos.Auditoria.id)
        ).group_by(modelos.Auditoria.tabla).order_by(
            func.count(modelos.Auditoria.id).desc()
        ).limit(5).all()
    )
    
    return AuditoriaEstadisticas(
        total_registros=total_registros,
        registros_por_accion=registros_por_accion,
        registros_por_tabla=registros_por_tabla,
        registros_por_usuario=registros_por_usuario,
        registros_por_mes=registros_por_mes,
        registros_por_dia=registros_por_dia,
        registros_por_hora=registros_por_hora,
        ultimas_acciones=ultimas_acciones,
        usuarios_mas_activos=usuarios_mas_activos,
        tablas_mas_modificadas=tablas_mas_modificadas
    )
