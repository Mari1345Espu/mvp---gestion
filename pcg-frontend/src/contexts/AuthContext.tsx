import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';
import { User, LoginCredentials, RegisterData } from '../types';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isAdmin: boolean;
  setUser: (user: User | null) => void;
  updateProfile: (data: Partial<User>) => Promise<void>;
  changePassword: (userId: number, currentPassword: string, newPassword: string) => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      authService.getCurrentUser()
        .then(user => {
          setUser(user);
        })
        .catch(() => {
          localStorage.removeItem('token');
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      setError(null);
      const { token, user } = await authService.login(credentials.email, credentials.password);
      localStorage.setItem('token', token);
      setUser(user);
    } catch (err) {
      setError('Credenciales inválidas');
      throw err;
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      setError(null);
      const { token, user } = await authService.register(userData);
      localStorage.setItem('token', token);
      setUser(user);
    } catch (err) {
      setError('Error al registrar usuario');
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const updateProfile = async (data: Partial<User>) => {
    try {
      setError(null);
      const updatedUser = await authService.updateProfile(data);
      setUser(updatedUser);
    } catch (err) {
      setError('Error al actualizar el perfil');
      throw err;
    }
  };

  const changePassword = async (userId: number, currentPassword: string, newPassword: string) => {
    try {
      setError(null);
      await authService.changePassword(userId.toString(), currentPassword, newPassword);
    } catch (err) {
      setError('Error al cambiar la contraseña');
      throw err;
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    isAdmin: user?.rol === 'admin',
    setUser,
    updateProfile,
    changePassword,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
