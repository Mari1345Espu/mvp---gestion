from app.esquemas.proyecto import Proyecto, ProyectoCreate, ProyectoBase
from app.esquemas.usuario import Usuario, UsuarioCreate, UsuarioBase
from app.esquemas.rol import Rol, RolCreate, RolBase
from app.esquemas.cronograma import Cronograma, CronogramaCreate, CronogramaBase
from app.esquemas.recurso import Recurso, RecursoCreate, RecursoBase
from app.esquemas.participante import Participante, ParticipanteCreate, ParticipanteBase
from app.esquemas.avance import Avance, AvanceCreate, AvanceBase
from app.esquemas.producto import Producto, ProductoCreate, ProductoBase
from app.esquemas.tarea import Tarea, TareaCreate, TareaBase
from app.esquemas.estado import Estado, EstadoCreate, EstadoBase
from app.esquemas.conceptoevaluacion import ConceptoEvaluacion, ConceptoEvaluacionCreate, ConceptoEvaluacionBase
from app.esquemas.tipo_estado import TipoEstado, TipoEstadoCreate, TipoEstadoBase
from app.esquemas.grupoinvestigacion import GrupoInvestigacion, GrupoInvestigacionCreate, GrupoInvestigacionBase
from app.esquemas.lineainvestigacion import LineaInvestigacion, LineaInvestigacionCreate, LineaInvestigacionBase
from app.esquemas.anexo import Anexo, AnexoCreate, AnexoBase
from app.esquemas.auditoria import Auditoria, AuditoriaCreate, AuditoriaBase
from app.esquemas.cierre import Cierre, CierreCreate, CierreBase
from app.esquemas.destino import Destino, DestinoCreate, DestinoBase
from app.esquemas.evaluacion import Evaluacion, EvaluacionCreate, EvaluacionBase
from app.esquemas.extension import Extension, ExtensionCreate, ExtensionBase
from app.esquemas.facultad import Facultad, FacultadCreate, FacultadBase
from app.esquemas.programa import Programa, ProgramaCreate, ProgramaBase
from app.esquemas.impacto import Impacto, ImpactoCreate, ImpactoBase
from app.esquemas.tipo_proyecto import TipoProyecto, TipoProyectoCreate, TipoProyectoBase
from app.esquemas.seguimiento import Seguimiento, SeguimientoCreate, SeguimientoBase
from app.esquemas.convocatoria import Convocatoria, ConvocatoriaCreate, ConvocatoriaBase

from .proyecto import router as proyecto_router
from .usuario import router as usuario_router
from .rol import router as rol_router
from .facultad import router as facultad_router
from .estado import router as estado_router
from .convocatoria import router as convocatoria_router
from .producto import router as producto_router
from .recurso import router as recurso_router
from .auth import router as auth_router
from .avance import router as avance_router
from .tarea import router as tarea_router
from .tipo_estado import router as tipo_estado_router
from .lineainvestigacion import router as lineainvestigacion_router
from .anexo import router as anexo_router
from .cierre import router as cierre_router
from .destino import router as destino_router
from .extension import router as extension_router
from .auditoria import router as auditoria_router
from .evaluacion import router as evaluacion_router
from .programa import router as programa_router
from .impacto import router as impacto_router
from .notificacion import router as notificacion_router
from .reporte import router as reporte_router

routers = [
    proyecto_router,
    usuario_router,
    rol_router,
    facultad_router,
    estado_router,
    convocatoria_router,
    producto_router,
    recurso_router,
    auth_router,
    avance_router,
    tarea_router,
    tipo_estado_router,
    lineainvestigacion_router,
    anexo_router,
    cierre_router,
    destino_router,
    extension_router,
    auditoria_router,
    evaluacion_router,
    programa_router,
    impacto_router,
    notificacion_router,
    reporte_router
]
