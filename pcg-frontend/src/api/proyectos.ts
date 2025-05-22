import axios from 'axios';

export interface Proyecto {
  id: number;
  titulo: string;
  descripcion: string;
  fecha_inicio: string;
  fecha_fin: string;
  estado: string;
  grupo_investigacion_id: number;
  lider_id: number;
}

export const proyectosApi = {
  getAll: async (): Promise<Proyecto[]> => {
    const response = await axios.get('/api/v1/proyectos');
    return response.data;
  },

  getById: async (id: number): Promise<Proyecto> => {
    const response = await axios.get(`/api/v1/proyectos/${id}`);
    return response.data;
  },

  create: async (proyecto: Omit<Proyecto, 'id'>): Promise<Proyecto> => {
    const response = await axios.post('/api/v1/proyectos', proyecto);
    return response.data;
  },

  update: async (id: number, proyecto: Partial<Proyecto>): Promise<Proyecto> => {
    const response = await axios.put(`/api/v1/proyectos/${id}`, proyecto);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await axios.delete(`/api/v1/proyectos/${id}`);
  }
}; 