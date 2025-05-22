import axiosInstance from './axiosConfig';
import { Recurso, PaginatedResponse } from '../types';

export const getRecursos = async (): Promise<PaginatedResponse<Recurso>> => {
  const response = await axiosInstance.get<PaginatedResponse<Recurso>>('/recursos');
  return response.data;
};

export const getRecurso = async (id: number): Promise<Recurso> => {
  const response = await axiosInstance.get<Recurso>(`/recursos/${id}`);
  return response.data;
};

export const createRecurso = async (recurso: Omit<Recurso, 'id'>): Promise<Recurso> => {
  const response = await axiosInstance.post<Recurso>('/recursos', recurso);
  return response.data;
};

export const updateRecurso = async (id: number, recurso: Partial<Recurso>): Promise<Recurso> => {
  const response = await axiosInstance.put<Recurso>(`/recursos/${id}`, recurso);
  return response.data;
};

export const deleteRecurso = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/recursos/${id}`);
};

export const getRecursosByProyecto = async (proyectoId: number): Promise<Recurso[]> => {
  const response = await axiosInstance.get<Recurso[]>(`/recursos/proyecto/${proyectoId}`);
  return response.data;
};

export const getRecursosByTipo = async (tipo: string): Promise<Recurso[]> => {
  const response = await axiosInstance.get<Recurso[]>(`/recursos/tipo/${tipo}`);
  return response.data;
};

export const getRecursosByEstado = async (estado: string): Promise<Recurso[]> => {
  const response = await axiosInstance.get<Recurso[]>(`/recursos/estado/${estado}`);
  return response.data;
};

export const getRecursosByFecha = async (fechaInicio: string, fechaFin: string): Promise<Recurso[]> => {
  const response = await axiosInstance.get<Recurso[]>(`/recursos/fecha`, {
    params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin }
  });
  return response.data;
};

export const updateRecursoEstado = async (id: number, estado: string): Promise<Recurso> => {
  const response = await axiosInstance.patch<Recurso>(`/recursos/${id}/estado`, { estado });
  return response.data;
}; 