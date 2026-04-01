/**
 * Configuração de ambiente
 * Em produção: usa a mesma domain que o frontend
 * Em desenvolvimento: usa localhost:5000
 */

export const API_URL = 
  process.env.NODE_ENV === 'production' 
    ? `${window.location.protocol}//${window.location.host}` 
    : 'http://localhost:5000';

export const API_ENDPOINTS = {
  ENVIAR_MANUTENCAO: `${API_URL}/api/manutencao/enviar`,
  DOWNLOAD_EXCEL: `${API_URL}/api/download-excel`,
  HEALTH: `${API_URL}/api/health`,
};

export default API_URL;
