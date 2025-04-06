<template>
  <div class="player-stats">
    <h4 class="mb-3">Season Statistics</h4>
    
    <div v-if="!stats || Object.keys(stats).length === 0" class="alert alert-info">
      No statistics available for this player
    </div>
    
    <div v-else>
      <div class="row g-2 mb-3">
        <div class="col-6">
          <div class="stat-card">
            <div class="stat-label">PPG</div>
            <div class="stat-value">{{ formatStat(stats.pointsPerGame) }}</div>
          </div>
        </div>
        <div class="col-6">
          <div class="stat-card">
            <div class="stat-label">RPG</div>
            <div class="stat-value">{{ formatStat(stats.reboundsPerGame) }}</div>
          </div>
        </div>
        <div class="col-6">
          <div class="stat-card">
            <div class="stat-label">APG</div>
            <div class="stat-value">{{ formatStat(stats.assistsPerGame) }}</div>
          </div>
        </div>
        <div class="col-6">
          <div class="stat-card">
            <div class="stat-label">FG%</div>
            <div class="stat-value">{{ formatPercentage(stats.fieldGoalPercentage) }}</div>
          </div>
        </div>
        <div class="col-6">
          <div class="stat-card">
            <div class="stat-label">3P%</div>
            <div class="stat-value">{{ formatPercentage(stats.threePointPercentage) }}</div>
          </div>
        </div>
        <div class="col-6">
          <div class="stat-card">
            <div class="stat-label">FT%</div>
            <div class="stat-value">{{ formatPercentage(stats.freeThrowPercentage) }}</div>
          </div>
        </div>
      </div>

      <table class="table table-sm table-striped">
        <thead>
          <tr>
            <th>Stat</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Games Played</td>
            <td>{{ stats.gamesPlayed || 'N/A' }}</td>
          </tr>
          <tr>
            <td>Minutes Per Game</td>
            <td>{{ formatStat(stats.minutesPerGame) }}</td>
          </tr>
          <tr>
            <td>Steals Per Game</td>
            <td>{{ formatStat(stats.stealsPerGame) }}</td>
          </tr>
          <tr>
            <td>Blocks Per Game</td>
            <td>{{ formatStat(stats.blocksPerGame) }}</td>
          </tr>
          <tr>
            <td>Turnovers Per Game</td>
            <td>{{ formatStat(stats.turnoversPerGame) }}</td>
          </tr>
          <tr>
            <td>Personal Fouls Per Game</td>
            <td>{{ formatStat(stats.personalFoulsPerGame) }}</td>
          </tr>
          <tr>
            <td>Plus Minus</td>
            <td>{{ formatStat(stats.plusMinus, true) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlayerStats',
  props: {
    stats: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatStat(value, allowNegative = false) {
      if (value === undefined || value === null) return 'N/A'
      if (typeof value !== 'number') return value
      
      return value.toFixed(1)
    },
    formatPercentage(value) {
      if (value === undefined || value === null) return 'N/A'
      if (typeof value !== 'number') return value
      
      return (value * 100).toFixed(1) + '%'
    }
  }
}
</script>

<style scoped>
.player-stats {
  height: 100%;
}

.stat-card {
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 10px;
  text-align: center;
  height: 100%;
}

.stat-label {
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
  color: #6c757d;
}

.stat-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: #212529;
}

.table {
  font-size: 0.9rem;
}
</style>
