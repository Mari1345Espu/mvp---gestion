import axios from 'axios';

export const login = async (email: string, password: string) => {
  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', password);
  
  const response = await axios.post('/api/v1/token', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  
  return response.data;
};

export const register = async (email: string, password: string, name: string) => {
  const response = await axios.post('/api/v1/register', {
    nombre: name,
    correo: email,
    contraseña: password,
  });
  
  return response.data;
}; 