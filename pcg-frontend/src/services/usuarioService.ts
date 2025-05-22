import api from './api';
import { User, PaginatedResponse, FiltrosUsuario, RegisterData } from '../types';

export const usuarioService = {
  async getUsuarios(params?: FiltrosUsuario): Promise<PaginatedResponse<User>> {
    const response = await api.get('/usuarios', { params });
    return response.data;
  },

  async getUsuario(id: number): Promise<User> {
    const response = await api.get(`/usuarios/${id}`);
    return response.data;
  },

  async createUsuario(usuario: RegisterData): Promise<User> {
    const response = await api.post('/usuarios', usuario);
    return response.data;
  },

  async updateUsuario(id: number, usuario: Partial<User>): Promise<User> {
    const response = await api.put(`/usuarios/${id}`, usuario);
    return response.data;
  },

  async deleteUsuario(id: number): Promise<void> {
    await api.delete(`/usuarios/${id}`);
  },

  async getUsuariosByRol(rol: string): Promise<User[]> {
    const response = await api.get(`/usuarios/rol/${rol}`);
    return response.data;
  },

  async getUsuariosByEstado(estado: string): Promise<User[]> {
    const response = await api.get(`/usuarios/estado/${estado}`);
    return response.data;
  },

  async getUsuariosByPrograma(programaId: number): Promise<User[]> {
    const response = await api.get(`/usuarios/programa/${programaId}`);
    return response.data;
  },

  async getUsuariosByProyecto(proyectoId: number): Promise<User[]> {
    const response = await api.get(`/usuarios/proyecto/${proyectoId}`);
    return response.data;
  }
}; 