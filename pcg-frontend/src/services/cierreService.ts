import axiosInstance from './axiosConfig';
import { Cierre, PaginatedResponse } from '../types';

export const getCierres = async (): Promise<PaginatedResponse<Cierre>> => {
  const response = await axiosInstance.get<PaginatedResponse<Cierre>>('/cierres');
  return response.data;
};

export const getCierre = async (id: number): Promise<Cierre> => {
  const response = await axiosInstance.get<Cierre>(`/cierres/${id}`);
  return response.data;
};

export const createCierre = async (cierre: Omit<Cierre, 'id'>): Promise<Cierre> => {
  const response = await axiosInstance.post<Cierre>('/cierres', cierre);
  return response.data;
};

export const updateCierre = async (id: number, cierre: Partial<Cierre>): Promise<Cierre> => {
  const response = await axiosInstance.put<Cierre>(`/cierres/${id}`, cierre);
  return response.data;
};

export const deleteCierre = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/cierres/${id}`);
};

export const getCierresByProyecto = async (proyectoId: number): Promise<Cierre[]> => {
  const response = await axiosInstance.get<Cierre[]>(`/cierres/proyecto/${proyectoId}`);
  return response.data;
};

export const getCierresByTipo = async (tipo: string): Promise<Cierre[]> => {
  const response = await axiosInstance.get<Cierre[]>(`/cierres/tipo/${tipo}`);
  return response.data;
};

export const getCierresByEstado = async (estado: string): Promise<Cierre[]> => {
  const response = await axiosInstance.get<Cierre[]>(`/cierres/estado/${estado}`);
  return response.data;
};

export const getCierresByAprobador = async (aprobadorId: number): Promise<Cierre[]> => {
  const response = await axiosInstance.get<Cierre[]>(`/cierres/aprobador/${aprobadorId}`);
  return response.data;
};

export const getCierresByFecha = async (fechaInicio: string, fechaFin: string): Promise<Cierre[]> => {
  const response = await axiosInstance.get<Cierre[]>(`/cierres/fecha`, {
    params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin }
  });
  return response.data;
};

export const aprobarCierre = async (id: number): Promise<Cierre> => {
  const response = await axiosInstance.post<Cierre>(`/cierres/${id}/aprobar`);
  return response.data;
};

export const rechazarCierre = async (id: number, motivo: string): Promise<Cierre> => {
  const response = await axiosInstance.post<Cierre>(`/cierres/${id}/rechazar`, { motivo });
  return response.data;
}; 