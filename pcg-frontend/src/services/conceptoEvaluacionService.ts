import axiosInstance from './axiosConfig';
import { ConceptoEvaluacion, PaginatedResponse } from '../types';

export const getConceptosEvaluacion = async (): Promise<PaginatedResponse<ConceptoEvaluacion>> => {
  const response = await axiosInstance.get<PaginatedResponse<ConceptoEvaluacion>>('/conceptos-evaluacion');
  return response.data;
};

export const getConceptoEvaluacion = async (id: number): Promise<ConceptoEvaluacion> => {
  const response = await axiosInstance.get<ConceptoEvaluacion>(`/conceptos-evaluacion/${id}`);
  return response.data;
};

export const createConceptoEvaluacion = async (concepto: Omit<ConceptoEvaluacion, 'id'>): Promise<ConceptoEvaluacion> => {
  const response = await axiosInstance.post<ConceptoEvaluacion>('/conceptos-evaluacion', concepto);
  return response.data;
};

export const updateConceptoEvaluacion = async (id: number, concepto: Partial<ConceptoEvaluacion>): Promise<ConceptoEvaluacion> => {
  const response = await axiosInstance.put<ConceptoEvaluacion>(`/conceptos-evaluacion/${id}`, concepto);
  return response.data;
};

export const deleteConceptoEvaluacion = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/conceptos-evaluacion/${id}`);
};

export const getConceptosByTipo = async (tipo: string): Promise<ConceptoEvaluacion[]> => {
  const response = await axiosInstance.get<ConceptoEvaluacion[]>(`/conceptos-evaluacion/tipo/${tipo}`);
  return response.data;
};

export const getConceptosByCriterio = async (criterio: string): Promise<ConceptoEvaluacion[]> => {
  const response = await axiosInstance.get<ConceptoEvaluacion[]>(`/conceptos-evaluacion/criterio/${criterio}`);
  return response.data;
};

export const getConceptosByEstado = async (estado: string): Promise<ConceptoEvaluacion[]> => {
  const response = await axiosInstance.get<ConceptoEvaluacion[]>(`/conceptos-evaluacion/estado/${estado}`);
  return response.data;
};

export const updateConceptoEstado = async (id: number, estado: string): Promise<ConceptoEvaluacion> => {
  const response = await axiosInstance.patch<ConceptoEvaluacion>(`/conceptos-evaluacion/${id}/estado`, { estado });
  return response.data;
};

export const agregarCriterio = async (id: number, criterio: string): Promise<ConceptoEvaluacion> => {
  const response = await axiosInstance.post<ConceptoEvaluacion>(`/conceptos-evaluacion/${id}/criterios`, { criterio });
  return response.data;
};

export const eliminarCriterio = async (id: number, criterio: string): Promise<ConceptoEvaluacion> => {
  const response = await axiosInstance.delete<ConceptoEvaluacion>(`/conceptos-evaluacion/${id}/criterios`, {
    data: { criterio }
  });
  return response.data;
}; 