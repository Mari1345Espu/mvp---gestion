import axiosInstance from './axiosConfig';
import { Notificacion, PaginatedResponse } from '../types';

export const getNotificaciones = async (): Promise<PaginatedResponse<Notificacion>> => {
  const response = await axiosInstance.get<PaginatedResponse<Notificacion>>('/notificaciones');
  return response.data;
};

export const getNotificacion = async (id: number): Promise<Notificacion> => {
  const response = await axiosInstance.get<Notificacion>(`/notificaciones/${id}`);
  return response.data;
};

export const createNotificacion = async (notificacion: Omit<Notificacion, 'id'>): Promise<Notificacion> => {
  const response = await axiosInstance.post<Notificacion>('/notificaciones', notificacion);
  return response.data;
};

export const updateNotificacion = async (id: number, notificacion: Partial<Notificacion>): Promise<Notificacion> => {
  const response = await axiosInstance.put<Notificacion>(`/notificaciones/${id}`, notificacion);
  return response.data;
};

export const deleteNotificacion = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/notificaciones/${id}`);
};

export const getNotificacionesByUsuario = async (usuarioId: number): Promise<Notificacion[]> => {
  const response = await axiosInstance.get<Notificacion[]>(`/notificaciones/usuario/${usuarioId}`);
  return response.data;
};

export const getNotificacionesByTipo = async (tipo: string): Promise<Notificacion[]> => {
  const response = await axiosInstance.get<Notificacion[]>(`/notificaciones/tipo/${tipo}`);
  return response.data;
};

export const getNotificacionesByProyecto = async (proyectoId: number): Promise<Notificacion[]> => {
  const response = await axiosInstance.get<Notificacion[]>(`/notificaciones/proyecto/${proyectoId}`);
  return response.data;
};

export const getNotificacionesNoLeidas = async (usuarioId: number): Promise<Notificacion[]> => {
  const response = await axiosInstance.get<Notificacion[]>(`/notificaciones/usuario/${usuarioId}/no-leidas`);
  return response.data;
};

export const getNotificacionesByPrioridad = async (prioridad: string): Promise<Notificacion[]> => {
  const response = await axiosInstance.get<Notificacion[]>(`/notificaciones/prioridad/${prioridad}`);
  return response.data;
};

export const marcarComoLeida = async (id: number): Promise<Notificacion> => {
  const response = await axiosInstance.patch<Notificacion>(`/notificaciones/${id}/leer`);
  return response.data;
};

export const marcarTodasComoLeidas = async (usuarioId: number): Promise<void> => {
  await axiosInstance.patch(`/notificaciones/usuario/${usuarioId}/leer-todas`);
}; 