import api from './api';

export interface Notification {
  id: number;
  titulo: string;
  mensaje: string;
  tipo: 'info' | 'success' | 'warning' | 'error';
  leida: boolean;
  fecha_creacion: string;
  fecha_lectura?: string;
  usuario_id: number;
  proyecto_id?: number;
  programa_id?: number;
  reporte_id?: number;
  extension_id?: number;
}

export interface NotificationResponse {
  data: Notification[];
  total: number;
  unread: number;
}

export const notificationService = {
  async getNotifications(page = 1, limit = 10): Promise<NotificationResponse> {
    const response = await api.get('/notifications', {
      params: { page, limit }
    });
    return response.data;
  },

  async getUnreadNotifications(): Promise<Notification[]> {
    const response = await api.get('/notifications/unread');
    return response.data;
  },

  async markAsRead(id: number): Promise<Notification> {
    const response = await api.put(`/notifications/${id}/read`);
    return response.data;
  },

  async markAllAsRead(): Promise<void> {
    await api.put('/notifications/read-all');
  },

  async deleteNotification(id: number): Promise<void> {
    await api.delete(`/notifications/${id}`);
  },

  async deleteAllNotifications(): Promise<void> {
    await api.delete('/notifications');
  },

  async getNotificationsByUser(userId: number): Promise<Notification[]> {
    const response = await api.get(`/notifications/user/${userId}`);
    return response.data;
  },

  async getNotificationsByProyecto(proyectoId: number): Promise<Notification[]> {
    const response = await api.get(`/notifications/proyecto/${proyectoId}`);
    return response.data;
  },

  async getNotificationsByPrograma(programaId: number): Promise<Notification[]> {
    const response = await api.get(`/notifications/programa/${programaId}`);
    return response.data;
  },

  async getNotificationsByReporte(reporteId: number): Promise<Notification[]> {
    const response = await api.get(`/notifications/reporte/${reporteId}`);
    return response.data;
  },

  async getNotificationsByExtension(extensionId: number): Promise<Notification[]> {
    const response = await api.get(`/notifications/extension/${extensionId}`);
    return response.data;
  }
}; 