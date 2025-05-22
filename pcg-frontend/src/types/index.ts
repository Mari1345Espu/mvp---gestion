// Tipos de usuario
export interface User {
  id: number;
  nombre: string;
  apellido?: string;
  email: string;
  telefono?: string;
  rol: 'admin' | 'lider' | 'investigador' | 'evaluador_interno' | 'evaluador_externo' | 'asesor';
  rol_id: number;
  rol_nombre?: string;
  estado_id: number;
  activo: boolean;
  avatar_url?: string;
  foto?: string;
  correo?: string;
  fecha_registro?: string;
  ultima_sesion?: string;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  nombre: string;
  email: string;
  telefono: string;
  password: string;
  rol_id: number;
}

export interface UserUpdate {
  nombre?: string;
  email?: string;
  telefono?: string;
  password?: string;
  rol_id?: number;
  estado_id?: number;
}

// Tipos de autenticación
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  nombre: string;
  apellido?: string;
  email: string;
  password: string;
  telefono?: string;
  rol?: string;
  rol_id?: number;
  estado_id?: number;
  activo?: boolean;
  fecha_registro?: string;
  ultima_sesion?: string;
}

export interface PasswordChange {
  currentPassword: string;
  newPassword: string;
}

// Tipos de proyecto
export interface Proyecto {
  id: number;
  titulo: string;
  nombre?: string;
  descripcion: string;
  objetivo: string;
  metodologia: string;
  resultados_esperados: string;
  presupuesto: string;
  duracion: string;
  estado: 'borrador' | 'en_revision' | 'aprobado' | 'rechazado' | 'en_progreso' | 'completado';
  estado_id?: number;
  tipo_proyecto: 'investigacion' | 'desarrollo' | 'innovacion';
  area_conocimiento: string;
  palabras_clave: string;
  lider_id: number;
  responsable?: User;
  programa?: Programa;
  fechaInicio?: string;
  fechaFin?: string;
  imagen?: string;
  created_at: string;
  updated_at: string;
}

// Tipos de reporte
export interface Reporte {
  id: number;
  titulo: string;
  descripcion: string;
  estado_id: number;
  estado?: string;
  tipo?: string;
  usuario?: User;
  proyecto?: Proyecto;
  fecha_creacion: string;
  fecha_actualizacion: string;
}

// Tipos de grupo de investigación
export interface ResearchGroup {
  id: number;
  nombre: string;
  descripcion: string;
  fecha_creacion: string;
  lider_id: number;
}

// Tipos de convocatoria
export interface Convocatoria {
  id: number;
  titulo: string;
  descripcion: string;
  fecha_inicio: string;
  fecha_fin: string;
  estado: 'abierta' | 'cerrada' | 'cancelada';
  tipo: 'interna' | 'externa';
  requisitos: string[];
  documentos_requeridos: string[];
}

// Tipos de estado
export interface Estado {
  id: number;
  nombre: string;
  descripcion: string;
  color: string;
}

// Tipos de permiso
export interface Permiso {
  id: number;
  nombre: string;
  descripcion: string;
  codigo: string;
}

// Tipos de rol
export interface Rol {
  id: number;
  nombre: string;
  descripcion: string;
  permisos: Permiso[];
}

// Tipos de solicitud
export interface Solicitud {
  id: number;
  tipo: 'proyecto' | 'reporte' | 'convocatoria';
  estado: 'pendiente' | 'aprobada' | 'rechazada';
  fecha_creacion: string;
  fecha_actualizacion: string;
  usuario_id: number;
  usuario?: User;
  detalles: Record<string, any>;
}

// Tipos de notificación
export interface Notificacion {
  id: number;
  titulo: string;
  mensaje: string;
  tipo: 'info' | 'success' | 'warning' | 'error';
  fecha_creacion: string;
  fecha_lectura?: string;
  leida: boolean;
  usuario_id: number;
  usuario?: User;
  proyecto_id?: number;
  proyecto?: Proyecto;
  enlace?: string;
  prioridad: 'baja' | 'media' | 'alta';
}

// Tipos de respuesta de API
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  content: T[];
  total: number;
  totalElements: number;
  page: number;
  per_page: number;
  total_pages: number;
}

// Tipos de filtros
export interface FiltrosProyecto {
  estado?: string;
  programa?: number;
  responsable?: number;
  fechaInicio?: string;
  fechaFin?: string;
  page?: number;
  limit?: number;
}

export interface FiltrosReporte {
  titulo?: string;
  tipo?: string;
  autor_id?: number;
  fecha_inicio?: string;
  fecha_fin?: string;
}

export interface FiltrosConvocatoria {
  estado?: string;
  tipo?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}

// Tipos de Programa
export interface Programa {
  id: number;
  nombre: string;
  descripcion: string;
  fechaInicio: string;
  fechaFin: string;
  estado: string;
  estado_id: number;
  responsable: User;
  created_at: string;
  updated_at: string;
}

// Tipos de Extensión
export interface Extension {
  id: number;
  nombre: string;
  descripcion: string;
  tipo: 'curso' | 'diplomado' | 'certificado' | 'otro';
  duracion: number;
  modalidad: 'presencial' | 'virtual' | 'hibrido';
  programa_id: number;
  programa?: Programa;
  activo: boolean;
}

// Tipos de Avance
export interface Avance {
  id: number;
  proyecto_id: number;
  proyecto?: Proyecto;
  titulo: string;
  descripcion: string;
  fecha: string;
  porcentaje: number;
  estado: 'borrador' | 'en_revision' | 'aprobado' | 'rechazado';
  usuario_id: number;
  usuario?: User;
  observaciones?: string;
}

// Tipos de Anexo
export interface Anexo {
  id: number;
  nombre: string;
  descripcion: string;
  tipo: 'documento' | 'imagen' | 'video' | 'otro';
  url: string;
  proyecto_id: number;
  proyecto?: Proyecto;
  avance_id?: number;
  avance?: Avance;
  fecha_subida: string;
  usuario_id: number;
  usuario?: User;
}

// Tipos de filtros adicionales
export interface FiltrosAvance {
  proyecto_id?: number;
  usuario_id?: number;
  estado?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}

export interface FiltrosAnexo {
  proyecto_id?: number;
  avance_id?: number;
  tipo?: string;
  usuario_id?: number;
  fecha_inicio?: string;
  fecha_fin?: string;
}

// Tipos de Facultad
export interface Facultad {
  id: number;
  nombre: string;
  descripcion: string;
  codigo: string;
  decano_id: number;
  decano?: User;
  activo: boolean;
}

// Tipos de Recurso
export interface Recurso {
  id: number;
  nombre: string;
  descripcion: string;
  tipo: 'equipo' | 'material' | 'servicio' | 'otro';
  cantidad: number;
  unidad: string;
  costo_unitario: number;
  proyecto_id: number;
  proyecto?: Proyecto;
  proveedor?: string;
  fecha_adquisicion: string;
  estado: 'disponible' | 'en_uso' | 'mantenimiento' | 'baja';
}

// Tipos de Seguimiento
export interface Seguimiento {
  id: number;
  proyecto_id: number;
  proyecto?: Proyecto;
  fecha: string;
  tipo: 'revision' | 'evaluacion' | 'ajuste' | 'otro';
  descripcion: string;
  observaciones: string;
  recomendaciones: string;
  usuario_id: number;
  usuario?: User;
  estado: 'pendiente' | 'en_proceso' | 'completado';
}

// Tipos de Línea de Investigación
export interface LineaInvestigacion {
  id: number;
  nombre: string;
  descripcion: string;
  codigo: string;
  facultad_id: number;
  facultad?: Facultad;
  coordinador_id: number;
  coordinador?: User;
  fecha_creacion: string;
  activo: boolean;
}

// Tipos de filtros adicionales
export interface FiltrosRecurso {
  proyecto_id?: number;
  tipo?: string;
  estado?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}

export interface FiltrosSeguimiento {
  proyecto_id?: number;
  tipo?: string;
  estado?: string;
  usuario_id?: number;
  fecha_inicio?: string;
  fecha_fin?: string;
}

export interface FiltrosLineaInvestigacion {
  facultad_id?: number;
  coordinador_id?: number;
  activo?: boolean;
}

// Tipos de Cronograma
export interface Cronograma {
  id: number;
  proyecto_id: number;
  proyecto?: Proyecto;
  titulo: string;
  descripcion: string;
  fecha_inicio: string;
  fecha_fin: string;
  estado: 'pendiente' | 'en_progreso' | 'completado' | 'atrasado';
  responsable_id: number;
  responsable?: User;
  dependencias?: number[];
  porcentaje_avance: number;
}

// Tipos de Evaluación
export interface Evaluacion {
  id: number;
  proyecto_id: number;
  proyecto?: Proyecto;
  evaluador_id: number;
  evaluador?: User;
  fecha: string;
  tipo: 'inicial' | 'intermedia' | 'final';
  criterios: {
    nombre: string;
    puntaje: number;
    observaciones: string;
  }[];
  puntaje_total: number;
  observaciones_generales: string;
  recomendaciones: string;
  estado: 'borrador' | 'enviada' | 'aprobada' | 'rechazada';
}

// Tipos de Cierre
export interface Cierre {
  id: number;
  proyecto_id: number;
  proyecto?: Proyecto;
  fecha_cierre: string;
  tipo: 'parcial' | 'total';
  motivo: string;
  observaciones: string;
  documentos: string[];
  aprobado_por_id: number;
  aprobado_por?: User;
  estado: 'pendiente' | 'aprobado' | 'rechazado';
}

// Tipos de filtros adicionales
export interface FiltrosCronograma {
  proyecto_id?: number;
  responsable_id?: number;
  estado?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}

export interface FiltrosEvaluacion {
  proyecto_id?: number;
  evaluador_id?: number;
  tipo?: string;
  estado?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}

export interface FiltrosNotificacion {
  usuario_id?: number;
  tipo?: string;
  leida?: boolean;
  prioridad?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}

export interface FiltrosCierre {
  proyecto_id?: number;
  tipo?: string;
  estado?: string;
  aprobado_por_id?: number;
  fecha_inicio?: string;
  fecha_fin?: string;
}

// Tipos de Participante
export interface Participante {
  id: number;
  nombre: string;
  email: string;
  telefono: string;
  rol_id: number;
  estado_id: number;
  created_at: string;
  updated_at: string;
}

// Tipos de Concepto de Evaluación
export interface ConceptoEvaluacion {
  id: number;
  nombre: string;
  descripcion: string;
  tipo: 'proyecto' | 'extension' | 'programa' | 'general';
  criterios: {
    id: number;
    nombre: string;
    descripcion: string;
    peso: number;
    puntaje_maximo: number;
  }[];
  activo: boolean;
  fecha_creacion: string;
  fecha_actualizacion: string;
}

// Tipos de filtros adicionales
export interface FiltrosParticipante {
  proyecto_id?: number;
  usuario_id?: number;
  rol?: string;
  estado?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}

export interface FiltrosReporte {
  proyecto_id?: number;
  autor_id?: number;
  tipo?: string;
  estado?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}

export interface FiltrosConceptoEvaluacion {
  tipo?: string;
  activo?: boolean;
}

export interface FiltrosPrograma {
  estado?: string;
  responsable?: number;
  fechaInicio?: string;
  fechaFin?: string;
  page?: number;
  limit?: number;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface ApiError {
  message: string;
  status: number;
}

export interface PaginationParams {
  page?: number;
  per_page?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface FiltrosUsuario {
  rol?: string;
  estado?: string;
  search?: string;
  page?: number;
  limit?: number;
}

export interface FiltrosExtension {
  tipo?: string;
  modalidad?: string;
  programa?: number;
  activo?: boolean;
  page?: number;
  limit?: number;
} 