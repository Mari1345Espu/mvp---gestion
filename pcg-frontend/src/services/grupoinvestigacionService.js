import axios from 'axios';

const API_URL = '/grupoinvestigacion/';

const getGrupos = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

const getGrupo = async (id) => {
  const response = await axios.get(API_URL + id);
  return response.data;
};

const createGrupo = async (grupo) => {
  const response = await axios.post(API_URL, grupo);
  return response.data;
};

const updateGrupo = async (id, grupo) => {
  const response = await axios.put(API_URL + id, grupo);
  return response.data;
};

const deleteGrupo = async (id) => {
  const response = await axios.delete(API_URL + id);
  return response.data;
};

export default {
  getGrupos,
  getGrupo,
  createGrupo,
  updateGrupo,
  deleteGrupo,
};
