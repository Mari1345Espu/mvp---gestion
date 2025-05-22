import api from './api';

export interface Activity {
  id: number;
  tipo: 'create' | 'update' | 'delete' | 'login' | 'logout' | 'other';
  descripcion: string;
  usuario_id: number;
  usuario?: {
    id: number;
    nombre: string;
    email: string;
  };
  entidad_tipo: 'proyecto' | 'programa' | 'reporte' | 'extension' | 'usuario' | 'other';
  entidad_id: number;
  cambios?: {
    campo: string;
    valor_anterior: any;
    valor_nuevo: any;
  }[];
  ip: string;
  user_agent: string;
  created_at: string;
}

export interface ActivityResponse {
  data: Activity[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export const activityService = {
  async getActivities(page = 1, limit = 10): Promise<ActivityResponse> {
    const response = await api.get('/activities', {
      params: { page, limit }
    });
    return response.data;
  },

  async getActivity(id: number): Promise<Activity> {
    const response = await api.get(`/activities/${id}`);
    return response.data;
  },

  async getActivitiesByType(type: Activity['tipo'], page = 1, limit = 10): Promise<ActivityResponse> {
    const response = await api.get(`/activities/type/${type}`, {
      params: { page, limit }
    });
    return response.data;
  },

  async getActivitiesByUser(userId: number, page = 1, limit = 10): Promise<ActivityResponse> {
    const response = await api.get(`/activities/user/${userId}`, {
      params: { page, limit }
    });
    return response.data;
  },

  async getActivitiesByEntity(entityType: Activity['entidad_tipo'], entityId: number, page = 1, limit = 10): Promise<ActivityResponse> {
    const response = await api.get(`/activities/entity/${entityType}/${entityId}`, {
      params: { page, limit }
    });
    return response.data;
  },

  async getActivitiesByDateRange(startDate: string, endDate: string, page = 1, limit = 10): Promise<ActivityResponse> {
    const response = await api.get('/activities/date-range', {
      params: { start_date: startDate, end_date: endDate, page, limit }
    });
    return response.data;
  },

  async getActivitiesByIp(ip: string, page = 1, limit = 10): Promise<ActivityResponse> {
    const response = await api.get(`/activities/ip/${ip}`, {
      params: { page, limit }
    });
    return response.data;
  },

  async getActivitiesByUserAgent(userAgent: string, page = 1, limit = 10): Promise<ActivityResponse> {
    const response = await api.get(`/activities/user-agent/${userAgent}`, {
      params: { page, limit }
    });
    return response.data;
  },

  async deleteActivity(id: number): Promise<void> {
    await api.delete(`/activities/${id}`);
  },

  async deleteActivitiesByType(type: Activity['tipo']): Promise<void> {
    await api.delete(`/activities/type/${type}`);
  },

  async deleteActivitiesByUser(userId: number): Promise<void> {
    await api.delete(`/activities/user/${userId}`);
  },

  async deleteActivitiesByEntity(entityType: Activity['entidad_tipo'], entityId: number): Promise<void> {
    await api.delete(`/activities/entity/${entityType}/${entityId}`);
  },

  async deleteActivitiesByDateRange(startDate: string, endDate: string): Promise<void> {
    await api.delete('/activities/date-range', {
      params: { start_date: startDate, end_date: endDate }
    });
  }
}; 