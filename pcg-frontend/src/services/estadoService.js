import axios from 'axios';

const API_URL = '/estados/';

const getEstados = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

const getEstado = async (id) => {
  const response = await axios.get(`${API_URL}${id}`);
  return response.data;
};

const createEstado = async (estado) => {
  const response = await axios.post(API_URL, estado);
  return response.data;
};

const updateEstado = async (id, estado) => {
  const response = await axios.put(`${API_URL}${id}`, estado);
  return response.data;
};

const deleteEstado = async (id) => {
  const response = await axios.delete(`${API_URL}${id}`);
  return response.data;
};

export default {
  getEstados,
  getEstado,
  createEstado,
  updateEstado,
  deleteEstado,
};
