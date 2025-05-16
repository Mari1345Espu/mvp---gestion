from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controladores import conceptoevaluacion, grupoinvestigacion, usuario, rol, proyecto, cronograma, autentificacion, recurso, participante, avance, producto, tarea, estado, tipo_estado, lineainvestigacion, anexo, cierre, destino, extension, auditoria, evaluacion, facultad, programa, impacto



app = FastAPI()

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
app.include_router(programa.router, prefix="/api/v1")

@app.get("/")
def leer_raiz():
    return {"Hola": "Mundo"}

