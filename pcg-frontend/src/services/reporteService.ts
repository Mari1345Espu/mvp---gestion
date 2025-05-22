import api from './api';
import { Reporte, PaginatedResponse, FiltrosReporte } from '../types';

export const reporteService = {
  async getReportes(params?: FiltrosReporte): Promise<PaginatedResponse<Reporte>> {
    const response = await api.get('/reportes', { params });
    return response.data;
  },

  async getReporte(id: number): Promise<Reporte> {
    const response = await api.get(`/reportes/${id}`);
    return response.data;
  },

  async createReporte(reporte: Omit<Reporte, 'id' | 'fecha_creacion' | 'fecha_actualizacion'>): Promise<Reporte> {
    const response = await api.post('/reportes', reporte);
    return response.data;
  },

  async updateReporte(id: number, reporte: Partial<Reporte>): Promise<Reporte> {
    const response = await api.put(`/reportes/${id}`, reporte);
    return response.data;
  },

  async deleteReporte(id: number): Promise<void> {
    await api.delete(`/reportes/${id}`);
  },

  async getReportesByUsuario(usuarioId: number): Promise<Reporte[]> {
    const response = await api.get(`/reportes/usuario/${usuarioId}`);
    return response.data;
  },

  async getReportesByProyecto(proyectoId: number): Promise<Reporte[]> {
    const response = await api.get(`/reportes/proyecto/${proyectoId}`);
    return response.data;
  },

  async getReportesByEstado(estado: string): Promise<Reporte[]> {
    const response = await api.get(`/reportes/estado/${estado}`);
    return response.data;
  },

  async getReportesByTipo(tipo: string): Promise<Reporte[]> {
    const response = await api.get(`/reportes/tipo/${tipo}`);
    return response.data;
  }
}; 