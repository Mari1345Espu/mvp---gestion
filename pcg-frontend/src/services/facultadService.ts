import axiosInstance from './axiosConfig';
import { Facultad, PaginatedResponse } from '../types';

export const getFacultades = async (): Promise<PaginatedResponse<Facultad>> => {
  const response = await axiosInstance.get<PaginatedResponse<Facultad>>('/facultades');
  return response.data;
};

export const getFacultad = async (id: number): Promise<Facultad> => {
  const response = await axiosInstance.get<Facultad>(`/facultades/${id}`);
  return response.data;
};

export const createFacultad = async (facultad: Omit<Facultad, 'id'>): Promise<Facultad> => {
  const response = await axiosInstance.post<Facultad>('/facultades', facultad);
  return response.data;
};

export const updateFacultad = async (id: number, facultad: Partial<Facultad>): Promise<Facultad> => {
  const response = await axiosInstance.put<Facultad>(`/facultades/${id}`, facultad);
  return response.data;
};

export const deleteFacultad = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/facultades/${id}`);
};

export const getFacultadesByDecano = async (decanoId: number): Promise<Facultad[]> => {
  const response = await axiosInstance.get<Facultad[]>(`/facultades/decano/${decanoId}`);
  return response.data;
};

export const toggleFacultadStatus = async (id: number): Promise<Facultad> => {
  const response = await axiosInstance.patch<Facultad>(`/facultades/${id}/toggle-status`);
  return response.data;
}; 