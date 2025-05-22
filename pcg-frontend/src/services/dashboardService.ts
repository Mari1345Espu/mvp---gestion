import axios from 'axios';

interface User {
  id: number;
  nombre: string;
  email: string;
  rol: string;
}

interface DashboardStats {
  totalUsers: number;
  activeUsers: number;
  totalProjects: number;
  activeProjects: number;
}

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

const getToken = () => {
  return localStorage.getItem('token');
};

export const getDashboardStats = async (): Promise<DashboardStats> => {
  const token = getToken();
  
  const response = await axios.get(`${API_URL}/dashboard/stats`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const getRecentUsers = async (): Promise<User[]> => {
  const token = getToken();
  
  const response = await axios.get(`${API_URL}/dashboard/recent-users`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const getRecentProjects = async (): Promise<any[]> => {
  const token = getToken();
  
  const response = await axios.get(`${API_URL}/dashboard/recent-projects`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
}; 