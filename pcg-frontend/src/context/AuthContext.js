import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState({
    accessToken: localStorage.getItem('access_token') || null,
    user: null,
    role: null,
  });

  useEffect(() => {
    if (auth.accessToken) {
      try {
        const decoded = jwtDecode(auth.accessToken);
        setAuth((prev) => ({
          ...prev,
          user: { correo: decoded.sub },
          role: decoded.role,
        }));
      } catch (e) {
        console.error('Invalid token');
        setAuth({ accessToken: null, user: null, role: null });
      }
    }
  }, [auth.accessToken]);

  const login = async (correo, contraseña) => {
    const params = new URLSearchParams();
    params.append('username', correo);
    params.append('password', contraseña);

    const response = await axios.post('http://localhost:8000/api/v1/token', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    const { access_token } = response.data;
    localStorage.setItem('access_token', access_token);
    const decoded = jwtDecode(access_token);
    setAuth({
      accessToken: access_token,
      user: { correo: decoded.sub },
      role: decoded.role,
    });
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setAuth({ accessToken: null, user: null, role: null });
  };

  const isAuthenticated = !!auth.accessToken;

  return (
    <AuthContext.Provider value={{ auth, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};
