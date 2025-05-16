import axios from 'axios';

const API_URL = '/api/v1/usuarios/';

const getUsuarios = async (filters = {}) => {
  const params = new URLSearchParams();
  if (filters.nombre) params.append('nombre', filters.nombre);
  if (filters.correo) params.append('correo', filters.correo);
  if (filters.rol_id) params.append('rol_id', filters.rol_id);
  const response = await axios.get(API_URL, { params: params });
  return response.data;
};

const getUsuario = async (id) => {
  const response = await axios.get(API_URL + id);
  return response.data;
};

const createUsuario = async (usuario) => {
  const response = await axios.post(API_URL, usuario);
  return response.data;
};

const updateUsuario = async (id, usuario) => {
  const response = await axios.put(API_URL + id, usuario);
  return response.data;
};

const deleteUsuario = async (id) => {
  const response = await axios.delete(API_URL + id);
  return response.data;
};

export default {
  getUsuarios,
  getUsuario,
  createUsuario,
  updateUsuario,
  deleteUsuario,
};
