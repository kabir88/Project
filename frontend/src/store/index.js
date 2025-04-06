import { createStore } from 'vuex';
import api from '../services/api';

export default createStore({
  state: {
    players: [],
    selectedPlayer: null,
    playerStats: null,
    predictions: null,
    savedAnalyses: [],
    loading: false,
    error: null
  },
  
  getters: {
    allPlayers: state => state.players,
    selectedPlayer: state => state.selectedPlayer,
    playerStats: state => state.playerStats,
    predictions: state => state.predictions,
    allSavedAnalyses: state => state.savedAnalyses,
    isLoading: state => state.loading,
    hasError: state => !!state.error,
    errorMessage: state => state.error
  },
  
  mutations: {
    SET_PLAYERS(state, players) {
      state.players = players;
    },
    
    SET_SELECTED_PLAYER(state, player) {
      state.selectedPlayer = player;
    },
    
    SET_PLAYER_STATS(state, stats) {
      state.playerStats = stats;
    },
    
    SET_PREDICTIONS(state, predictions) {
      state.predictions = predictions;
    },
    
    SET_SAVED_ANALYSES(state, analyses) {
      state.savedAnalyses = analyses;
    },
    
    ADD_SAVED_ANALYSIS(state, analysis) {
      state.savedAnalyses.unshift(analysis);
    },
    
    REMOVE_SAVED_ANALYSIS(state, id) {
      state.savedAnalyses = state.savedAnalyses.filter(analysis => analysis._id !== id);
    },
    
    SET_LOADING(state, status) {
      state.loading = status;
    },
    
    SET_ERROR(state, error) {
      state.error = error;
    }
  },
  
  actions: {
    async searchPlayers({ commit }, query) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      
      try {
        const response = await api.searchPlayers(query);
        commit('SET_PLAYERS', response.data);
      } catch (error) {
        commit('SET_ERROR', 'Failed to search players. Please try again.');
        console.error('Search players error:', error);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    async getPlayerStats({ commit }, playerId) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      
      try {
        const response = await api.getPlayerStats(playerId);
        commit('SET_PLAYER_STATS', response.data);
      } catch (error) {
        commit('SET_ERROR', 'Failed to load player statistics. Please try again.');
        console.error('Get player stats error:', error);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    async getPredictions({ commit }, playerId) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      
      try {
        const response = await api.getPredictions(playerId);
        commit('SET_PREDICTIONS', response.data);
      } catch (error) {
        commit('SET_ERROR', 'Failed to generate predictions. Please try again.');
        console.error('Get predictions error:', error);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    async getSavedAnalyses({ commit }) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      
      try {
        const response = await api.getSavedAnalyses();
        commit('SET_SAVED_ANALYSES', response.data);
      } catch (error) {
        commit('SET_ERROR', 'Failed to load saved analyses. Please try again.');
        console.error('Get saved analyses error:', error);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    async saveAnalysis({ commit }, analysis) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      
      try {
        const response = await api.saveAnalysis(analysis);
        commit('ADD_SAVED_ANALYSIS', response.data);
        return response.data;
      } catch (error) {
        commit('SET_ERROR', 'Failed to save analysis. Please try again.');
        console.error('Save analysis error:', error);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    async deleteAnalysis({ commit }, id) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      
      try {
        await api.deleteAnalysis(id);
        commit('REMOVE_SAVED_ANALYSIS', id);
      } catch (error) {
        commit('SET_ERROR', 'Failed to delete analysis. Please try again.');
        console.error('Delete analysis error:', error);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    selectPlayer({ commit }, player) {
      commit('SET_SELECTED_PLAYER', player);
    },
    
    clearError({ commit }) {
      commit('SET_ERROR', null);
    }
  }
});