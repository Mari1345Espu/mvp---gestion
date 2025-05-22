import axios from 'axios';

export interface Estado {
  id: number;
  nombre: string;
  descripcion: string;
  color: string;
}

export const estadoService = {
  getAll: async (): Promise<Estado[]> => {
    const response = await axios.get('/api/v1/estados');
    return response.data;
  },

  getById: async (id: number): Promise<Estado> => {
    const response = await axios.get(`/api/v1/estados/${id}`);
    return response.data;
  },

  create: async (estado: Omit<Estado, 'id'>): Promise<Estado> => {
    const response = await axios.post('/api/v1/estados', estado);
    return response.data;
  },

  update: async (id: number, estado: Partial<Estado>): Promise<Estado> => {
    const response = await axios.put(`/api/v1/estados/${id}`, estado);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await axios.delete(`/api/v1/estados/${id}`);
  }
}; 