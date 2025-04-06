<template>
  <div class="saved-analyses">
    <div class="row mb-4">
      <div class="col-12">
        <div class="card shadow-sm">
          <div class="card-body">
            <h1 class="card-title">Saved Analyses</h1>
            <p class="text-muted">Your saved player analyses and predictions</p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading your saved analyses...</p>
    </div>

    <div v-else-if="analyses.length === 0" class="text-center my-5">
      <div class="empty-state">
        <i class="fas fa-folder-open fa-4x text-muted mb-3"></i>
        <h3>No saved analyses yet</h3>
        <p class="text-muted">Search for players and save their analyses to view them here</p>
        <router-link to="/" class="btn btn-primary mt-2">
          <i class="fas fa-search me-2"></i> Search Players
        </router-link>
      </div>
    </div>

    <div v-else class="row">
      <div class="col-md-4 mb-4" v-for="analysis in analyses" :key="analysis._id">
        <div class="card h-100 shadow-sm">
          <div class="card-header d-flex align-items-center">
            <h5 class="mb-0">{{ analysis.playerName }}</h5>
            <button 
              class="btn btn-sm btn-danger ms-auto"
              @click="deleteAnalysis(analysis._id)"
              :disabled="deletingId === analysis._id"
            >
              <i class="fas fa-trash-alt"></i>
            </button>
          </div>
          <div class="card-body">
            <p class="text-muted">
              <i class="far fa-calendar-alt me-1"></i>
              {{ formatDate(analysis.date) }}
            </p>
            
            <div class="mb-3">
              <h6>Key Stats</h6>
              <div class="row g-2">
                <div class="col-4" v-for="(stat, key) in getKeyStats(analysis.stats)" :key="key">
                  <div class="small-stat-card">
                    <div class="small-stat-label">{{ key }}</div>
                    <div class="small-stat-value">{{ stat }}</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="analysis.predictions">
              <h6>Predictions</h6>
              <div class="alert alert-primary">
                <p class="mb-1"><strong>Next Game</strong></p>
                <p class="mb-0">
                  <span class="me-2">{{ formatStat(analysis.predictions.nextGame.points) }} PTS</span>
                  <span class="me-2">{{ formatStat(analysis.predictions.nextGame.rebounds) }} REB</span>
                  <span>{{ formatStat(analysis.predictions.nextGame.assists) }} AST</span>
                </p>
              </div>
            </div>
            
            <router-link :to="`/player/${analysis.playerId}`" class="btn btn-outline-primary mt-2 w-100">
              View Full Analysis
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Alert -->
    <div v-if="hasError" class="alert alert-danger alert-dismissible fade show mt-3" role="alert">
      {{ errorMessage }}
      <button type="button" class="btn-close" @click="clearError"></button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'SavedAnalyses',
  setup() {
    const store = useStore()
    const deletingId = ref(null)

    const analyses = computed(() => store.getters.allSavedAnalyses)
    const loading = computed(() => store.getters.isLoading)
    const hasError = computed(() => store.getters.hasError)
    const errorMessage = computed(() => store.getters.errorMessage)

    onMounted(() => {
      store.dispatch('getSavedAnalyses')
    })

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    const getKeyStats = (stats) => {
      if (!stats) return {}
      
      return {
        'PPG': stats.pointsPerGame ? stats.pointsPerGame.toFixed(1) : 'N/A',
        'RPG': stats.reboundsPerGame ? stats.reboundsPerGame.toFixed(1) : 'N/A',
        'APG': stats.assistsPerGame ? stats.assistsPerGame.toFixed(1) : 'N/A',
        'FG%': stats.fieldGoalPercentage ? (stats.fieldGoalPercentage * 100).toFixed(1) + '%' : 'N/A',
        'STL': stats.stealsPerGame ? stats.stealsPerGame.toFixed(1) : 'N/A',
        'BLK': stats.blocksPerGame ? stats.blocksPerGame.toFixed(1) : 'N/A'
      }
    }

    const formatStat = (value) => {
      if (value === undefined || value === null) return 'N/A'
      return value.toFixed(1)
    }

    const deleteAnalysis = async (id) => {
      if (confirm('Are you sure you want to delete this analysis?')) {
        deletingId.value = id
        await store.dispatch('deleteAnalysis', id)
        deletingId.value = null
      }
    }

    const clearError = () => {
      store.dispatch('clearError')
    }

    return {
      analyses,
      loading,
      hasError,
      errorMessage,
      deletingId,
      formatDate,
      getKeyStats,
      formatStat,
      deleteAnalysis,
      clearError
    }
  }
}
</script>

<style scoped>
.empty-state {
  padding: 40px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.small-stat-card {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 6px;
  text-align: center;
  height: 100%;
}

.small-stat-label {
  font-size: 0.7rem;
  font-weight: 500;
  text-transform: uppercase;
  color: #6c757d;
}

.small-stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #212529;
}
</style>
