import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar si hay un token guardado al cargar la aplicación
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
      setAuth({ token, user: JSON.parse(user) });
      // Configurar el token en axios para todas las peticiones
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
    setLoading(false);
  }, []);

  const login = async (correo, contraseña) => {
    try {
      // Crear FormData para enviar los datos en el formato correcto
      const formData = new URLSearchParams();
      formData.append('username', correo);
      formData.append('password', contraseña);

      const response = await axios.post('http://localhost:8000/api/v1/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }
      });

      const { access_token } = response.data;
      
      // Obtener información del usuario
      const userResponse = await axios.get('http://localhost:8000/api/v1/usuarios/me', {
        headers: {
          'Authorization': `Bearer ${access_token}`,
          'Accept': 'application/json'
        }
      });
      
      const user = userResponse.data;
      
      // Guardar en localStorage
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      
      // Configurar el token en axios
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Configurar el token en todas las peticiones futuras
      axios.interceptors.request.use(
        (config) => {
          config.headers.Authorization = `Bearer ${access_token}`;
          config.headers.Accept = 'application/json';
          return config;
        },
        (error) => {
          return Promise.reject(error);
        }
      );
      
      setAuth({ token: access_token, user });
      return { access_token, user };
    } catch (error) {
      console.error('Error en login:', error);
      throw error;
    }
  };

  const logout = () => {
    // Limpiar localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    
    // Limpiar el token de axios
    delete axios.defaults.headers.common['Authorization'];
    
    // Limpiar los interceptores
    axios.interceptors.request.handlers = [];
    
    setAuth(null);
  };

  const value = {
    auth,
    isAuthenticated: !!auth,
    loading,
    login,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 