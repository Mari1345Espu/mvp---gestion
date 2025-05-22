import { hash } from 'bcryptjs';

export const roles = [
  {
    id: 1,
    nombre: 'admin',
    descripcion: 'Administrador del sistema',
  },
  {
    id: 2,
    nombre: 'investigador',
    descripcion: 'Investigador del sistema',
  },
  {
    id: 3,
    nombre: 'evaluador_interno',
    descripcion: 'Evaluador interno de proyectos',
  },
  {
    id: 4,
    nombre: 'evaluador_externo',
    descripcion: 'Evaluador externo de proyectos',
  },
  {
    id: 5,
    nombre: 'lider_grupo',
    descripcion: 'Líder de grupo de investigación',
  },
];

export const estados = [
  {
    id: 1,
    nombre: 'activo',
    descripcion: 'Estado activo',
    color: '#4CAF50',
  },
  {
    id: 2,
    nombre: 'inactivo',
    descripcion: 'Estado inactivo',
    color: '#9E9E9E',
  },
  {
    id: 3,
    nombre: 'pendiente',
    descripcion: 'Estado pendiente',
    color: '#FFC107',
  },
  {
    id: 4,
    nombre: 'en_revision',
    descripcion: 'En revisión',
    color: '#2196F3',
  },
  {
    id: 5,
    nombre: 'aprobado',
    descripcion: 'Aprobado',
    color: '#4CAF50',
  },
  {
    id: 6,
    nombre: 'rechazado',
    descripcion: 'Rechazado',
    color: '#F44336',
  },
];

export const getUsers = async () => {
  const password = await hash('password123', 10);
  
  return [
    {
      nombre: 'Admin User',
      email: 'admin@example.com',
      password,
      rol_id: 1,
      estado_id: 1,
      activo: true,
      fecha_registro: new Date().toISOString(),
      ultima_sesion: new Date().toISOString(),
    },
    {
      nombre: 'Investigador User',
      email: 'investigador@example.com',
      password,
      rol_id: 2,
      estado_id: 1,
      activo: true,
      fecha_registro: new Date().toISOString(),
      ultima_sesion: new Date().toISOString(),
    },
    {
      nombre: 'Evaluador Interno User',
      email: 'evaluador.interno@example.com',
      password,
      rol_id: 3,
      estado_id: 1,
      activo: true,
      fecha_registro: new Date().toISOString(),
      ultima_sesion: new Date().toISOString(),
    },
    {
      nombre: 'Evaluador Externo User',
      email: 'evaluador.externo@example.com',
      password,
      rol_id: 4,
      estado_id: 1,
      activo: true,
      fecha_registro: new Date().toISOString(),
      ultima_sesion: new Date().toISOString(),
    },
    {
      nombre: 'Lider Grupo User',
      email: 'lider.grupo@example.com',
      password,
      rol_id: 5,
      estado_id: 1,
      activo: true,
      fecha_registro: new Date().toISOString(),
      ultima_sesion: new Date().toISOString(),
    },
  ];
};

export const programas = [
  {
    nombre: 'Programa de Investigación 1',
    descripcion: 'Descripción del programa de investigación 1',
    fechaInicio: new Date().toISOString(),
    fechaFin: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString(),
    estado: 'activo',
    estado_id: 1,
    responsable_id: 1,
  },
  {
    nombre: 'Programa de Investigación 2',
    descripcion: 'Descripción del programa de investigación 2',
    fechaInicio: new Date().toISOString(),
    fechaFin: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString(),
    estado: 'activo',
    estado_id: 1,
    responsable_id: 1,
  },
];

export const proyectos = [
  {
    nombre: 'Proyecto de Investigación 1',
    descripcion: 'Descripción del proyecto de investigación 1',
    fechaInicio: new Date().toISOString(),
    fechaFin: new Date(Date.now() + 180 * 24 * 60 * 60 * 1000).toISOString(),
    estado: 'activo',
    estado_id: 1,
    programa_id: 1,
    responsable_id: 2,
  },
  {
    nombre: 'Proyecto de Investigación 2',
    descripcion: 'Descripción del proyecto de investigación 2',
    fechaInicio: new Date().toISOString(),
    fechaFin: new Date(Date.now() + 180 * 24 * 60 * 60 * 1000).toISOString(),
    estado: 'en_revision',
    estado_id: 4,
    programa_id: 1,
    responsable_id: 2,
  },
  {
    nombre: 'Proyecto de Investigación 3',
    descripcion: 'Descripción del proyecto de investigación 3',
    fechaInicio: new Date().toISOString(),
    fechaFin: new Date(Date.now() + 180 * 24 * 60 * 60 * 1000).toISOString(),
    estado: 'pendiente',
    estado_id: 3,
    programa_id: 2,
    responsable_id: 2,
  },
];

export const gruposInvestigacion = [
  {
    nombre: 'Grupo de Investigación 1',
    descripcion: 'Descripción del grupo de investigación 1',
    fecha_creacion: new Date().toISOString(),
    lider_id: 5,
  },
  {
    nombre: 'Grupo de Investigación 2',
    descripcion: 'Descripción del grupo de investigación 2',
    fecha_creacion: new Date().toISOString(),
    lider_id: 5,
  },
];

export const reportes = [
  {
    titulo: 'Reporte de Avance 1',
    descripcion: 'Descripción del reporte de avance 1',
    estado_id: 1,
    tipo: 'avance',
    usuario_id: 2,
    proyecto_id: 1,
    fecha_creacion: new Date().toISOString(),
    fecha_actualizacion: new Date().toISOString(),
  },
  {
    titulo: 'Reporte Final 1',
    descripcion: 'Descripción del reporte final 1',
    estado_id: 4,
    tipo: 'final',
    usuario_id: 2,
    proyecto_id: 1,
    fecha_creacion: new Date().toISOString(),
    fecha_actualizacion: new Date().toISOString(),
  },
]; 