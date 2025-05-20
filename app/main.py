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
    auth
)
from app.db.session import get_db
from app import modelos
from app.core.seguridad import get_current_user
from fastapi.responses import JSONResponse

app = FastAPI(title="Sistema de Gestión de Investigación")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/")
async def root():
    return {"message": "API is running"}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

