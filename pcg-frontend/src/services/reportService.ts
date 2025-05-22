import axiosInstance from './axiosConfig';
import { Reporte, PaginatedResponse, FiltrosReporte } from '../types';

export const getReportes = async (filtros?: FiltrosReporte): Promise<PaginatedResponse<Reporte>> => {
  const response = await axiosInstance.get<PaginatedResponse<Reporte>>('/reportes', {
    params: filtros,
  });
  return response.data;
};

export const getReporte = async (id: number): Promise<Reporte> => {
  const response = await axiosInstance.get<Reporte>(`/reportes/${id}`);
  return response.data;
};

export const createReporte = async (reporte: Omit<Reporte, 'id'>): Promise<Reporte> => {
  const response = await axiosInstance.post<Reporte>('/reportes', reporte);
  return response.data;
};

export const updateReporte = async (id: number, reporte: Partial<Reporte>): Promise<Reporte> => {
  const response = await axiosInstance.put<Reporte>(`/reportes/${id}`, reporte);
  return response.data;
};

export const deleteReporte = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/reportes/${id}`);
};

export const getReportesByUsuario = async (usuarioId: number): Promise<Reporte[]> => {
  const response = await axiosInstance.get<Reporte[]>(`/reportes/usuario/${usuarioId}`);
  return response.data;
};

export const getReportesByProyecto = async (proyectoId: number): Promise<Reporte[]> => {
  const response = await axiosInstance.get<Reporte[]>(`/reportes/proyecto/${proyectoId}`);
  return response.data;
};

export const getReportesByEstado = async (estado: string): Promise<Reporte[]> => {
  const response = await axiosInstance.get<Reporte[]>(`/reportes/estado/${estado}`);
  return response.data;
}; 