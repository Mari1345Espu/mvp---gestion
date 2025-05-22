from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.controladores import (
    usuario, rol, proyecto, 
    recurso, avance, 
    producto, tarea, estado, tipo_estado, lineainvestigacion, 
    anexo, cierre, destino, extension, auditoria, evaluacion, 
    facultad, programa, impacto, notificacion, reporte,
    auth, dashboard
)
from app.db.session import get_db
from app import modelos
from app.core.seguridad import get_current_user
from fastapi.responses import JSONResponse
from .config import settings
from .utilidades.logging import setup_logging, RequestLogger
from .utilidades.monitoring import setup_monitoring
from .database import engine
from app.config import get_config
from app.db.base import Base

# Configurar logging
setup_logging()

# Obtener la configuración
config = get_config()

# Crear aplicación
app = FastAPI(
    title="API de Gestión",
    description="API para el sistema de gestión de extensiones",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middleware de logging
app.add_middleware(RequestLogger)

# Configurar monitoreo
db_monitor = setup_monitoring(app, engine)

# Incluir rutas
app.include_router(auth.router, prefix="/api/v1", tags=["Autenticación"])
app.include_router(usuario.router, prefix="/api/v1", tags=["Usuarios"])
app.include_router(rol.router, prefix="/api/v1", tags=["Roles"])
app.include_router(estado.router, prefix="/api/v1", tags=["Estados"])
app.include_router(proyecto.router, prefix="/api/v1", tags=["Proyectos"])
app.include_router(recurso.router, prefix="/api/v1", tags=["Recursos"])
app.include_router(avance.router, prefix="/api/v1", tags=["Avances"])
app.include_router(producto.router, prefix="/api/v1", tags=["Productos"])
app.include_router(tarea.router, prefix="/api/v1", tags=["Tareas"])
app.include_router(tipo_estado.router, prefix="/api/v1", tags=["Tipos de Estado"])
app.include_router(lineainvestigacion.router, prefix="/api/v1", tags=["Líneas de Investigación"])
app.include_router(anexo.router, prefix="/api/v1", tags=["Anexos"])
app.include_router(cierre.router, prefix="/api/v1", tags=["Cierres"])
app.include_router(destino.router, prefix="/api/v1", tags=["Destinos"])
app.include_router(extension.router, prefix="/api/v1", tags=["Extensiones"])
app.include_router(auditoria.router, prefix="/api/v1", tags=["Auditoría"])
app.include_router(evaluacion.router, prefix="/api/v1", tags=["Evaluación"])
app.include_router(facultad.router, prefix="/api/v1", tags=["Facultades"])
app.include_router(programa.router, prefix="/api/v1", tags=["Programas"])
app.include_router(impacto.router, prefix="/api/v1", tags=["Impactos"])
app.include_router(notificacion.router, prefix="/api/v1", tags=["Notificaciones"])
app.include_router(reporte.router, prefix="/api/v1", tags=["Reportes"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])

@app.get("/")
async def root():
    """Endpoint de salud."""
    return {
        "status": "ok",
        "version": "1.0.0"
    }

@app.get("/api/v1/dashboard")
async def get_dashboard_data(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Obtener conteos
        usuarios_count = db.query(modelos.Usuario).count()
        roles_count = db.query(modelos.Rol).count()
        grupos_count = db.query(modelos.GrupoInvestigacion).count()
        proyectos_count = db.query(modelos.Proyecto).count()
        convocatorias_count = db.query(modelos.Convocatoria).count()
        
        # Obtener convocatorias recientes
        convocatorias_recientes = db.query(modelos.Convocatoria).order_by(modelos.Convocatoria.fecha_creacion.desc()).limit(5).all()
        
        # Obtener proyectos recientes
        proyectos_recientes = db.query(modelos.Proyecto).order_by(modelos.Proyecto.fecha_creacion.desc()).limit(5).all()
        
        return {
            "stats": {
                "usuarios": usuarios_count,
                "roles": roles_count,
                "grupos": grupos_count,
                "proyectos": proyectos_count,
                "convocatorias": convocatorias_count
            },
            "recientes": {
                "convocatorias": convocatorias_recientes,
                "proyectos": proyectos_recientes
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error al obtener datos del dashboard: {str(e)}"}
        )

# Crear las tablas en el orden correcto
def init_db():
    # Primero las tablas base sin dependencias
    Base.metadata.create_all(bind=engine, tables=[modelos.Rol.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Estado.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.TipoEstado.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Facultad.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Programa.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.LineaInvestigacion.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.GrupoInvestigacion.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.TipoProyecto.__table__])
    
    # Luego las tablas con dependencias simples
    Base.metadata.create_all(bind=engine, tables=[modelos.Usuario.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Proyecto.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Tarea.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Avance.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Recurso.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Producto.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Anexo.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Auditoria.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Notificacion.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Reporte.__table__])
    
    # Finalmente las tablas con múltiples dependencias
    Base.metadata.create_all(bind=engine, tables=[modelos.Cierre.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Evaluacion.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Destino.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Extension.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Impacto.__table__])
    Base.metadata.create_all(bind=engine, tables=[modelos.Seguimiento.__table__])

# Inicializar la base de datos
init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

