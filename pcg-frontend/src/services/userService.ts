import { API_URL } from '../config';
import { User, UserCreate, UserUpdate, PaginatedResponse } from '../types';

class UserService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = `${API_URL}/users`;
  }

  private getToken(): string | null {
    return localStorage.getItem('token');
  }

  async getUsers(page = 1, perPage = 10): Promise<PaginatedResponse<User>> {
    const token = this.getToken();
    if (!token) {
      throw new Error('No hay token de autenticación');
    }

    const response = await fetch(
      `${this.baseUrl}?page=${page}&per_page=${perPage}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error('Error al obtener los usuarios');
    }

    return response.json();
  }

  async createUser(data: UserCreate): Promise<User> {
    const token = this.getToken();
    if (!token) {
      throw new Error('No hay token de autenticación');
    }

    const response = await fetch(this.baseUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Error al crear el usuario');
    }

    return response.json();
  }

  async updateUser(id: number, data: UserUpdate): Promise<User> {
    const token = this.getToken();
    if (!token) {
      throw new Error('No hay token de autenticación');
    }

    const response = await fetch(`${this.baseUrl}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Error al actualizar el usuario');
    }

    return response.json();
  }

  async deleteUser(id: number): Promise<void> {
    const token = this.getToken();
    if (!token) {
      throw new Error('No hay token de autenticación');
    }

    const response = await fetch(`${this.baseUrl}/${id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Error al eliminar el usuario');
    }
  }

  async updateUserStatus(id: number, estado_id: number): Promise<User> {
    const token = this.getToken();
    if (!token) {
      throw new Error('No hay token de autenticación');
    }

    const response = await fetch(`${this.baseUrl}/${id}/status`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ estado_id }),
    });

    if (!response.ok) {
      throw new Error('Error al actualizar el estado del usuario');
    }

    return response.json();
  }

  async updateUserProfile(data: UserUpdate): Promise<User> {
    const token = this.getToken();
    if (!token) {
      throw new Error('No hay token de autenticación');
    }

    const response = await fetch(`${this.baseUrl}/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Error al actualizar el perfil');
    }

    return response.json();
  }

  async uploadAvatar(file: File): Promise<User> {
    const token = this.getToken();
    if (!token) {
      throw new Error('No hay token de autenticación');
    }

    const formData = new FormData();
    formData.append('avatar', file);

    const response = await fetch(`${this.baseUrl}/avatar`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Error al subir el avatar');
    }

    return response.json();
  }

  async getUser(id: number): Promise<User> {
    const token = this.getToken();
    if (!token) {
      throw new Error('No hay token de autenticación');
    }

    const response = await fetch(`${this.baseUrl}/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Error al obtener el usuario');
    }

    return response.json();
  }

  async getUsersByRole(roleId: number): Promise<User[]> {
    const token = this.getToken();
    if (!token) {
      throw new Error('No hay token de autenticación');
    }

    const response = await fetch(`${this.baseUrl}/role/${roleId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Error al obtener los usuarios por rol');
    }

    return response.json();
  }
}

export const userService = new UserService();

export const getUsers = (page = 1, perPage = 10) => userService.getUsers(page, perPage);
export const getUser = (id: number) => userService.getUser(id);
export const createUser = (userData: UserCreate) => userService.createUser(userData);
export const updateUser = (userId: number, userData: UserUpdate) => userService.updateUser(userId, userData);
export const deleteUser = (userId: number) => userService.deleteUser(userId);
export const getUsersByRole = (roleId: number) => userService.getUsersByRole(roleId);
export const updateUserStatus = (userId: number, estado_id: number) => userService.updateUserStatus(userId, estado_id);
export const updateUserProfile = (userData: UserUpdate) => userService.updateUserProfile(userData);
export const uploadAvatar = (file: File) => userService.uploadAvatar(file); 