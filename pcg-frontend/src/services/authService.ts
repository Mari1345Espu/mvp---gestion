import api from './api';
import { User, LoginCredentials, AuthResponse, RegisterData } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await api.post('/auth/login', credentials);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
    }
    return response.data;
  },

  async register(userData: RegisterData): Promise<AuthResponse> {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  async logout(): Promise<void> {
    localStorage.removeItem('token');
    await api.post('/auth/logout');
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/auth/me');
    return response.data;
  },

  async refreshToken(): Promise<AuthResponse> {
    const response = await api.post('/auth/refresh');
    return response.data;
  },

  async forgotPassword(email: string): Promise<void> {
    await api.post('/auth/forgot-password', { email });
  },

  async resetPassword(token: string, password: string): Promise<void> {
    await api.post('/auth/reset-password', { token, password });
  },

  async changePassword(oldPassword: string, newPassword: string): Promise<void> {
    await api.post('/auth/change-password', { oldPassword, newPassword });
  },

  async updateProfile(userData: Partial<User>): Promise<User> {
    const response = await api.put('/auth/profile', userData);
    return response.data;
  },

  async verifyToken(): Promise<AuthResponse> {
    const response = await api.post('/auth/verify', {}, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });
    return response.data;
  },

  async uploadAvatar(userId: number, file: File): Promise<User> {
    const formData = new FormData();
    formData.append('avatar', file);

    const response = await api.post(`${API_URL}/users/${userId}/avatar`, formData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  removeToken(): void {
    localStorage.removeItem('token');
  }
}; 