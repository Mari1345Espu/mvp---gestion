import axiosInstance from './axiosConfig';
import { Evaluacion, PaginatedResponse } from '../types';

export const getEvaluaciones = async (): Promise<PaginatedResponse<Evaluacion>> => {
  const response = await axiosInstance.get<PaginatedResponse<Evaluacion>>('/evaluaciones');
  return response.data;
};

export const getEvaluacion = async (id: number): Promise<Evaluacion> => {
  const response = await axiosInstance.get<Evaluacion>(`/evaluaciones/${id}`);
  return response.data;
};

export const createEvaluacion = async (evaluacion: Omit<Evaluacion, 'id'>): Promise<Evaluacion> => {
  const response = await axiosInstance.post<Evaluacion>('/evaluaciones', evaluacion);
  return response.data;
};

export const updateEvaluacion = async (id: number, evaluacion: Partial<Evaluacion>): Promise<Evaluacion> => {
  const response = await axiosInstance.put<Evaluacion>(`/evaluaciones/${id}`, evaluacion);
  return response.data;
};

export const deleteEvaluacion = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/evaluaciones/${id}`);
};

export const getEvaluacionesByProyecto = async (proyectoId: number): Promise<Evaluacion[]> => {
  const response = await axiosInstance.get<Evaluacion[]>(`/evaluaciones/proyecto/${proyectoId}`);
  return response.data;
};

export const getEvaluacionesByEvaluador = async (evaluadorId: number): Promise<Evaluacion[]> => {
  const response = await axiosInstance.get<Evaluacion[]>(`/evaluaciones/evaluador/${evaluadorId}`);
  return response.data;
};

export const getEvaluacionesByTipo = async (tipo: string): Promise<Evaluacion[]> => {
  const response = await axiosInstance.get<Evaluacion[]>(`/evaluaciones/tipo/${tipo}`);
  return response.data;
};

export const getEvaluacionesByEstado = async (estado: string): Promise<Evaluacion[]> => {
  const response = await axiosInstance.get<Evaluacion[]>(`/evaluaciones/estado/${estado}`);
  return response.data;
};

export const getEvaluacionesByFecha = async (fechaInicio: string, fechaFin: string): Promise<Evaluacion[]> => {
  const response = await axiosInstance.get<Evaluacion[]>(`/evaluaciones/fecha`, {
    params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin }
  });
  return response.data;
};

export const updateEvaluacionEstado = async (id: number, estado: string): Promise<Evaluacion> => {
  const response = await axiosInstance.patch<Evaluacion>(`/evaluaciones/${id}/estado`, { estado });
  return response.data;
};

export const enviarEvaluacion = async (id: number): Promise<Evaluacion> => {
  const response = await axiosInstance.post<Evaluacion>(`/evaluaciones/${id}/enviar`);
  return response.data;
}; 