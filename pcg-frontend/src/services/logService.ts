import api from './api';

export interface Log {
  id: number;
  nivel: 'info' | 'warning' | 'error' | 'debug';
  mensaje: string;
  contexto: string;
  usuario_id?: number;
  ip: string;
  user_agent: string;
  created_at: string;
}

export interface LogResponse {
  data: Log[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export const logService = {
  async getLogs(page = 1, limit = 10): Promise<LogResponse> {
    const response = await api.get('/logs', {
      params: { page, limit }
    });
    return response.data;
  },

  async getLog(id: number): Promise<Log> {
    const response = await api.get(`/logs/${id}`);
    return response.data;
  },

  async getLogsByLevel(level: Log['nivel'], page = 1, limit = 10): Promise<LogResponse> {
    const response = await api.get(`/logs/level/${level}`, {
      params: { page, limit }
    });
    return response.data;
  },

  async getLogsByContext(context: string, page = 1, limit = 10): Promise<LogResponse> {
    const response = await api.get(`/logs/context/${context}`, {
      params: { page, limit }
    });
    return response.data;
  },

  async getLogsByUser(userId: number, page = 1, limit = 10): Promise<LogResponse> {
    const response = await api.get(`/logs/user/${userId}`, {
      params: { page, limit }
    });
    return response.data;
  },

  async getLogsByDateRange(startDate: string, endDate: string, page = 1, limit = 10): Promise<LogResponse> {
    const response = await api.get('/logs/date-range', {
      params: { start_date: startDate, end_date: endDate, page, limit }
    });
    return response.data;
  },

  async getLogsByIp(ip: string, page = 1, limit = 10): Promise<LogResponse> {
    const response = await api.get(`/logs/ip/${ip}`, {
      params: { page, limit }
    });
    return response.data;
  },

  async getLogsByUserAgent(userAgent: string, page = 1, limit = 10): Promise<LogResponse> {
    const response = await api.get(`/logs/user-agent/${userAgent}`, {
      params: { page, limit }
    });
    return response.data;
  },

  async deleteLog(id: number): Promise<void> {
    await api.delete(`/logs/${id}`);
  },

  async deleteLogsByLevel(level: Log['nivel']): Promise<void> {
    await api.delete(`/logs/level/${level}`);
  },

  async deleteLogsByContext(context: string): Promise<void> {
    await api.delete(`/logs/context/${context}`);
  },

  async deleteLogsByUser(userId: number): Promise<void> {
    await api.delete(`/logs/user/${userId}`);
  },

  async deleteLogsByDateRange(startDate: string, endDate: string): Promise<void> {
    await api.delete('/logs/date-range', {
      params: { start_date: startDate, end_date: endDate }
    });
  }
}; 