<template>
  <div class="player-search card shadow-sm">
    <div class="card-body">
      <h3 class="card-title">Find Players</h3>
      
      <div class="input-group mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search by player name"
          v-model="searchQuery"
          @keyup.enter="performSearch"
        >
        <button 
          class="btn btn-primary" 
          type="button" 
          @click="performSearch"
          :disabled="loading || !searchQuery"
        >
          <i class="fas fa-search"></i>
        </button>
      </div>

      <div v-if="loading" class="text-center my-4">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="players && players.length > 0" class="player-list">
        <div 
          v-for="player in players" 
          :key="player.id"
          class="player-item card mb-2"
          :class="{'selected': isSelected(player)}"
          @click="selectPlayer(player)"
        >
          <div class="card-body py-2 px-3">
            <div class="d-flex align-items-center">
              <div>
                <h5 class="mb-0">{{ player.firstName }} {{ player.lastName }}</h5>
                <small class="text-muted">{{ player.teamName || 'No team' }} | {{ player.position || 'N/A' }}</small>
              </div>
              <div class="ms-auto">
                <i class="fas fa-chevron-right text-muted"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="searched" class="alert alert-info mt-3">
        No players found matching "{{ searchQuery }}"
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'PlayerSearch',
  setup() {
    const store = useStore()
    const searchQuery = ref('')
    const searched = ref(false)

    const players = computed(() => store.getters.allPlayers)
    const currentPlayer = computed(() => store.getters.currentPlayer)
    const loading = computed(() => store.getters.isLoading)

    const performSearch = async () => {
      if (!searchQuery.value.trim()) return
      searched.value = true
      await store.dispatch('searchPlayers', searchQuery.value)
    }

    const selectPlayer = async (player) => {
      store.dispatch('selectPlayer', player)
      await Promise.all([
        store.dispatch('getPlayerStats', player.id),
        store.dispatch('getPredictions', player.id)
      ])
    }

    const isSelected = (player) => {
      return currentPlayer.value && currentPlayer.value.id === player.id
    }

    return {
      searchQuery,
      searched,
      players,
      loading,
      performSearch,
      selectPlayer,
      isSelected
    }
  }
}
</script>

<style scoped>
.player-search {
  height: 100%;
}

.player-list {
  max-height: 400px;
  overflow-y: auto;
}

.player-item {
  cursor: pointer;
  transition: all 0.2s ease;
}

.player-item:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
}

.player-item.selected {
  border-left: 4px solid #007bff;
  background-color: #e8f4ff;
}
</style>
