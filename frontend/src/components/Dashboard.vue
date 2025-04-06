<template>
  <div class="dashboard">
    <h1>NBA Player Analytics Dashboard</h1>
    <p>Search for NBA players to visualize their stats and performance predictions</p>
    
    <div>
      <label for="playerSearch">Search for a player:</label>
      <input 
        id="playerSearch" 
        type="text" 
        v-model="searchQuery" 
        placeholder="Enter player name" 
        @input="handleSearch"
      />
    </div>

    <div v-if="players.length > 0" class="player-results">
      <h2>Search Results</h2>
      <ul>
        <li v-for="player in players" :key="player.id" @click="selectPlayer(player)">
          {{ player.firstName }} {{ player.lastName }}
        </li>
      </ul>
    </div>

    <div v-if="selectedPlayer" class="player-details">
      <h2>{{ selectedPlayer.firstName }} {{ selectedPlayer.lastName }}</h2>
      <div v-if="loading">Loading player data...</div>
      <div v-else-if="playerStats">
        <h3>Player Statistics</h3>
        <pre>{{ playerStats }}</pre>
        
        <h3>Performance Predictions</h3>
        <pre>{{ predictions }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      searchQuery: '',
      players: [],
      selectedPlayer: null,
      playerStats: null,
      predictions: null,
      loading: false
    }
  },
  methods: {
    async handleSearch() {
      if (this.searchQuery.length < 2) {
        this.players = [];
        return;
      }
      
      try {
        // Simulate API call for player search
        console.log('Searching for players:', this.searchQuery);
        this.players = [
          { id: 1, firstName: 'LeBron', lastName: 'James' },
          { id: 2, firstName: 'Kevin', lastName: 'Durant' },
          { id: 3, firstName: 'Stephen', lastName: 'Curry' }
        ].filter(p => 
          p.firstName.toLowerCase().includes(this.searchQuery.toLowerCase()) || 
          p.lastName.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      } catch (error) {
        console.error('Error searching for players:', error);
      }
    },
    selectPlayer(player) {
      this.selectedPlayer = player;
      this.loading = true;
      
      // Simulate loading player data
      setTimeout(() => {
        this.playerStats = {
          points: 27.5,
          rebounds: 7.4,
          assists: 8.3,
          steals: 1.2,
          blocks: 0.6
        };
        
        this.predictions = {
          nextGame: {
            points: 26.8,
            rebounds: 7.1,
            assists: 8.5
          },
          season: {
            points: 28.2,
            rebounds: 7.6,
            assists: 8.1
          }
        };
        
        this.loading = false;
      }, 1000);
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

input {
  padding: 8px;
  width: 100%;
  margin-bottom: 20px;
}

.player-results ul {
  list-style: none;
  padding: 0;
}

.player-results li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.player-results li:hover {
  background-color: #f5f5f5;
}

.player-details {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
</style>
