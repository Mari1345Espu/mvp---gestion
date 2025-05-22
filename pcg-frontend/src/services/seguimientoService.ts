import axiosInstance from './axiosConfig';
import { Seguimiento, PaginatedResponse } from '../types';

export const getSeguimientos = async (): Promise<PaginatedResponse<Seguimiento>> => {
  const response = await axiosInstance.get<PaginatedResponse<Seguimiento>>('/seguimientos');
  return response.data;
};

export const getSeguimiento = async (id: number): Promise<Seguimiento> => {
  const response = await axiosInstance.get<Seguimiento>(`/seguimientos/${id}`);
  return response.data;
};

export const createSeguimiento = async (seguimiento: Omit<Seguimiento, 'id'>): Promise<Seguimiento> => {
  const response = await axiosInstance.post<Seguimiento>('/seguimientos', seguimiento);
  return response.data;
};

export const updateSeguimiento = async (id: number, seguimiento: Partial<Seguimiento>): Promise<Seguimiento> => {
  const response = await axiosInstance.put<Seguimiento>(`/seguimientos/${id}`, seguimiento);
  return response.data;
};

export const deleteSeguimiento = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/seguimientos/${id}`);
};

export const getSeguimientosByProyecto = async (proyectoId: number): Promise<Seguimiento[]> => {
  const response = await axiosInstance.get<Seguimiento[]>(`/seguimientos/proyecto/${proyectoId}`);
  return response.data;
};

export const getSeguimientosByTipo = async (tipo: string): Promise<Seguimiento[]> => {
  const response = await axiosInstance.get<Seguimiento[]>(`/seguimientos/tipo/${tipo}`);
  return response.data;
};

export const getSeguimientosByEstado = async (estado: string): Promise<Seguimiento[]> => {
  const response = await axiosInstance.get<Seguimiento[]>(`/seguimientos/estado/${estado}`);
  return response.data;
};

export const getSeguimientosByUsuario = async (usuarioId: number): Promise<Seguimiento[]> => {
  const response = await axiosInstance.get<Seguimiento[]>(`/seguimientos/usuario/${usuarioId}`);
  return response.data;
};

export const getSeguimientosByFecha = async (fechaInicio: string, fechaFin: string): Promise<Seguimiento[]> => {
  const response = await axiosInstance.get<Seguimiento[]>(`/seguimientos/fecha`, {
    params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin }
  });
  return response.data;
};

export const updateSeguimientoEstado = async (id: number, estado: string): Promise<Seguimiento> => {
  const response = await axiosInstance.patch<Seguimiento>(`/seguimientos/${id}/estado`, { estado });
  return response.data;
}; 