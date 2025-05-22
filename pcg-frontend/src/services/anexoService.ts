import axiosInstance from './axiosConfig';
import { Anexo, PaginatedResponse } from '../types';

export const getAnexos = async (): Promise<PaginatedResponse<Anexo>> => {
  const response = await axiosInstance.get<PaginatedResponse<Anexo>>('/anexos');
  return response.data;
};

export const getAnexo = async (id: number): Promise<Anexo> => {
  const response = await axiosInstance.get<Anexo>(`/anexos/${id}`);
  return response.data;
};

export const createAnexo = async (anexo: Omit<Anexo, 'id'>): Promise<Anexo> => {
  const response = await axiosInstance.post<Anexo>('/anexos', anexo);
  return response.data;
};

export const updateAnexo = async (id: number, anexo: Partial<Anexo>): Promise<Anexo> => {
  const response = await axiosInstance.put<Anexo>(`/anexos/${id}`, anexo);
  return response.data;
};

export const deleteAnexo = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/anexos/${id}`);
};

export const getAnexosByProyecto = async (proyectoId: number): Promise<Anexo[]> => {
  const response = await axiosInstance.get<Anexo[]>(`/anexos/proyecto/${proyectoId}`);
  return response.data;
};

export const getAnexosByExtension = async (extensionId: number): Promise<Anexo[]> => {
  const response = await axiosInstance.get<Anexo[]>(`/anexos/extension/${extensionId}`);
  return response.data;
};

export const getAnexosByPrograma = async (programaId: number): Promise<Anexo[]> => {
  const response = await axiosInstance.get<Anexo[]>(`/anexos/programa/${programaId}`);
  return response.data;
};

export const getAnexosByAvance = async (avanceId: number): Promise<Anexo[]> => {
  const response = await axiosInstance.get<Anexo[]>(`/anexos/avance/${avanceId}`);
  return response.data;
};

export const getAnexosByTipo = async (tipo: string): Promise<Anexo[]> => {
  const response = await axiosInstance.get<Anexo[]>(`/anexos/tipo/${tipo}`);
  return response.data;
};

export const toggleAnexoStatus = async (id: number): Promise<Anexo> => {
  const response = await axiosInstance.patch<Anexo>(`/anexos/${id}/toggle-status`);
  return response.data;
}; 