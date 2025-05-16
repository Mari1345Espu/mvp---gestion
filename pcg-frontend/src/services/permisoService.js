import axios from 'axios';

const API_URL = '/permisos/';

const getPermisos = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

const getPermiso = async (id) => {
  const response = await axios.get(`${API_URL}${id}`);
  return response.data;
};

const createPermiso = async (permiso) => {
  const response = await axios.post(API_URL, permiso);
  return response.data;
};

const updatePermiso = async (id, permiso) => {
  const response = await axios.put(`${API_URL}${id}`, permiso);
  return response.data;
};

const deletePermiso = async (id) => {
  const response = await axios.delete(`${API_URL}${id}`);
  return response.data;
};

export default {
  getPermisos,
  getPermiso,
  createPermiso,
  updatePermiso,
  deletePermiso,
};
