import axios from 'axios';

export interface GrupoInvestigacion {
  id: number;
  nombre: string;
  descripcion: string;
  fecha_creacion: string;
  lider_id: number;
}

export const grupoinvestigacionService = {
  getAll: async (): Promise<GrupoInvestigacion[]> => {
    const response = await axios.get('/api/v1/grupos-investigacion');
    return response.data;
  },

  getById: async (id: number): Promise<GrupoInvestigacion> => {
    const response = await axios.get(`/api/v1/grupos-investigacion/${id}`);
    return response.data;
  },

  create: async (grupo: Omit<GrupoInvestigacion, 'id'>): Promise<GrupoInvestigacion> => {
    const response = await axios.post('/api/v1/grupos-investigacion', grupo);
    return response.data;
  },

  update: async (id: number, grupo: Partial<GrupoInvestigacion>): Promise<GrupoInvestigacion> => {
    const response = await axios.put(`/api/v1/grupos-investigacion/${id}`, grupo);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await axios.delete(`/api/v1/grupos-investigacion/${id}`);
  }
}; 