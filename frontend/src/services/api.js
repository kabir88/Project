import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || '/api';

export default {
  // Player endpoints
  searchPlayers(query) {
    return axios.get(`${API_URL}/players/search`, { params: { query } });
  },
  
  getPlayerById(id) {
    return axios.get(`${API_URL}/players/${id}`);
  },
  
  getPlayerStats(id) {
    return axios.get(`${API_URL}/players/${id}/stats`);
  },
  
  // Prediction endpoints
  getPredictions(playerId) {
    return axios.get(`${API_URL}/predictions/${playerId}`);
  },
  
  // Analysis endpoints
  getSavedAnalyses() {
    return axios.get(`${API_URL}/analyses`);
  },
  
  saveAnalysis(analysis) {
    return axios.post(`${API_URL}/analyses`, analysis);
  },
  
  updateAnalysis(id, analysis) {
    return axios.put(`${API_URL}/analyses/${id}`, analysis);
  },
  
  deleteAnalysis(id) {
    return axios.delete(`${API_URL}/analyses/${id}`);
  }
};