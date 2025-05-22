import axiosInstance from './axiosConfig';
import { Cronograma, PaginatedResponse } from '../types';

export const getCronogramas = async (): Promise<PaginatedResponse<Cronograma>> => {
  const response = await axiosInstance.get<PaginatedResponse<Cronograma>>('/cronogramas');
  return response.data;
};

export const getCronograma = async (id: number): Promise<Cronograma> => {
  const response = await axiosInstance.get<Cronograma>(`/cronogramas/${id}`);
  return response.data;
};

export const createCronograma = async (cronograma: Omit<Cronograma, 'id'>): Promise<Cronograma> => {
  const response = await axiosInstance.post<Cronograma>('/cronogramas', cronograma);
  return response.data;
};

export const updateCronograma = async (id: number, cronograma: Partial<Cronograma>): Promise<Cronograma> => {
  const response = await axiosInstance.put<Cronograma>(`/cronogramas/${id}`, cronograma);
  return response.data;
};

export const deleteCronograma = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/cronogramas/${id}`);
};

export const getCronogramasByProyecto = async (proyectoId: number): Promise<Cronograma[]> => {
  const response = await axiosInstance.get<Cronograma[]>(`/cronogramas/proyecto/${proyectoId}`);
  return response.data;
};

export const getCronogramasByResponsable = async (responsableId: number): Promise<Cronograma[]> => {
  const response = await axiosInstance.get<Cronograma[]>(`/cronogramas/responsable/${responsableId}`);
  return response.data;
};

export const getCronogramasByEstado = async (estado: string): Promise<Cronograma[]> => {
  const response = await axiosInstance.get<Cronograma[]>(`/cronogramas/estado/${estado}`);
  return response.data;
};

export const getCronogramasByFecha = async (fechaInicio: string, fechaFin: string): Promise<Cronograma[]> => {
  const response = await axiosInstance.get<Cronograma[]>(`/cronogramas/fecha`, {
    params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin }
  });
  return response.data;
};

export const updateCronogramaEstado = async (id: number, estado: string): Promise<Cronograma> => {
  const response = await axiosInstance.patch<Cronograma>(`/cronogramas/${id}/estado`, { estado });
  return response.data;
};

export const updateCronogramaAvance = async (id: number, porcentaje: number): Promise<Cronograma> => {
  const response = await axiosInstance.patch<Cronograma>(`/cronogramas/${id}/avance`, { porcentaje_avance: porcentaje });
  return response.data;
}; 