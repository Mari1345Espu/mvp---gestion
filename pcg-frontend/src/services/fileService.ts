import api from './api';

export interface FileUploadResponse {
  url: string;
  filename: string;
  size: number;
  mimeType: string;
}

export const fileService = {
  async uploadFile(file: File, type: 'avatar' | 'document' | 'image'): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);

    const response = await api.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  async deleteFile(filename: string): Promise<void> {
    await api.delete(`/files/${filename}`);
  },

  async getFileUrl(filename: string): Promise<string> {
    const response = await api.get(`/files/${filename}/url`);
    return response.data.url;
  },

  async getFileInfo(filename: string): Promise<FileUploadResponse> {
    const response = await api.get(`/files/${filename}/info`);
    return response.data;
  },

  async getFilesByType(type: 'avatar' | 'document' | 'image'): Promise<FileUploadResponse[]> {
    const response = await api.get(`/files/type/${type}`);
    return response.data;
  },

  async getFilesByUser(userId: number): Promise<FileUploadResponse[]> {
    const response = await api.get(`/files/user/${userId}`);
    return response.data;
  },

  async getFilesByProyecto(proyectoId: number): Promise<FileUploadResponse[]> {
    const response = await api.get(`/files/proyecto/${proyectoId}`);
    return response.data;
  },

  async getFilesByPrograma(programaId: number): Promise<FileUploadResponse[]> {
    const response = await api.get(`/files/programa/${programaId}`);
    return response.data;
  }
}; 