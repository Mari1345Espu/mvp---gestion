import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/convocatorias/';

// Función para obtener el token
const getAuthHeader = () => {
  const token = localStorage.getItem('access_token');
  return {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  };
};

const getConvocatorias = async () => {
  const response = await axios.get(API_URL, getAuthHeader());
  return response.data;
};

const getConvocatoria = async (id) => {
  const response = await axios.get(API_URL + id, getAuthHeader());
  return response.data;
};

const createConvocatoria = async (convocatoria) => {
  const response = await axios.post(API_URL, convocatoria, getAuthHeader());
  return response.data;
};

const updateConvocatoria = async (id, convocatoria) => {
  const response = await axios.put(API_URL + id, convocatoria, getAuthHeader());
  return response.data;
};

const deleteConvocatoria = async (id) => {
  const response = await axios.delete(API_URL + id, getAuthHeader());
  return response.data;
};

export default {
  getConvocatorias,
  getConvocatoria,
  createConvocatoria,
  updateConvocatoria,
  deleteConvocatoria,
};
