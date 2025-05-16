import axios from 'axios';

const API_URL = '/roles/';

const getRoles = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

const getRol = async (id) => {
  const response = await axios.get(API_URL + id);
  return response.data;
};

const createRol = async (rol) => {
  const response = await axios.post(API_URL, rol);
  return response.data;
};

const updateRol = async (id, rol) => {
  const response = await axios.put(API_URL + id, rol);
  return response.data;
};

const deleteRol = async (id) => {
  const response = await axios.delete(API_URL + id);
  return response.data;
};

export default {
  getRoles,
  getRol,
  createRol,
  updateRol,
  deleteRol,
};
