import axios from 'axios';

export interface Permiso {
  id: number;
  nombre: string;
  descripcion: string;
  codigo: string;
}

export const permisoService = {
  getAll: async (): Promise<Permiso[]> => {
    const response = await axios.get('/api/v1/permisos');
    return response.data;
  },

  getById: async (id: number): Promise<Permiso> => {
    const response = await axios.get(`/api/v1/permisos/${id}`);
    return response.data;
  },

  create: async (permiso: Omit<Permiso, 'id'>): Promise<Permiso> => {
    const response = await axios.post('/api/v1/permisos', permiso);
    return response.data;
  },

  update: async (id: number, permiso: Partial<Permiso>): Promise<Permiso> => {
    const response = await axios.put(`/api/v1/permisos/${id}`, permiso);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await axios.delete(`/api/v1/permisos/${id}`);
  }
}; 