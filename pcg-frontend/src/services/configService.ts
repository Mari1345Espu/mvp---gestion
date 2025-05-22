import api from './api';

export interface Config {
  id: number;
  clave: string;
  valor: string;
  descripcion: string;
  tipo: 'string' | 'number' | 'boolean' | 'json';
  created_at: string;
  updated_at: string;
}

export const configService = {
  async getConfigs(): Promise<Config[]> {
    const response = await api.get('/configs');
    return response.data;
  },

  async getConfig(key: string): Promise<Config> {
    const response = await api.get(`/configs/${key}`);
    return response.data;
  },

  async createConfig(config: Omit<Config, 'id' | 'created_at' | 'updated_at'>): Promise<Config> {
    const response = await api.post('/configs', config);
    return response.data;
  },

  async updateConfig(key: string, config: Partial<Config>): Promise<Config> {
    const response = await api.put(`/configs/${key}`, config);
    return response.data;
  },

  async deleteConfig(key: string): Promise<void> {
    await api.delete(`/configs/${key}`);
  },

  async getConfigValue(key: string): Promise<string> {
    const response = await api.get(`/configs/${key}/value`);
    return response.data.value;
  },

  async setConfigValue(key: string, value: string): Promise<void> {
    await api.put(`/configs/${key}/value`, { value });
  },

  async getConfigsByType(type: Config['tipo']): Promise<Config[]> {
    const response = await api.get(`/configs/type/${type}`);
    return response.data;
  },

  async getStringConfigs(): Promise<Config[]> {
    const response = await api.get('/configs/type/string');
    return response.data;
  },

  async getNumberConfigs(): Promise<Config[]> {
    const response = await api.get('/configs/type/number');
    return response.data;
  },

  async getBooleanConfigs(): Promise<Config[]> {
    const response = await api.get('/configs/type/boolean');
    return response.data;
  },

  async getJsonConfigs(): Promise<Config[]> {
    const response = await api.get('/configs/type/json');
    return response.data;
  }
}; 