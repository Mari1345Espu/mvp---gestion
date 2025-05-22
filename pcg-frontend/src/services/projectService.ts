import axios from 'axios';
import axiosInstance from './axiosConfig';
import { Proyecto, PaginatedResponse, FiltrosProyecto } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export interface Project {
  id: number;
  titulo: string;
  objetivos: string;
  convocatoria_id: number;
  grupo_investigacion_id: number;
  linea_investigacion_id: number;
  extension_id: number;
  estado_id: number;
  fecha_inicio: string;
  evaluador_externo_id: number | null;
  convocatoria?: string;
  grupo_investigacion?: string;
  linea_investigacion?: string;
  extension?: string;
  estado?: string;
  evaluador_externo?: string;
}

export interface ProjectCreate {
  titulo: string;
  objetivos: string;
  convocatoria_id: number;
  grupo_investigacion_id: number;
  linea_investigacion_id: number;
  extension_id: number;
  estado_id: number;
  fecha_inicio: string;
  evaluador_externo_id?: number;
}

export interface ProjectUpdate {
  titulo?: string;
  objetivos?: string;
  convocatoria_id?: number;
  grupo_investigacion_id?: number;
  linea_investigacion_id?: number;
  extension_id?: number;
  estado_id?: number;
  fecha_inicio?: string;
  evaluador_externo_id?: number;
}

const projectService = {
  async getProjects(): Promise<Project[]> {
    const response = await axios.get(`${API_URL}/proyectos`);
    return response.data;
  },

  async getProject(id: number): Promise<Project> {
    const response = await axios.get(`${API_URL}/proyectos/${id}`);
    return response.data;
  },

  async createProject(project: ProjectCreate): Promise<Project> {
    const response = await axios.post(`${API_URL}/proyectos`, project);
    return response.data;
  },

  async updateProject(id: number, project: ProjectUpdate): Promise<Project> {
    const response = await axios.put(`${API_URL}/proyectos/${id}`, project);
    return response.data;
  },

  async deleteProject(id: number): Promise<void> {
    await axios.delete(`${API_URL}/proyectos/${id}`);
  },

  async getConvocatorias(): Promise<any[]> {
    const response = await axios.get(`${API_URL}/convocatorias`);
    return response.data;
  },

  async getGruposInvestigacion(): Promise<any[]> {
    const response = await axios.get(`${API_URL}/grupos-investigacion`);
    return response.data;
  },

  async getLineasInvestigacion(): Promise<any[]> {
    const response = await axios.get(`${API_URL}/lineas-investigacion`);
    return response.data;
  },

  async getExtensiones(): Promise<any[]> {
    const response = await axios.get(`${API_URL}/extensiones`);
    return response.data;
  },

  async getEstados(): Promise<any[]> {
    const response = await axios.get(`${API_URL}/estados`);
    return response.data;
  },

  async getEvaluadoresExternos(): Promise<any[]> {
    const response = await axios.get(`${API_URL}/evaluadores-externos`);
    return response.data;
  },

  async getProyectos(filtros?: FiltrosProyecto): Promise<PaginatedResponse<Proyecto>> {
    const response = await axiosInstance.get<PaginatedResponse<Proyecto>>('/proyectos', {
      params: filtros,
    });
    return response.data;
  },

  async getProyecto(id: number): Promise<Proyecto> {
    const response = await axiosInstance.get<Proyecto>(`/proyectos/${id}`);
    return response.data;
  },

  async createProyecto(proyecto: Omit<Proyecto, 'id'>): Promise<Proyecto> {
    const response = await axiosInstance.post<Proyecto>('/proyectos', proyecto);
    return response.data;
  },

  async updateProyecto(id: number, proyecto: Partial<Proyecto>): Promise<Proyecto> {
    const response = await axiosInstance.put<Proyecto>(`/proyectos/${id}`, proyecto);
    return response.data;
  },

  async deleteProyecto(id: number): Promise<void> {
    await axiosInstance.delete(`/proyectos/${id}`);
  },

  async getProyectosByResponsable(responsableId: number): Promise<Proyecto[]> {
    const response = await axiosInstance.get<Proyecto[]>(`/proyectos/responsable/${responsableId}`);
    return response.data;
  },

  async getProyectosByEstado(estado: string): Promise<Proyecto[]> {
    const response = await axiosInstance.get<Proyecto[]>(`/proyectos/estado/${estado}`);
    return response.data;
  },
};

export default projectService; 