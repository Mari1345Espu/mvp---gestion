import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Crear instancia de axios
const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar el token a las peticiones
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de respuesta
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Si el error es 401 y no es una petición de refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Aquí podrías implementar la lógica de refresh token si es necesario
        // Por ahora, simplemente redirigimos al login
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }

    // Manejar otros errores
    if (error.response?.data?.detail) {
      // Manejar errores de validación de FastAPI
      if (Array.isArray(error.response.data.detail)) {
        const errorMessage = error.response.data.detail
          .map((err: any) => `${err.loc.join('.')}: ${err.msg}`)
          .join(', ');
        return Promise.reject(new Error(errorMessage));
      }
      return Promise.reject(new Error(error.response.data.detail));
    }

    if (error.response?.data?.message) {
      return Promise.reject(new Error(error.response.data.message));
    }

    return Promise.reject(error);
  }
);

export default axiosInstance; 