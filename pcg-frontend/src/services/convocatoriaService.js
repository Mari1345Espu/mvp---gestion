import axios from 'axios';

const API_URL = '/convocatorias/';

const getConvocatorias = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

const getConvocatoria = async (id) => {
  const response = await axios.get(`${API_URL}${id}`);
  return response.data;
};

const createConvocatoria = async (convocatoria) => {
  const response = await axios.post(API_URL, convocatoria);
  return response.data;
};

const updateConvocatoria = async (id, convocatoria) => {
  const response = await axios.put(`${API_URL}${id}`, convocatoria);
  return response.data;
};

const deleteConvocatoria = async (id) => {
  const response = await axios.delete(`${API_URL}${id}`);
  return response.data;
};

export default {
  getConvocatorias,
  getConvocatoria,
  createConvocatoria,
  updateConvocatoria,
  deleteConvocatoria,
};
