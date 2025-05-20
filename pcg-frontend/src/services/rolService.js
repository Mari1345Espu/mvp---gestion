import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/roles/';

// Función para obtener el token
const getAuthHeader = () => {
  const token = localStorage.getItem('access_token');
  return {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  };
};

const getRoles = async () => {
  const response = await axios.get(API_URL, getAuthHeader());
  return response.data;
};

const getRol = async (id) => {
  const response = await axios.get(API_URL + id, getAuthHeader());
  return response.data;
};

const createRol = async (rol) => {
  const response = await axios.post(API_URL, rol, getAuthHeader());
  return response.data;
};

const updateRol = async (id, rol) => {
  const response = await axios.put(API_URL + id, rol, getAuthHeader());
  return response.data;
};

const deleteRol = async (id) => {
  const response = await axios.delete(API_URL + id, getAuthHeader());
  return response.data;
};

export default {
  getRoles,
  getRol,
  createRol,
  updateRol,
  deleteRol,
};
