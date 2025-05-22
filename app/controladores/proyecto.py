from fastapi import APIRouter, Depends, HTTPException, Query, Request, Form, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta, date
from fastapi.responses import JSONResponse

from app import modelos
from app.db.session import get_db
from app.core.seguridad import get_current_user
from app.esquemas.proyecto import Proyecto as ProyectoSchema, ProyectoCreate, ProyectoUpdate, DashboardResponse, ReporteProyecto, ProyectoFiltro, ProyectoEstadisticas

router = APIRouter(
    prefix="/proyectos",
    tags=["proyectos"]
)

@router.get("/", response_model=List[ProyectoSchema])
def read_proyectos(
    skip: int = 0,
    limit: int = 100,
    estado_id: Optional[int] = None,
    grupo_id: Optional[int] = None,
    linea_id: Optional[int] = None,
    convocatoria_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    query = db.query(modelos.Proyecto)
    
    if estado_id:
        query = query.filter(modelos.Proyecto.estado_id == estado_id)
    if grupo_id:
        query = query.filter(modelos.Proyecto.grupo_investigacion_id == grupo_id)
    if linea_id:
        query = query.filter(modelos.Proyecto.linea_investigacion_id == linea_id)
    if convocatoria_id:
        query = query.filter(modelos.Proyecto.convocatoria_id == convocatoria_id)
    if fecha_inicio and fecha_fin:
        query = query.filter(
            and_(
                modelos.Proyecto.fecha_inicio >= fecha_inicio,
                modelos.Proyecto.fecha_inicio <= fecha_fin
            )
        )
    if search:
        query = query.filter(
            or_(
                modelos.Proyecto.titulo.ilike(f"%{search}%"),
                modelos.Proyecto.objetivos.ilike(f"%{search}%"),
                modelos.Proyecto.palabras_clave.ilike(f"%{search}%")
            )
        )
    
    proyectos = query.offset(skip).limit(limit).all()
    return proyectos

@router.get("/{proyecto_id}", response_model=ProyectoSchema)
def read_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto

@router.post("/", response_model=ProyectoSchema)
def create_proyecto(
    proyecto: ProyectoCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    # Verificar que el usuario tenga permisos para crear proyectos
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear proyectos"
        )
    
    db_proyecto = modelos.Proyecto(**proyecto.dict())
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.put("/{proyecto_id}", response_model=ProyectoSchema)
def update_proyecto(
    proyecto_id: int,
    proyecto: ProyectoUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Verificar permisos
    if current_user.rol.nombre not in ["Admin", "Investigador"] and current_user.id != db_proyecto.asesor_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar este proyecto"
        )
    
    for key, value in proyecto.dict(exclude_unset=True).items():
        setattr(db_proyecto, key, value)
    
    db_proyecto.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.delete("/{proyecto_id}", response_model=ProyectoSchema)
def delete_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar proyectos"
        )
    
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    db.delete(db_proyecto)
    db.commit()
    return db_proyecto

@router.get("/estadisticas/", response_model=ProyectoEstadisticas)
def get_estadisticas_proyectos(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de proyectos
    total_proyectos = db.query(func.count(modelos.Proyecto.id)).scalar()
    
    # Proyectos activos y finalizados
    proyectos_activos = db.query(func.count(modelos.Proyecto.id)).filter(
        modelos.Proyecto.estado_id == 1  # Asumiendo que 1 es el ID del estado "Activo"
    ).scalar()
    
    proyectos_finalizados = db.query(func.count(modelos.Proyecto.id)).filter(
        modelos.Proyecto.estado_id == 2  # Asumiendo que 2 es el ID del estado "Finalizado"
    ).scalar()
    
    # Proyectos por estado
    proyectos_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.Proyecto.id)
        ).join(modelos.Proyecto).group_by(modelos.Estado.nombre).all()
    )
    
    # Proyectos por grupo de investigación
    proyectos_por_grupo = dict(
        db.query(
            modelos.GrupoInvestigacion.nombre,
            func.count(modelos.Proyecto.id)
        ).join(modelos.Proyecto).group_by(modelos.GrupoInvestigacion.nombre).all()
    )
    
    # Proyectos por línea de investigación
    proyectos_por_linea = dict(
        db.query(
            modelos.LineaInvestigacion.nombre,
            func.count(modelos.Proyecto.id)
        ).join(modelos.Proyecto).group_by(modelos.LineaInvestigacion.nombre).all()
    )
    
    # Promedio de avance
    promedio_avance = db.query(func.avg(modelos.Proyecto.porcentaje_avance)).scalar() or 0
    
    # Total de presupuesto
    total_presupuesto = db.query(func.sum(modelos.Proyecto.presupuesto)).scalar() or 0
    
    # Presupuesto por grupo
    presupuesto_por_grupo = dict(
        db.query(
            modelos.GrupoInvestigacion.nombre,
            func.sum(modelos.Proyecto.presupuesto)
        ).join(modelos.Proyecto).group_by(modelos.GrupoInvestigacion.nombre).all()
    )
    
    return ProyectoEstadisticas(
        total_proyectos=total_proyectos,
        proyectos_activos=proyectos_activos,
        proyectos_finalizados=proyectos_finalizados,
        proyectos_por_estado=proyectos_por_estado,
        proyectos_por_grupo=proyectos_por_grupo,
        proyectos_por_linea=proyectos_por_linea,
        promedio_avance=promedio_avance,
        total_presupuesto=total_presupuesto,
        presupuesto_por_grupo=presupuesto_por_grupo
    )

@router.put("/{proyecto_id}/asignar-evaluador", response_model=ProyectoSchema)
def asignar_evaluador(
    proyecto_id: int,
    evaluador_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden asignar evaluadores"
        )
    
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Verificar que el evaluador existe y tiene el rol correcto
    evaluador = db.query(modelos.Usuario).filter(
        and_(
            modelos.Usuario.id == evaluador_id,
            modelos.Usuario.rol_id == 3  # Asumiendo que 3 es el ID del rol "Evaluador"
        )
    ).first()
    
    if not evaluador:
        raise HTTPException(status_code=404, detail="Evaluador no encontrado o no tiene el rol correcto")
    
    db_proyecto.evaluador_externo_id = evaluador_id
    db_proyecto.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.put("/{proyecto_id}/asignar-asesor", response_model=ProyectoSchema)
def asignar_asesor(
    proyecto_id: int,
    asesor_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden asignar asesores"
        )
    
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Verificar que el asesor existe y tiene el rol correcto
    asesor = db.query(modelos.Usuario).filter(
        and_(
            modelos.Usuario.id == asesor_id,
            modelos.Usuario.rol_id == 4  # Asumiendo que 4 es el ID del rol "Asesor"
        )
    ).first()
    
    if not asesor:
        raise HTTPException(status_code=404, detail="Asesor no encontrado o no tiene el rol correcto")
    
    db_proyecto.asesor_id = asesor_id
    db_proyecto.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.put("/{proyecto_id}/actualizar-estado", response_model=ProyectoSchema)
def actualizar_estado_proyecto(
    proyecto_id: int,
    estado_id: int,
    tipo_estado_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Evaluador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar el estado del proyecto"
        )
    
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Verificar que el estado y tipo de estado existen
    estado = db.query(modelos.Estado).filter(modelos.Estado.id == estado_id).first()
    tipo_estado = db.query(modelos.TipoEstado).filter(modelos.TipoEstado.id == tipo_estado_id).first()
    
    if not estado or not tipo_estado:
        raise HTTPException(status_code=404, detail="Estado o tipo de estado no encontrado")
    
    db_proyecto.estado_id = estado_id
    db_proyecto.tipo_estado_id = tipo_estado_id
    db_proyecto.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

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

@router.post("/", response_model=ProyectoSchema)
def crear_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    db_proyecto = modelos.Proyecto(**proyecto.dict())
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.get("/", response_model=List[ProyectoSchema])
def listar_proyectos(
    filtro: ProyectoFiltro = Depends(),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(modelos.Proyecto)
    
    if filtro.convocatoria_id:
        query = query.filter(modelos.Proyecto.convocatoria_id == filtro.convocatoria_id)
    if filtro.estado_id:
        query = query.filter(modelos.Proyecto.estado_id == filtro.estado_id)
    if filtro.tipo_proyecto_id:
        query = query.filter(modelos.Proyecto.tipo_proyecto_id == filtro.tipo_proyecto_id)
    if filtro.extension_id:
        query = query.filter(modelos.Proyecto.extension_id == filtro.extension_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{proyecto_id}", response_model=ProyectoSchema)
def obtener_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto

@router.put("/{proyecto_id}", response_model=ProyectoSchema)
def actualizar_proyecto(
    proyecto_id: int,
    proyecto: ProyectoCreate,
    db: Session = Depends(get_db)
):
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    for key, value in proyecto.dict().items():
        setattr(db_proyecto, key, value)
    
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.delete("/{proyecto_id}", response_model=ProyectoSchema)
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    db.delete(db_proyecto)
    db.commit()
    return {"mensaje": "Proyecto eliminado exitosamente"}
