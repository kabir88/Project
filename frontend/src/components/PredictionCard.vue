<template>
  <div class="prediction-card">
    <h4 class="mb-3">Performance Predictions</h4>
    
    <div v-if="!predictions || Object.keys(predictions).length === 0" class="alert alert-info">
      No predictions available for this player
    </div>
    
    <div v-else>
      <div class="card mb-3">
        <div class="card-header bg-primary text-white">
          <h5 class="mb-0">Next Game Prediction</h5>
        </div>
        <div class="card-body">
          <div class="row g-2">
            <div class="col-6">
              <div class="prediction-stat">
                <div class="prediction-label">Points</div>
                <div class="prediction-value">
                  {{ formatStat(predictions.nextGame.points) }}
                  <small 
                    :class="getConfidenceClass(predictions.confidence.points)"
                    class="ms-1"
                  >
                    {{ formatConfidence(predictions.confidence.points) }}
                  </small>
                </div>
              </div>
            </div>
            <div class="col-6">
              <div class="prediction-stat">
                <div class="prediction-label">Rebounds</div>
                <div class="prediction-value">
                  {{ formatStat(predictions.nextGame.rebounds) }}
                  <small 
                    :class="getConfidenceClass(predictions.confidence.rebounds)"
                    class="ms-1"
                  >
                    {{ formatConfidence(predictions.confidence.rebounds) }}
                  </small>
                </div>
              </div>
            </div>
            <div class="col-6">
              <div class="prediction-stat">
                <div class="prediction-label">Assists</div>
                <div class="prediction-value">
                  {{ formatStat(predictions.nextGame.assists) }}
                  <small 
                    :class="getConfidenceClass(predictions.confidence.assists)"
                    class="ms-1"
                  >
                    {{ formatConfidence(predictions.confidence.assists) }}
                  </small>
                </div>
              </div>
            </div>
            <div class="col-6">
              <div class="prediction-stat">
                <div class="prediction-label">FG%</div>
                <div class="prediction-value">
                  {{ formatPercentage(predictions.nextGame.fieldGoalPercentage) }}
                  <small 
                    :class="getConfidenceClass(predictions.confidence.fieldGoalPercentage)"
                    class="ms-1"
                  >
                    {{ formatConfidence(predictions.confidence.fieldGoalPercentage) }}
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header bg-info text-white">
          <h5 class="mb-0">Season Trend</h5>
        </div>
        <div class="card-body">
          <table class="table table-sm">
            <tbody>
              <tr v-for="(value, key) in predictions.seasonTrend" :key="key">
                <td class="text-capitalize">{{ formatTrendKey(key) }}</td>
                <td>
                  <div class="d-flex align-items-center">
                    <i 
                      :class="getTrendIcon(value)" 
                      :style="{ color: getTrendColor(value) }"
                      class="me-2"
                    ></i>
                    {{ formatTrend(value) }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PredictionCard',
  props: {
    predictions: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatStat(value) {
      if (value === undefined || value === null) return 'N/A'
      return value.toFixed(1)
    },
    formatPercentage(value) {
      if (value === undefined || value === null) return 'N/A'
      return (value * 100).toFixed(1) + '%'
    },
    formatConfidence(value) {
      if (value === undefined || value === null) return ''
      return `(${(value * 100).toFixed(0)}%)`
    },
    getConfidenceClass(value) {
      if (value === undefined || value === null) return ''
      if (value >= 0.7) return 'text-success'
      if (value >= 0.4) return 'text-warning'
      return 'text-danger'
    },
    formatTrendKey(key) {
      return key.replace(/([A-Z])/g, ' $1').toLowerCase()
    },
    formatTrend(value) {
      if (value > 0.3) return 'Improving'
      if (value > 0.1) return 'Slightly improving'
      if (value >= -0.1) return 'Stable'
      if (value >= -0.3) return 'Slightly declining'
      return 'Declining'
    },
    getTrendIcon(value) {
      if (value > 0.3) return 'fas fa-arrow-up'
      if (value > 0.1) return 'fas fa-arrow-up'
      if (value >= -0.1) return 'fas fa-minus'
      if (value >= -0.3) return 'fas fa-arrow-down'
      return 'fas fa-arrow-down'
    },
    getTrendColor(value) {
      if (value > 0.3) return '#28a745'
      if (value > 0.1) return '#28a745'
      if (value >= -0.1) return '#6c757d'
      if (value >= -0.3) return '#dc3545'
      return '#dc3545'
    }
  }
}
</script>

<style scoped>
.prediction-card {
  height: 100%;
}

.prediction-stat {
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 10px;
  text-align: center;
  height: 100%;
}

.prediction-label {
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
  color: #6c757d;
}

.prediction-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: #212529;
}
</style>
