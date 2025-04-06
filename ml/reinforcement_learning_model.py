#!/usr/bin/env python3
"""
Reinforcement Learning model for NBA player analysis
This is a simplified reinforcement learning approach for demonstration purposes.
"""

import os
import sys
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Define paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(SCRIPT_DIR, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

# Model file path
RL_MODEL_PATH = os.path.join(MODEL_DIR, 'reinforcement_model.pkl')

class SimplifiedRLModel:
    """
    A simplified RL model that uses Q-learning concepts
    to predict player performance based on game context
    """
    
    def __init__(self, state_size, action_size):
        self.state_size = state_size  # Number of state features
        self.action_size = action_size  # Number of possible actions/predictions
        
        # Initialize Q-table with zeros
        self.q_table = np.zeros((state_size, action_size))
        
        # Hyperparameters
        self.learning_rate = 0.1
        self.gamma = 0.95  # Discount factor
        self.epsilon = 0.1  # Exploration rate
        
        # For tracking performance
        self.performance_history = []
    
    def update(self, state, action, reward, next_state):
        """Update Q-table using Q-learning update rule"""
        # Current Q-value
        q_value = self.q_table[state, action]
        
        # Calculate new Q-value
        max_next_q = np.max(self.q_table[next_state])
        new_q_value = q_value + self.learning_rate * (reward + self.gamma * max_next_q - q_value)
        
        # Update Q-table
        self.q_table[state, action] = new_q_value
    
    def predict(self, state):
        """Make a prediction based on current state"""
        # Epsilon-greedy policy
        if np.random.random() < self.epsilon:
            # Explore: choose random action
            return np.random.randint(self.action_size)
        else:
            # Exploit: choose best action from Q-table
            return np.argmax(self.q_table[state])
    
    def save(self, path):
        """Save model to file"""
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(cls, path):
        """Load model from file"""
        with open(path, 'rb') as f:
            return pickle.load(f)

def discretize_state(player_stats, scaler=None):
    """
    Convert player stats into a discretized state representation
    
    For simplification, we convert continuous values into discrete bins
    """
    # Extract relevant features
    features = [
        player_stats.get('pointsPerGame', 0),
        player_stats.get('reboundsPerGame', 0),
        player_stats.get('assistsPerGame', 0),
        player_stats.get('stealsPerGame', 0),
        player_stats.get('blocksPerGame', 0),
        player_stats.get('fieldGoalPercentage', 0),
        player_stats.get('threePointPercentage', 0),
        player_stats.get('freeThrowPercentage', 0)
    ]
    
    # Convert to numpy array
    state_vector = np.array(features).reshape(1, -1)
    
    # Scale if scaler is provided
    if scaler:
        state_vector = scaler.transform(state_vector)
    
    # Discretize each feature into bins (simplified)
    # In a real implementation, we would use more sophisticated binning
    bins = [3, 3, 3, 2, 2, 3, 3, 3]  # Number of bins for each feature
    
    discretized_state = []
    for i, val in enumerate(state_vector[0]):
        # Convert to bin index
        bin_idx = min(int(val * bins[i]), bins[i] - 1)
        discretized_state.append(bin_idx)
    
    # Return state index (in a real system, this would be a unique state ID)
    # For simplicity, we'll just use the first feature's bin index
    return discretized_state[0]

def predict_with_rl(player_id, player_stats):
    """
    Generate predictions using the RL model
    For demonstration purposes, this is quite simplified
    """
    try:
        # Try to load the RL model
        try:
            model = SimplifiedRLModel.load(RL_MODEL_PATH)
            scaler = None  # In a real implementation, we would also load a scaler
        except:
            # If model doesn't exist, create a simple one
            # In production, you would train this model properly
            model = SimplifiedRLModel(state_size=10, action_size=5)
            scaler = None
        
        # Convert player stats to a state representation
        state = discretize_state(player_stats, scaler)
        
        # Make prediction
        action = model.predict(state)
        
        # Map action to prediction (simplified)
        # In a real implementation, this would be more sophisticated
        base_points = player_stats.get('pointsPerGame', 0)
        base_rebounds = player_stats.get('reboundsPerGame', 0)
        base_assists = player_stats.get('assistsPerGame', 0)
        
        # Action determines performance relative to average
        # 0: below average, 1: average, 2: above average, etc.
        performance_factor = 0.8 + (action * 0.1)  # 0.8, 0.9, 1.0, 1.1, 1.2
        
        predictions = {
            'points': base_points * performance_factor,
            'rebounds': base_rebounds * performance_factor,
            'assists': base_assists * performance_factor,
            'fieldGoalPercentage': min(1.0, player_stats.get('fieldGoalPercentage', 0.45) * performance_factor)
        }
        
        # Calculate confidence based on historical performance reliability
        # This is a placeholder for a real confidence calculation
        confidence = 0.5 + (action * 0.1)  # 0.5-0.9
        
        return {
            'predictions': predictions,
            'confidence': confidence,
            'model_type': 'reinforcement_learning',
            'state': state,
            'action': action
        }
        
    except Exception as e:
        print(f"Error in RL prediction: {str(e)}", file=sys.stderr)
        return {
            'error': str(e),
            'predictions': {
                'points': player_stats.get('pointsPerGame', 0),
                'rebounds': player_stats.get('reboundsPerGame', 0),
                'assists': player_stats.get('assistsPerGame', 0),
                'fieldGoalPercentage': player_stats.get('fieldGoalPercentage', 0.45)
            },
            'confidence': 0.3,
            'model_type': 'fallback'
        }

def main():
    """Main function when script is run directly"""
    if len(sys.argv) < 3:
        print("Usage: python reinforcement_learning_model.py <player_id> <stats_file>")
        sys.exit(1)
    
    player_id = sys.argv[1]
    stats_file = sys.argv[2]
    
    try:
        # Load player stats
        with open(stats_file, 'r') as f:
            player_stats = json.load(f)
        
        # Generate predictions
        result = predict_with_rl(player_id, player_stats)
        
        # Print result as JSON
        print(json.dumps(result))
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
