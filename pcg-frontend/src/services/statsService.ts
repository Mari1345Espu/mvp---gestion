import api from './api';

export interface StatsResponse {
  total_proyectos: number;
  total_programas: number;
  total_usuarios: number;
  total_reportes: number;
  total_extensiones: number;
  proyectos_por_estado: {
    estado: string;
    cantidad: number;
  }[];
  programas_por_estado: {
    estado: string;
    cantidad: number;
  }[];
  usuarios_por_rol: {
    rol: string;
    cantidad: number;
  }[];
  reportes_por_tipo: {
    tipo: string;
    cantidad: number;
  }[];
  extensiones_por_tipo: {
    tipo: string;
    cantidad: number;
  }[];
  proyectos_por_programa: {
    programa: string;
    cantidad: number;
  }[];
  usuarios_por_programa: {
    programa: string;
    cantidad: number;
  }[];
  reportes_por_proyecto: {
    proyecto: string;
    cantidad: number;
  }[];
  extensiones_por_programa: {
    programa: string;
    cantidad: number;
  }[];
}

export const statsService = {
  async getStats(): Promise<StatsResponse> {
    const response = await api.get('/stats');
    return response.data;
  },

  async getProyectosStats(): Promise<StatsResponse['proyectos_por_estado']> {
    const response = await api.get('/stats/proyectos');
    return response.data;
  },

  async getProgramasStats(): Promise<StatsResponse['programas_por_estado']> {
    const response = await api.get('/stats/programas');
    return response.data;
  },

  async getUsuariosStats(): Promise<StatsResponse['usuarios_por_rol']> {
    const response = await api.get('/stats/usuarios');
    return response.data;
  },

  async getReportesStats(): Promise<StatsResponse['reportes_por_tipo']> {
    const response = await api.get('/stats/reportes');
    return response.data;
  },

  async getExtensionesStats(): Promise<StatsResponse['extensiones_por_tipo']> {
    const response = await api.get('/stats/extensiones');
    return response.data;
  },

  async getProyectosByProgramaStats(): Promise<StatsResponse['proyectos_por_programa']> {
    const response = await api.get('/stats/proyectos/programa');
    return response.data;
  },

  async getUsuariosByProgramaStats(): Promise<StatsResponse['usuarios_por_programa']> {
    const response = await api.get('/stats/usuarios/programa');
    return response.data;
  },

  async getReportesByProyectoStats(): Promise<StatsResponse['reportes_por_proyecto']> {
    const response = await api.get('/stats/reportes/proyecto');
    return response.data;
  },

  async getExtensionesByProgramaStats(): Promise<StatsResponse['extensiones_por_programa']> {
    const response = await api.get('/stats/extensiones/programa');
    return response.data;
  }
}; 