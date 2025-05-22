import axiosInstance from './axiosConfig';
import { Avance, PaginatedResponse } from '../types';

export const getAvances = async (): Promise<PaginatedResponse<Avance>> => {
  const response = await axiosInstance.get<PaginatedResponse<Avance>>('/avances');
  return response.data;
};

export const getAvance = async (id: number): Promise<Avance> => {
  const response = await axiosInstance.get<Avance>(`/avances/${id}`);
  return response.data;
};

export const createAvance = async (avance: Omit<Avance, 'id'>): Promise<Avance> => {
  const response = await axiosInstance.post<Avance>('/avances', avance);
  return response.data;
};

export const updateAvance = async (id: number, avance: Partial<Avance>): Promise<Avance> => {
  const response = await axiosInstance.put<Avance>(`/avances/${id}`, avance);
  return response.data;
};

export const deleteAvance = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/avances/${id}`);
};

export const getAvancesByProyecto = async (proyectoId: number): Promise<Avance[]> => {
  const response = await axiosInstance.get<Avance[]>(`/avances/proyecto/${proyectoId}`);
  return response.data;
};

export const getAvancesByExtension = async (extensionId: number): Promise<Avance[]> => {
  const response = await axiosInstance.get<Avance[]>(`/avances/extension/${extensionId}`);
  return response.data;
};

export const getAvancesByPrograma = async (programaId: number): Promise<Avance[]> => {
  const response = await axiosInstance.get<Avance[]>(`/avances/programa/${programaId}`);
  return response.data;
};

export const getAvancesByFecha = async (fechaInicio: string, fechaFin: string): Promise<Avance[]> => {
  const response = await axiosInstance.get<Avance[]>(`/avances/fecha`, {
    params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin }
  });
  return response.data;
};

export const toggleAvanceStatus = async (id: number): Promise<Avance> => {
  const response = await axiosInstance.patch<Avance>(`/avances/${id}/toggle-status`);
  return response.data;
}; 