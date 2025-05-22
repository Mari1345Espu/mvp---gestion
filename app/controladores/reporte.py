from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime, timedelta
import os
import json
from uuid import uuid4

from ..dependencias import get_db, get_current_user
from ..modelos import Reporte as ReporteModel, Usuario
from ..esquemas.reporte import (
    Reporte, ReporteCreate, ReporteUpdate, ReporteEstadisticas,
    TipoReporte, FormatoReporte, EstadoReporte
)
from ..esquemas.usuario import Usuario as UsuarioSchema
from ..config import settings

router = APIRouter(
    prefix="/reportes",
    tags=["reportes"]
)

# Directorio para almacenar reportes generados
REPORTS_DIR = os.path.join(settings.UPLOAD_DIR, "reportes")
os.makedirs(REPORTS_DIR, exist_ok=True)

async def generar_reporte(reporte: ReporteModel, db: Session):
    """
    Función para generar el reporte en segundo plano.
    Se implementará la lógica de generación de reportes aquí.
    """
    try:
        # Actualizar estado a procesando
        reporte.estado = EstadoReporte.PROCESANDO
        db.commit()

        # TODO: Implementar lógica de generación de reportes según el tipo y formato
        # Por ahora, solo simulamos un proceso
        await asyncio.sleep(5)  # Simular procesamiento

        # Generar nombre único para el archivo
        file_extension = f".{reporte.formato}"
        unique_filename = f"{uuid4()}{file_extension}"
        file_path = os.path.join(REPORTS_DIR, unique_filename)

        # TODO: Generar el archivo real según el formato
        with open(file_path, "w") as f:
            f.write("Contenido del reporte")

        # Actualizar reporte
        reporte.estado = EstadoReporte.COMPLETADO
        reporte.fecha_completado = datetime.utcnow()
        reporte.archivo_url = f"/reportes/{unique_filename}"
        db.commit()

    except Exception as e:
        reporte.estado = EstadoReporte.ERROR
        reporte.error_mensaje = str(e)
        db.commit()

@router.get("/", response_model=List[Reporte])
def read_reportes(
    tipo: Optional[TipoReporte] = None,
    formato: Optional[FormatoReporte] = None,
    estado: Optional[EstadoReporte] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener lista de reportes con filtros opcionales.
    Los usuarios solo ven sus propios reportes.
    Los administradores pueden ver todos los reportes.
    """
    query = db.query(ReporteModel)

    # Aplicar filtros
    if tipo:
        query = query.filter(ReporteModel.tipo == tipo)
    if formato:
        query = query.filter(ReporteModel.formato == formato)
    if estado:
        query = query.filter(ReporteModel.estado == estado)
    if fecha_inicio:
        query = query.filter(ReporteModel.fecha_creacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(ReporteModel.fecha_creacion <= fecha_fin)
    if search:
        search_filter = or_(
            ReporteModel.nombre.ilike(f"%{search}%"),
            ReporteModel.descripcion.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Restricción por usuario si no es administrador
    if current_user.rol != "Admin":
        query = query.filter(ReporteModel.usuario_id == current_user.id)

    # Ordenar por fecha de creación descendente
    query = query.order_by(ReporteModel.fecha_creacion.desc())

    reportes = query.offset(skip).limit(limit).all()
    return reportes

@router.get("/{reporte_id}", response_model=Reporte)
def read_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener un reporte específico por ID.
    Los usuarios solo pueden ver sus propios reportes.
    Los administradores pueden ver cualquier reporte.
    """
    reporte = db.query(ReporteModel).filter(ReporteModel.id == reporte_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin" and reporte.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para ver este reporte")

    return reporte

@router.post("/", response_model=Reporte)
async def create_reporte(
    reporte: ReporteCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Crear un nuevo reporte.
    Los usuarios solo pueden crear reportes para sí mismos.
    """
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == reporte.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin" and reporte.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para crear reportes para otros usuarios")

    db_reporte = ReporteModel(**reporte.dict())
    db.add(db_reporte)
    db.commit()
    db.refresh(db_reporte)

    # Iniciar generación del reporte en segundo plano
    background_tasks.add_task(generar_reporte, db_reporte, db)

    return db_reporte

@router.put("/{reporte_id}", response_model=Reporte)
def update_reporte(
    reporte_id: int,
    reporte: ReporteUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Actualizar un reporte existente.
    Los usuarios solo pueden actualizar sus propios reportes.
    Los administradores pueden actualizar cualquier reporte.
    """
    db_reporte = db.query(ReporteModel).filter(ReporteModel.id == reporte_id).first()
    if not db_reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin" and db_reporte.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para actualizar este reporte")

    # No permitir actualizar reportes completados o en proceso
    if db_reporte.estado in [EstadoReporte.COMPLETADO, EstadoReporte.PROCESANDO]:
        raise HTTPException(
            status_code=400,
            detail="No se puede actualizar un reporte que está completado o en proceso"
        )

    # Actualizar campos
    for key, value in reporte.dict(exclude_unset=True).items():
        setattr(db_reporte, key, value)

    db_reporte.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_reporte)
    return db_reporte

@router.delete("/{reporte_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Eliminar un reporte.
    Los usuarios solo pueden eliminar sus propios reportes.
    Los administradores pueden eliminar cualquier reporte.
    """
    reporte = db.query(ReporteModel).filter(ReporteModel.id == reporte_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin" and reporte.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para eliminar este reporte")

    # Eliminar archivo si existe
    if reporte.archivo_url:
        file_path = os.path.join(REPORTS_DIR, os.path.basename(reporte.archivo_url))
        if os.path.exists(file_path):
            os.remove(file_path)

    db.delete(reporte)
    db.commit()

@router.post("/{reporte_id}/regenerar")
async def regenerar_reporte(
    reporte_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Regenerar un reporte existente.
    Los usuarios solo pueden regenerar sus propios reportes.
    Los administradores pueden regenerar cualquier reporte.
    """
    reporte = db.query(ReporteModel).filter(ReporteModel.id == reporte_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin" and reporte.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para regenerar este reporte")

    # Eliminar archivo anterior si existe
    if reporte.archivo_url:
        file_path = os.path.join(REPORTS_DIR, os.path.basename(reporte.archivo_url))
        if os.path.exists(file_path):
            os.remove(file_path)

    # Reiniciar estado del reporte
    reporte.estado = EstadoReporte.PENDIENTE
    reporte.fecha_completado = None
    reporte.archivo_url = None
    reporte.error_mensaje = None
    reporte.fecha_actualizacion = datetime.utcnow()
    db.commit()

    # Iniciar generación del reporte en segundo plano
    background_tasks.add_task(generar_reporte, reporte, db)

    return {"message": "Reporte en proceso de regeneración"}

@router.get("/estadisticas/", response_model=ReporteEstadisticas)
def get_estadisticas(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener estadísticas de reportes.
    Solo administradores pueden ver estadísticas globales.
    Los usuarios normales solo ven estadísticas de sus propios reportes.
    """
    # Base query
    query = db.query(ReporteModel)

    # Filtrar por usuario si no es admin
    if current_user.rol != "Admin":
        query = query.filter(ReporteModel.usuario_id == current_user.id)

    # Total de reportes
    total_reportes = query.count()

    # Reportes por tipo
    reportes_por_tipo = query.with_entities(
        ReporteModel.tipo,
        func.count(ReporteModel.id)
    ).group_by(ReporteModel.tipo).all()
    reportes_por_tipo = dict(reportes_por_tipo)

    # Reportes por formato
    reportes_por_formato = query.with_entities(
        ReporteModel.formato,
        func.count(ReporteModel.id)
    ).group_by(ReporteModel.formato).all()
    reportes_por_formato = dict(reportes_por_formato)

    # Reportes por estado
    reportes_por_estado = query.with_entities(
        ReporteModel.estado,
        func.count(ReporteModel.id)
    ).group_by(ReporteModel.estado).all()
    reportes_por_estado = dict(reportes_por_estado)

    # Reportes por usuario
    reportes_por_usuario = query.join(Usuario).with_entities(
        Usuario.nombre,
        func.count(ReporteModel.id)
    ).group_by(Usuario.nombre).all()
    reportes_por_usuario = dict(reportes_por_usuario)

    # Reportes por estado específico
    reportes_pendientes = query.filter(ReporteModel.estado == EstadoReporte.PENDIENTE).count()
    reportes_procesando = query.filter(ReporteModel.estado == EstadoReporte.PROCESANDO).count()
    reportes_completados = query.filter(ReporteModel.estado == EstadoReporte.COMPLETADO).count()
    reportes_error = query.filter(ReporteModel.estado == EstadoReporte.ERROR).count()

    # Promedio de tiempo de procesamiento
    reportes_completados_tiempo = query.filter(
        ReporteModel.estado == EstadoReporte.COMPLETADO,
        ReporteModel.fecha_completado != None
    ).all()
    
    if reportes_completados_tiempo:
        tiempo_total = sum(
            (r.fecha_completado - r.fecha_creacion).total_seconds() / 60
            for r in reportes_completados_tiempo
        )
        promedio_tiempo = tiempo_total / len(reportes_completados_tiempo)
    else:
        promedio_tiempo = 0

    # Reportes del último mes
    un_mes_atras = datetime.utcnow() - timedelta(days=30)
    reportes_ultimo_mes = query.filter(ReporteModel.fecha_creacion >= un_mes_atras).count()

    return ReporteEstadisticas(
        total_reportes=total_reportes,
        reportes_por_tipo=reportes_por_tipo,
        reportes_por_formato=reportes_por_formato,
        reportes_por_estado=reportes_por_estado,
        reportes_por_usuario=reportes_por_usuario,
        reportes_pendientes=reportes_pendientes,
        reportes_procesando=reportes_procesando,
        reportes_completados=reportes_completados,
        reportes_error=reportes_error,
        promedio_tiempo_procesamiento=promedio_tiempo,
        reportes_ultimo_mes=reportes_ultimo_mes
    ) 