import axiosInstance from './axiosConfig';
import { Convocatoria, PaginatedResponse, FiltrosConvocatoria } from '../types';

export const getConvocatorias = async (filtros?: FiltrosConvocatoria): Promise<PaginatedResponse<Convocatoria>> => {
  const response = await axiosInstance.get<PaginatedResponse<Convocatoria>>('/convocatorias', {
    params: filtros,
  });
  return response.data;
};

export const getConvocatoria = async (id: number): Promise<Convocatoria> => {
  const response = await axiosInstance.get<Convocatoria>(`/convocatorias/${id}`);
  return response.data;
};

export const createConvocatoria = async (convocatoria: Omit<Convocatoria, 'id'>): Promise<Convocatoria> => {
  const response = await axiosInstance.post<Convocatoria>('/convocatorias', convocatoria);
  return response.data;
};

export const updateConvocatoria = async (id: number, convocatoria: Partial<Convocatoria>): Promise<Convocatoria> => {
  const response = await axiosInstance.put<Convocatoria>(`/convocatorias/${id}`, convocatoria);
  return response.data;
};

export const deleteConvocatoria = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/convocatorias/${id}`);
};

export const getConvocatoriasByEstado = async (estado: string): Promise<Convocatoria[]> => {
  const response = await axiosInstance.get<Convocatoria[]>(`/convocatorias/estado/${estado}`);
  return response.data;
};

export const getConvocatoriasByTipo = async (tipo: string): Promise<Convocatoria[]> => {
  const response = await axiosInstance.get<Convocatoria[]>(`/convocatorias/tipo/${tipo}`);
  return response.data;
};

export const getConvocatoriasActivas = async (): Promise<Convocatoria[]> => {
  const response = await axiosInstance.get<Convocatoria[]>('/convocatorias/activas');
  return response.data;
}; 