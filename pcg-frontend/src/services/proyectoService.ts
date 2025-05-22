import api from './api';
import { Proyecto, PaginatedResponse, FiltrosProyecto } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

interface PaginationParams {
  page?: number;
  size?: number;
  sort?: string;
  order?: 'asc' | 'desc';
}

export const proyectoService = {
  async getProyectos(params?: FiltrosProyecto): Promise<PaginatedResponse<Proyecto>> {
    const response = await api.get('/proyectos', { params });
    return response.data;
  },

  async getProyecto(id: number): Promise<Proyecto> {
    const response = await api.get(`/proyectos/${id}`);
    return response.data;
  },

  async createProyecto(proyecto: Omit<Proyecto, 'id' | 'created_at' | 'updated_at'>): Promise<Proyecto> {
    const response = await api.post('/proyectos', proyecto);
    return response.data;
  },

  async updateProyecto(id: number, proyecto: Partial<Proyecto>): Promise<Proyecto> {
    const response = await api.put(`/proyectos/${id}`, proyecto);
    return response.data;
  },

  async deleteProyecto(id: number): Promise<void> {
    await api.delete(`/proyectos/${id}`);
  },

  async getProyectosByLider(liderId: number): Promise<Proyecto[]> {
    const response = await api.get(`/proyectos/lider/${liderId}`);
    return response.data;
  },

  async getProyectosByInvestigador(investigadorId: number): Promise<Proyecto[]> {
    const response = await api.get(`/proyectos/investigador/${investigadorId}`);
    return response.data;
  },

  async getProyectosByEvaluador(evaluadorId: number): Promise<Proyecto[]> {
    const response = await api.get(`/proyectos/evaluador/${evaluadorId}`);
    return response.data;
  },

  async getProyectosByAsesor(asesorId: number): Promise<Proyecto[]> {
    const response = await api.get(`/proyectos/asesor/${asesorId}`);
    return response.data;
  }
};

export const getProyectos = async (page = 1, perPage = 10): Promise<PaginatedResponse<Proyecto>> => {
  return proyectoService.getProyectos(page, perPage);
};

export const getProyecto = async (id: number): Promise<Proyecto> => {
  return proyectoService.getProyecto(id);
};

export const getProyectosByPrograma = async (programaId: number): Promise<Proyecto[]> => {
  const response = await api.get<Proyecto[]>(`/proyectos/programa/${programaId}`);
  return response.data;
};

export const getProyectosByExtension = async (extensionId: number): Promise<Proyecto[]> => {
  const response = await api.get<Proyecto[]>(`/proyectos/extension/${extensionId}`);
  return response.data;
};

export const getProyectosByFacultad = async (facultadId: number): Promise<Proyecto[]> => {
  const response = await api.get<Proyecto[]>(`/proyectos/facultad/${facultadId}`);
  return response.data;
};

export const getProyectosByEstado = async (estado: string, params?: PaginationParams): Promise<PaginatedResponse<Proyecto>> => {
  const searchParams = new URLSearchParams();
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, value.toString());
      }
    });
  }
  const response = await api.get<PaginatedResponse<Proyecto>>(`/proyectos/estado/${estado}?${searchParams.toString()}`);
  return response.data;
};

export const getProyectosByFecha = async (fechaInicio: string, fechaFin: string, params?: PaginationParams): Promise<PaginatedResponse<Proyecto>> => {
  const response = await api.post<PaginatedResponse<Proyecto>>('/proyectos/fecha', {
    ...params,
    fecha_inicio: fechaInicio,
    fecha_fin: fechaFin,
  });
  return response.data;
};

export const getProyectosByResponsable = async (responsableId: number, params?: PaginationParams): Promise<PaginatedResponse<Proyecto>> => {
  const searchParams = new URLSearchParams();
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, value.toString());
      }
    });
  }
  const response = await api.get<PaginatedResponse<Proyecto>>(`/proyectos/responsable/${responsableId}?${searchParams.toString()}`);
  return response.data;
}; 