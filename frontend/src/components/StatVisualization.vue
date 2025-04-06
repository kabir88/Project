<template>
  <div class="stat-visualization">
    <div class="mb-4">
      <div class="d-flex align-items-center mb-3">
        <h5 class="mb-0">Performance Metrics</h5>
        <div class="ms-auto">
          <select class="form-select form-select-sm" v-model="chartType">
            <option value="radar">Radar Chart</option>
            <option value="bar">Bar Chart</option>
            <option value="line">Line Chart</option>
          </select>
        </div>
      </div>
      
      <div class="chart-container">
        <canvas ref="performanceChart"></canvas>
      </div>
    </div>

    <div v-if="hasGameByGameData" class="mt-4">
      <h5 class="mb-3">Game-by-Game Performance</h5>
      <div class="chart-container">
        <canvas ref="gameByGameChart"></canvas>
      </div>
    </div>
    
    <div v-if="hasAdvancedStats" class="mt-4">
      <h5 class="mb-3">Advanced Metrics</h5>
      <div class="chart-container">
        <canvas ref="advancedChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'StatVisualization',
  props: {
    stats: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const performanceChart = ref(null)
    const gameByGameChart = ref(null)
    const advancedChart = ref(null)
    const chartType = ref('radar')
    
    let performanceChartInstance = null
    let gameByGameChartInstance = null
    let advancedChartInstance = null
    
    const hasGameByGameData = computed(() => {
      return props.stats.gameByGame && props.stats.gameByGame.length > 0
    })
    
    const hasAdvancedStats = computed(() => {
      return props.stats.advanced && Object.keys(props.stats.advanced).length > 0
    })
    
    const renderPerformanceChart = () => {
      if (performanceChartInstance) {
        performanceChartInstance.destroy()
      }
      
      const ctx = performanceChart.value.getContext('2d')
      
      const data = {
        labels: [
          'Points', 
          'Rebounds', 
          'Assists', 
          'Steals', 
          'Blocks', 
          'FG%'
        ],
        datasets: [{
          label: 'Player Performance',
          data: [
            props.stats.pointsPerGame || 0,
            props.stats.reboundsPerGame || 0,
            props.stats.assistsPerGame || 0,
            props.stats.stealsPerGame || 0,
            props.stats.blocksPerGame || 0,
            props.stats.fieldGoalPercentage ? props.stats.fieldGoalPercentage * 100 : 0
          ],
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgb(54, 162, 235)',
          borderWidth: 2,
          pointBackgroundColor: 'rgb(54, 162, 235)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgb(54, 162, 235)'
        }]
      }
      
      const config = {
        type: chartType.value,
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: chartType.value !== 'radar' ? {
            y: {
              beginAtZero: true
            }
          } : undefined,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  let label = context.dataset.label || '';
                  if (label) {
                    label += ': ';
                  }
                  if (context.parsed !== null) {
                    label += context.formattedValue;
                  }
                  return label;
                }
              }
            }
          }
        }
      }
      
      performanceChartInstance = new Chart(ctx, config)
    }
    
    const renderGameByGameChart = () => {
      if (!hasGameByGameData.value) return
      
      if (gameByGameChartInstance) {
        gameByGameChartInstance.destroy()
      }
      
      const ctx = gameByGameChart.value.getContext('2d')
      
      // Use the last 10 games or all if fewer
      const gameData = props.stats.gameByGame.slice(-10)
      
      const data = {
        labels: gameData.map(game => game.opponent || game.date || `Game ${game.gameId}`),
        datasets: [
          {
            label: 'Points',
            data: gameData.map(game => game.points || 0),
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)'
          },
          {
            label: 'Rebounds',
            data: gameData.map(game => game.rebounds || 0),
            borderColor: 'rgb(54, 162, 235)',
            backgroundColor: 'rgba(54, 162, 235, 0.5)'
          },
          {
            label: 'Assists',
            data: gameData.map(game => game.assists || 0),
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.5)'
          }
        ]
      }
      
      const config = {
        type: 'line',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Recent Game Performance'
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      }
      
      gameByGameChartInstance = new Chart(ctx, config)
    }
    
    const renderAdvancedChart = () => {
      if (!hasAdvancedStats.value) return
      
      if (advancedChartInstance) {
        advancedChartInstance.destroy()
      }
      
      const ctx = advancedChart.value.getContext('2d')
      const advancedStats = props.stats.advanced
      
      const data = {
        labels: Object.keys(advancedStats),
        datasets: [{
          label: 'Advanced Metrics',
          data: Object.values(advancedStats),
          backgroundColor: [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
            'rgba(153, 102, 255, 0.6)',
            'rgba(255, 159, 64, 0.6)',
            'rgba(199, 199, 199, 0.6)'
          ],
          borderWidth: 1
        }]
      }
      
      const config = {
        type: 'polarArea',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
            },
            title: {
              display: true,
              text: 'Advanced Metrics'
            }
          }
        }
      }
      
      advancedChartInstance = new Chart(ctx, config)
    }
    
    onMounted(() => {
      renderPerformanceChart()
      renderGameByGameChart()
      renderAdvancedChart()
    })
    
    watch(() => props.stats, () => {
      renderPerformanceChart()
      renderGameByGameChart()
      renderAdvancedChart()
    }, { deep: true })
    
    watch(chartType, () => {
      renderPerformanceChart()
    })
    
    return {
      performanceChart,
      gameByGameChart,
      advancedChart,
      chartType,
      hasGameByGameData,
      hasAdvancedStats
    }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
</style>
