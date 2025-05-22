import axiosInstance from './axiosConfig';
import { Participante, PaginatedResponse } from '../types';

export const getParticipantes = async (): Promise<PaginatedResponse<Participante>> => {
  const response = await axiosInstance.get<PaginatedResponse<Participante>>('/participantes');
  return response.data;
};

export const getParticipante = async (id: number): Promise<Participante> => {
  const response = await axiosInstance.get<Participante>(`/participantes/${id}`);
  return response.data;
};

export const createParticipante = async (participante: Omit<Participante, 'id'>): Promise<Participante> => {
  const response = await axiosInstance.post<Participante>('/participantes', participante);
  return response.data;
};

export const updateParticipante = async (id: number, participante: Partial<Participante>): Promise<Participante> => {
  const response = await axiosInstance.put<Participante>(`/participantes/${id}`, participante);
  return response.data;
};

export const deleteParticipante = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/participantes/${id}`);
};

export const getParticipantesByProyecto = async (proyectoId: number): Promise<Participante[]> => {
  const response = await axiosInstance.get<Participante[]>(`/participantes/proyecto/${proyectoId}`);
  return response.data;
};

export const getParticipantesByUsuario = async (usuarioId: number): Promise<Participante[]> => {
  const response = await axiosInstance.get<Participante[]>(`/participantes/usuario/${usuarioId}`);
  return response.data;
};

export const getParticipantesByRol = async (rol: string): Promise<Participante[]> => {
  const response = await axiosInstance.get<Participante[]>(`/participantes/rol/${rol}`);
  return response.data;
};

export const getParticipantesByEstado = async (estado: string): Promise<Participante[]> => {
  const response = await axiosInstance.get<Participante[]>(`/participantes/estado/${estado}`);
  return response.data;
};

export const getParticipantesByFecha = async (fechaInicio: string, fechaFin: string): Promise<Participante[]> => {
  const response = await axiosInstance.get<Participante[]>(`/participantes/fecha`, {
    params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin }
  });
  return response.data;
};

export const updateParticipanteEstado = async (id: number, estado: string): Promise<Participante> => {
  const response = await axiosInstance.patch<Participante>(`/participantes/${id}/estado`, { estado });
  return response.data;
}; 