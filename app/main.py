from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.controladores import (
    conceptoevaluacion, grupoinvestigacion, usuario, rol, proyecto, 
    cronograma, autentificacion, recurso, participante, avance, 
    producto, tarea, estado, tipo_estado, lineainvestigacion, 
    anexo, cierre, destino, extension, auditoria, evaluacion, 
    facultad, programa, impacto, notificacion, reporte
)
from app.db.session import get_db
from app import modelos
from app.core.seguridad import get_current_user
from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:3000/",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de templates y archivos estáticos
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inclusión de routers
app.include_router(usuario.router, prefix="/api/v1")
app.include_router(rol.router, prefix="/api/v1")
app.include_router(proyecto.router, prefix="/api/v1")
app.include_router(cronograma.router, prefix="/api/v1")
app.include_router(autentificacion.router, prefix="/api/v1")
app.include_router(recurso.router, prefix="/api/v1")
app.include_router(participante.router, prefix="/api/v1")
app.include_router(avance.router, prefix="/api/v1")
app.include_router(producto.router, prefix="/api/v1")
app.include_router(tarea.router, prefix="/api/v1")
app.include_router(conceptoevaluacion.router, prefix="/api/v1")
app.include_router(estado.router, prefix="/api/v1")
app.include_router(tipo_estado.router, prefix="/api/v1")
app.include_router(grupoinvestigacion.router, prefix="/api/v1")
app.include_router(lineainvestigacion.router, prefix="/api/v1")
app.include_router(anexo.router, prefix="/api/v1")
app.include_router(cierre.router, prefix="/api/v1")
app.include_router(destino.router, prefix="/api/v1")
app.include_router(extension.router, prefix="/api/v1")
app.include_router(auditoria.router, prefix="/api/v1")
app.include_router(evaluacion.router, prefix="/api/v1")
app.include_router(facultad.router, prefix="/api/v1")
app.include_router(programa.router, prefix="/api/v1")
app.include_router(impacto.router, prefix="/api/v1")
app.include_router(notificacion.router, prefix="/api/v1")
app.include_router(reporte.router, prefix="/api/v1")

@app.get("/")
async def leer_raiz(request: Request, db: Session = Depends(get_db)):
    # Obtener datos para los filtros
    convocatorias = db.query(modelos.Convocatoria).all()
    programas = db.query(modelos.Programa).all()
    proyectos = db.query(modelos.Proyecto).join(modelos.Estado).filter(modelos.Estado.nombre == "Finalizado").all()
    tipos = db.query(modelos.TipoProyecto).all()
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "convocatorias": convocatorias,
            "programas": programas,
            "proyectos": proyectos,
            "tipos": tipos,
            "current_user": None
        }
    )

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request, "current_user": None})

@app.get("/registro")
async def registro(request: Request):
    return templates.TemplateResponse("auth/registro.html", {"request": request, "current_user": None})

@app.get("/recuperar-password")
async def recuperar_password(request: Request):
    return templates.TemplateResponse("auth/recuperar_password.html", {"request": request, "current_user": None})

@app.get("/admin/usuarios", response_class=HTMLResponse)
async def admin_usuarios(request: Request, current_user=Depends(get_current_user)):
    if request.headers.get('authorization'):
        return templates.get_template("admin/usuarios.html").render({"request": request, "current_user": current_user})
    else:
        return templates.TemplateResponse("protected_view.html", {"request": request})

@app.get("/admin/proyectos", response_class=HTMLResponse)
async def admin_proyectos(request: Request, current_user=Depends(get_current_user)):
    if request.headers.get('authorization'):
        return templates.get_template("admin/proyectos.html").render({"request": request, "current_user": current_user})
    else:
        return templates.TemplateResponse("protected_view.html", {"request": request})

@app.get("/admin/convocatorias", response_class=HTMLResponse)
async def admin_convocatorias(request: Request, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if request.headers.get('authorization'):
        convocatorias = db.query(modelos.Convocatoria).all()
        total_convocatorias = len(convocatorias)
        abiertas = len([c for c in convocatorias if c.estado and c.estado.nombre.lower() == 'abierta'])
        cerradas = len([c for c in convocatorias if c.estado and c.estado.nombre.lower() == 'cerrada'])
        estados = db.query(modelos.Estado).all()
        return templates.TemplateResponse("admin/convocatorias.html", {
            "request": request,
            "current_user": current_user,
            "convocatorias": convocatorias,
            "total_convocatorias": total_convocatorias,
            "abiertas": abiertas,
            "cerradas": cerradas,
            "estados": estados
        })
    else:
        return templates.TemplateResponse("protected_view.html", {"request": request})

@app.get("/perfil")
async def perfil(request: Request, current_user=Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("perfil.html", {"request": request, "current_user": current_user})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user=Depends(get_current_user)):
    import inspect
    # Detectar si la petición viene de fetch (tiene header Authorization)
    if request.headers.get('authorization'):
        rol = current_user.rol.nombre.lower()
        if rol == "administrador cti":
            return templates.get_template("admin/dashboard_admin.html").render({"request": request, "current_user": current_user})
        elif rol == "asesor":
            return templates.get_template("asesor/dashboard.html").render({"request": request, "current_user": current_user})
        elif rol == "evaluador":
            return templates.get_template("evaluador/dashboard.html").render({"request": request, "current_user": current_user})
        elif rol == "líder":
            return templates.get_template("lider/dashboard.html").render({"request": request, "current_user": current_user})
        elif rol == "investigador":
            return templates.get_template("investigador/dashboard.html").render({"request": request, "current_user": current_user})
        else:
            return "<p>Rol no reconocido</p>"
    else:
        # Si no es AJAX, redirige a la plantilla dashboard.html (que tiene el JS para cargar el dashboard)
        return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/admin/dashboard")
async def admin_dashboard_redirect():
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard.html")
async def dashboard_html(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/admin/usuarios.html")
async def usuarios_html(request: Request):
    return templates.TemplateResponse("protected_view.html", {"request": request})

@app.get("/admin/proyectos.html")
async def proyectos_html(request: Request):
    return templates.TemplateResponse("protected_view.html", {"request": request})

@app.get("/admin/convocatorias.html")
async def convocatorias_html(request: Request):
    return templates.TemplateResponse("protected_view.html", {"request": request})

