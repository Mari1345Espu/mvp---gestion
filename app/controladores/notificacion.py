from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app import modelos
from app.db.session import get_db
from app.core.seguridad import get_current_user
from app.core.email import send_notification_email

from app.esquemas.notificacion import NotificacionBase, NotificacionCreate, Notificacion

router = APIRouter()

@router.get("/notificaciones/", response_model=List[Notificacion])
async def leer_notificaciones(
    skip: int = 0,
    limit: int = 100,
    leida: Optional[bool] = None,
    tipo: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    """Obtiene las notificaciones del usuario actual"""
    query = db.query(modelos.Notificacion).filter(
        modelos.Notificacion.usuario_id == current_user.id
    )
    
    if leida is not None:
        query = query.filter(modelos.Notificacion.leida == leida)
    if tipo:
        query = query.filter(modelos.Notificacion.tipo == tipo)
        
    notificaciones = query.order_by(
        modelos.Notificacion.fecha_creacion.desc()
    ).offset(skip).limit(limit).all()
    
    return notificaciones

@router.get("/notificaciones/{notificacion_id}", response_model=Notificacion)
def leer_notificacion(notificacion_id: int, db: Session = Depends(get_db)):
    notificacion = db.query(modelos.Notificacion).filter(modelos.Notificacion.id == notificacion_id).first()
    if notificacion is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return notificacion

@router.post("/notificaciones/", response_model=Notificacion)
def crear_notificacion(notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    db_notificacion = modelos.Notificacion(**notificacion.dict())
    db.add(db_notificacion)
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion

@router.put("/notificaciones/{notificacion_id}", response_model=Notificacion)
def actualizar_notificacion(notificacion_id: int, notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    db_notificacion = db.query(modelos.Notificacion).filter(modelos.Notificacion.id == notificacion_id).first()
    if db_notificacion is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    for key, value in notificacion.dict().items():
        setattr(db_notificacion, key, value)
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion

@router.delete("/notificaciones/{notificacion_id}", response_model=Notificacion)
def eliminar_notificacion(notificacion_id: int, db: Session = Depends(get_db)):
    db_notificacion = db.query(modelos.Notificacion).filter(modelos.Notificacion.id == notificacion_id).first()
    if db_notificacion is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    db.delete(db_notificacion)
    db.commit()
    return db_notificacion

@router.post("/notificaciones/marcar-leida/{notificacion_id}")
async def marcar_notificacion_leida(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    """Marca una notificación como leída"""
    notificacion = db.query(modelos.Notificacion).filter(
        modelos.Notificacion.id == notificacion_id,
        modelos.Notificacion.usuario_id == current_user.id
    ).first()
    
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    
    notificacion.leida = True
    notificacion.fecha_lectura = datetime.now()
    db.commit()
    
    return {"message": "Notificación marcada como leída"}

@router.post("/notificaciones/marcar-todas-leidas")
async def marcar_todas_leidas(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    """Marca todas las notificaciones del usuario como leídas"""
    db.query(modelos.Notificacion).filter(
        modelos.Notificacion.usuario_id == current_user.id,
        modelos.Notificacion.leida == False
    ).update({
        "leida": True,
        "fecha_lectura": datetime.now()
    })
    db.commit()
    
    return {"message": "Todas las notificaciones han sido marcadas como leídas"}

async def crear_notificacion_proyecto(
    db: Session,
    proyecto_id: int,
    tipo: str,
    mensaje: str,
    usuarios: List[modelos.Usuario]
):
    """Crea notificaciones para múltiples usuarios sobre un proyecto"""
    notificaciones = []
    for usuario in usuarios:
        notificacion = modelos.Notificacion(
            usuario_id=usuario.id,
            proyecto_id=proyecto_id,
            tipo=tipo,
            mensaje=mensaje,
            fecha_creacion=datetime.now()
        )
        notificaciones.append(notificacion)
        
        # Enviar correo electrónico
        await send_notification_email(
            email=usuario.correo,
            subject=f"Nueva notificación: {tipo}",
            message=mensaje
        )
    
    db.add_all(notificaciones)
    db.commit()
    
    return notificaciones

@router.get("/notificaciones/no-leidas/count")
async def contar_notificaciones_no_leidas(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    """Cuenta las notificaciones no leídas del usuario"""
    count = db.query(modelos.Notificacion).filter(
        modelos.Notificacion.usuario_id == current_user.id,
        modelos.Notificacion.leida == False
    ).count()
    
    return {"count": count}
