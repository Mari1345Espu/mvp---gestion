import api from './api';

export interface Permission {
  id: number;
  nombre: string;
  descripcion: string;
  codigo: string;
  modulo: string;
  created_at: string;
  updated_at: string;
}

export const permissionService = {
  async getPermissions(): Promise<Permission[]> {
    const response = await api.get('/permissions');
    return response.data;
  },

  async getPermission(id: number): Promise<Permission> {
    const response = await api.get(`/permissions/${id}`);
    return response.data;
  },

  async createPermission(permission: Omit<Permission, 'id' | 'created_at' | 'updated_at'>): Promise<Permission> {
    const response = await api.post('/permissions', permission);
    return response.data;
  },

  async updatePermission(id: number, permission: Partial<Permission>): Promise<Permission> {
    const response = await api.put(`/permissions/${id}`, permission);
    return response.data;
  },

  async deletePermission(id: number): Promise<void> {
    await api.delete(`/permissions/${id}`);
  },

  async getPermissionsByModule(module: string): Promise<Permission[]> {
    const response = await api.get(`/permissions/module/${module}`);
    return response.data;
  },

  async getPermissionsByRole(roleId: number): Promise<Permission[]> {
    const response = await api.get(`/permissions/role/${roleId}`);
    return response.data;
  },

  async getPermissionsByUser(userId: number): Promise<Permission[]> {
    const response = await api.get(`/permissions/user/${userId}`);
    return response.data;
  },

  async assignPermissionToRole(permissionId: number, roleId: number): Promise<void> {
    await api.post(`/permissions/${permissionId}/roles`, { role_id: roleId });
  },

  async removePermissionFromRole(permissionId: number, roleId: number): Promise<void> {
    await api.delete(`/permissions/${permissionId}/roles/${roleId}`);
  }
}; 