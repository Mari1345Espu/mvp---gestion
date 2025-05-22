import api from './api';
import { Rol, Permiso, Estado } from '../types';

export interface Role {
  id: number;
  nombre: string;
  descripcion: string;
  permisos: string[];
  created_at: string;
  updated_at: string;
}

// Servicios de Roles
export const roleService = {
  async getRoles(): Promise<Rol[]> {
    const response = await api.get('/roles');
    return response.data;
  },

  async getRole(id: number): Promise<Rol> {
    const response = await api.get(`/roles/${id}`);
    return response.data;
  },

  async createRole(role: Omit<Rol, 'id'>): Promise<Rol> {
    const response = await api.post('/roles', role);
    return response.data;
  },

  async updateRole(id: number, role: Partial<Rol>): Promise<Rol> {
    const response = await api.put(`/roles/${id}`, role);
    return response.data;
  },

  async deleteRole(id: number): Promise<void> {
    await api.delete(`/roles/${id}`);
  },

  async getRolePermissions(id: number): Promise<Permiso[]> {
    const response = await api.get(`/roles/${id}/permissions`);
    return response.data;
  },

  async updateRolePermissions(id: number, permissions: number[]): Promise<Rol> {
    const response = await api.put(`/roles/${id}/permissions`, { permissions });
    return response.data;
  },

  async getRoleUsers(id: number): Promise<number[]> {
    const response = await api.get(`/roles/${id}/users`);
    return response.data;
  },

  async assignRoleToUser(roleId: number, userId: number): Promise<void> {
    await api.post(`/roles/${roleId}/users`, { user_id: userId });
  },

  async removeRoleFromUser(roleId: number, userId: number): Promise<void> {
    await api.delete(`/roles/${roleId}/users/${userId}`);
  }
};

// Servicios de Permisos
export const getPermisos = async (): Promise<Permiso[]> => {
  const response = await api.get<Permiso[]>('/permisos');
  return response.data;
};

export const getPermiso = async (id: number): Promise<Permiso> => {
  const response = await api.get<Permiso>(`/permisos/${id}`);
  return response.data;
};

export const createPermiso = async (permiso: Omit<Permiso, 'id'>): Promise<Permiso> => {
  const response = await api.post<Permiso>('/permisos', permiso);
  return response.data;
};

export const updatePermiso = async (id: number, permiso: Partial<Permiso>): Promise<Permiso> => {
  const response = await api.put<Permiso>(`/permisos/${id}`, permiso);
  return response.data;
};

export const deletePermiso = async (id: number): Promise<void> => {
  await api.delete(`/permisos/${id}`);
};

// Servicios de Estados
export const getEstados = async (): Promise<Estado[]> => {
  const response = await api.get<Estado[]>('/estados');
  return response.data;
};

export const getEstado = async (id: number): Promise<Estado> => {
  const response = await api.get<Estado>(`/estados/${id}`);
  return response.data;
};

export const createEstado = async (estado: Omit<Estado, 'id'>): Promise<Estado> => {
  const response = await api.post<Estado>('/estados', estado);
  return response.data;
};

export const updateEstado = async (id: number, estado: Partial<Estado>): Promise<Estado> => {
  const response = await api.put<Estado>(`/estados/${id}`, estado);
  return response.data;
};

export const deleteEstado = async (id: number): Promise<void> => {
  await api.delete(`/estados/${id}`);
}; 