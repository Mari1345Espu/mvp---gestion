import api from './api';
import { Extension, PaginatedResponse, FiltrosExtension } from '../types';

export const extensionService = {
  async getExtensiones(params?: FiltrosExtension): Promise<PaginatedResponse<Extension>> {
    const response = await api.get('/extensiones', { params });
    return response.data;
  },

  async getExtension(id: number): Promise<Extension> {
    const response = await api.get(`/extensiones/${id}`);
    return response.data;
  },

  async createExtension(extension: Omit<Extension, 'id'>): Promise<Extension> {
    const response = await api.post('/extensiones', extension);
    return response.data;
  },

  async updateExtension(id: number, extension: Partial<Extension>): Promise<Extension> {
    const response = await api.put(`/extensiones/${id}`, extension);
    return response.data;
  },

  async deleteExtension(id: number): Promise<void> {
    await api.delete(`/extensiones/${id}`);
  },

  async getExtensionesByPrograma(programaId: number): Promise<Extension[]> {
    const response = await api.get(`/extensiones/programa/${programaId}`);
    return response.data;
  },

  async getExtensionesByTipo(tipo: string): Promise<Extension[]> {
    const response = await api.get(`/extensiones/tipo/${tipo}`);
    return response.data;
  },

  async getExtensionesByModalidad(modalidad: string): Promise<Extension[]> {
    const response = await api.get(`/extensiones/modalidad/${modalidad}`);
    return response.data;
  },

  async getExtensionesByEstado(activo: boolean): Promise<Extension[]> {
    const response = await api.get(`/extensiones/estado/${activo}`);
    return response.data;
  },

  async toggleExtensionStatus(id: number): Promise<Extension> {
    const response = await api.patch(`/extensiones/${id}/toggle-status`);
    return response.data;
  }
}; 