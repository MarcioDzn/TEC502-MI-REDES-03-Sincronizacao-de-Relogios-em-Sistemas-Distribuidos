// services/clockService.js
import axios from 'axios';

const BASE_ENDPOINT = '/v1/api';

export const getClock = async (ip) => {
  try {
    const response = await axios.get(`http://${ip}${BASE_ENDPOINT}`, {
      timeout: 2000 // Tempo máximo em milissegundos (ex: 2000 ms = 2 segundos)
    });
    return { ip, data: response.data, error: null };
  } catch (error) {
    return {
      ip,
      data: null,
      error: error.code === 'ECONNABORTED' ? 'Request timeout' : error.response?.data?.message || 'Failed to fetch clock data'
    };
  }
};
