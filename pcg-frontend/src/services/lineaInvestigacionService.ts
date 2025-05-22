import axiosInstance from './axiosConfig';
import { LineaInvestigacion, PaginatedResponse } from '../types';

export const getLineasInvestigacion = async (): Promise<PaginatedResponse<LineaInvestigacion>> => {
  const response = await axiosInstance.get<PaginatedResponse<LineaInvestigacion>>('/lineas-investigacion');
  return response.data;
};

export const getLineaInvestigacion = async (id: number): Promise<LineaInvestigacion> => {
  const response = await axiosInstance.get<LineaInvestigacion>(`/lineas-investigacion/${id}`);
  return response.data;
};

export const createLineaInvestigacion = async (linea: Omit<LineaInvestigacion, 'id'>): Promise<LineaInvestigacion> => {
  const response = await axiosInstance.post<LineaInvestigacion>('/lineas-investigacion', linea);
  return response.data;
};

export const updateLineaInvestigacion = async (id: number, linea: Partial<LineaInvestigacion>): Promise<LineaInvestigacion> => {
  const response = await axiosInstance.put<LineaInvestigacion>(`/lineas-investigacion/${id}`, linea);
  return response.data;
};

export const deleteLineaInvestigacion = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/lineas-investigacion/${id}`);
};

export const getLineasByFacultad = async (facultadId: number): Promise<LineaInvestigacion[]> => {
  const response = await axiosInstance.get<LineaInvestigacion[]>(`/lineas-investigacion/facultad/${facultadId}`);
  return response.data;
};

export const getLineasByCoordinador = async (coordinadorId: number): Promise<LineaInvestigacion[]> => {
  const response = await axiosInstance.get<LineaInvestigacion[]>(`/lineas-investigacion/coordinador/${coordinadorId}`);
  return response.data;
};

export const toggleLineaInvestigacionStatus = async (id: number): Promise<LineaInvestigacion> => {
  const response = await axiosInstance.patch<LineaInvestigacion>(`/lineas-investigacion/${id}/toggle-status`);
  return response.data;
}; 