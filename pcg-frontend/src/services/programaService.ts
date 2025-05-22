import api from './api';
import { Programa, PaginatedResponse, FiltrosPrograma } from '../types';

export const programaService = {
  async getProgramas(params?: FiltrosPrograma): Promise<PaginatedResponse<Programa>> {
    const response = await api.get('/programas', { params });
    return response.data;
  },

  async getPrograma(id: number): Promise<Programa> {
    const response = await api.get(`/programas/${id}`);
    return response.data;
  },

  async createPrograma(programa: Omit<Programa, 'id' | 'created_at' | 'updated_at'>): Promise<Programa> {
    const response = await api.post('/programas', programa);
    return response.data;
  },

  async updatePrograma(id: number, programa: Partial<Programa>): Promise<Programa> {
    const response = await api.put(`/programas/${id}`, programa);
    return response.data;
  },

  async deletePrograma(id: number): Promise<void> {
    await api.delete(`/programas/${id}`);
  },

  async getProgramasByResponsable(responsableId: number): Promise<Programa[]> {
    const response = await api.get(`/programas/responsable/${responsableId}`);
    return response.data;
  },

  async getProgramasByEstado(estado: string): Promise<Programa[]> {
    const response = await api.get(`/programas/estado/${estado}`);
    return response.data;
  },

  async getProgramasByFechaInicio(fechaInicio: string): Promise<Programa[]> {
    const response = await api.get(`/programas/fecha-inicio/${fechaInicio}`);
    return response.data;
  },

  async getProgramasByFechaFin(fechaFin: string): Promise<Programa[]> {
    const response = await api.get(`/programas/fecha-fin/${fechaFin}`);
    return response.data;
  }
}; 