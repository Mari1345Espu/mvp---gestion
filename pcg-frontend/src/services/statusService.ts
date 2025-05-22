import api from './api';

export interface Status {
  id: number;
  nombre: string;
  descripcion: string;
  tipo: 'proyecto' | 'programa' | 'reporte' | 'extension';
  color: string;
  created_at: string;
  updated_at: string;
}

export const statusService = {
  async getStatuses(): Promise<Status[]> {
    const response = await api.get('/statuses');
    return response.data;
  },

  async getStatus(id: number): Promise<Status> {
    const response = await api.get(`/statuses/${id}`);
    return response.data;
  },

  async createStatus(status: Omit<Status, 'id' | 'created_at' | 'updated_at'>): Promise<Status> {
    const response = await api.post('/statuses', status);
    return response.data;
  },

  async updateStatus(id: number, status: Partial<Status>): Promise<Status> {
    const response = await api.put(`/statuses/${id}`, status);
    return response.data;
  },

  async deleteStatus(id: number): Promise<void> {
    await api.delete(`/statuses/${id}`);
  },

  async getStatusesByType(type: Status['tipo']): Promise<Status[]> {
    const response = await api.get(`/statuses/type/${type}`);
    return response.data;
  },

  async getProyectoStatuses(): Promise<Status[]> {
    const response = await api.get('/statuses/type/proyecto');
    return response.data;
  },

  async getProgramaStatuses(): Promise<Status[]> {
    const response = await api.get('/statuses/type/programa');
    return response.data;
  },

  async getReporteStatuses(): Promise<Status[]> {
    const response = await api.get('/statuses/type/reporte');
    return response.data;
  },

  async getExtensionStatuses(): Promise<Status[]> {
    const response = await api.get('/statuses/type/extension');
    return response.data;
  }
}; 