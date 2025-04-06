#!/usr/bin/env python3
"""
Train machine learning models for NBA player performance prediction
"""

import os
import sys
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from data_processor import load_and_preprocess_data, split_features_targets, scale_features
from reinforcement_learning_model import SimplifiedRLModel

# Define paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
MODEL_DIR = os.path.join(SCRIPT_DIR, 'models')

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# Model file paths
RF_MODEL_PATH = os.path.join(MODEL_DIR, 'random_forest_model.pkl')
RL_MODEL_PATH = os.path.join(MODEL_DIR, 'reinforcement_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

def generate_sample_data():
    """
    Generate sample data for model training when real data is not available
    This is used for demonstration purposes only
    """
    print("Generating sample data for model training...")
    
    # Create a list to hold player data
    players_data = []
    
    # Generate 10 players
    for player_id in range(1, 11):
        player_name = f"Player {player_id}"
        
        # Generate base stats for the player
        base_points = np.random.uniform(5, 30)
        base_rebounds = np.random.uniform(1, 15)
        base_assists = np.random.uniform(1, 10)
        base_fg_pct = np.random.uniform(0.35, 0.55)
        
        # Generate game-by-game stats
        game_by_game = []
        
        for game_id in range(1, 21):  # 20 games per player
            # Add random variation to base stats
            points = max(0, np.random.normal(base_points, base_points * 0.2))
            rebounds = max(0, np.random.normal(base_rebounds, base_rebounds * 0.3))
            assists = max(0, np.random.normal(base_assists, base_assists * 0.3))
            fg_pct = max(0, min(1, np.random.normal(base_fg_pct, 0.1)))
            
            # Create game stats
            game = {
                'gameId': f"{player_id}_{game_id}",
                'date': f"2023-{game_id//3 + 1:02d}-{game_id%30 + 1:02d}",
                'points': points,
                'rebounds': rebounds,
                'assists': assists,
                'steals': np.random.uniform(0, 3),
                'blocks': np.random.uniform(0, 2),
                'fieldGoalPercentage': fg_pct,
                'threePointPercentage': np.random.uniform(0.2, 0.5),
                'freeThrowPercentage': np.random.uniform(0.6, 0.95),
                'minutes': np.random.uniform(15, 40),
                'turnovers': np.random.uniform(0, 5),
                'personalFouls': np.random.uniform(0, 5),
                'plusMinus': np.random.normal(0, 10)
            }
            
            game_by_game.append(game)
        
        # Create player object
        player = {
            'id': str(player_id),
            'firstName': f"First{player_id}",
            'lastName': f"Last{player_id}",
            'teamId': str(np.random.randint(1, 31)),
            'teamName': f"Team {np.random.randint(1, 31)}",
            'position': np.random.choice(['PG', 'SG', 'SF', 'PF', 'C']),
            'gameByGame': game_by_game,
            'pointsPerGame': np.mean([g['points'] for g in game_by_game]),
            'reboundsPerGame': np.mean([g['rebounds'] for g in game_by_game]),
            'assistsPerGame': np.mean([g['assists'] for g in game_by_game]),
            'stealsPerGame': np.mean([g['steals'] for g in game_by_game]),
            'blocksPerGame': np.mean([g['blocks'] for g in game_by_game]),
            'fieldGoalPercentage': np.mean([g['fieldGoalPercentage'] for g in game_by_game]),
            'threePointPercentage': np.mean([g['threePointPercentage'] for g in game_by_game]),
            'freeThrowPercentage': np.mean([g['freeThrowPercentage'] for g in game_by_game])
        }
        
        players_data.append(player)
    
    # Save sample data to file
    sample_data_path = os.path.join(DATA_DIR, 'sample_data.json')
    with open(sample_data_path, 'w') as f:
        json.dump(players_data, f)
    
    return sample_data_path

def train_random_forest_models(X, y_dict, scaler):
    """
    Train Random Forest models for different target variables
    
    Args:
        X (numpy.ndarray): Scaled feature matrix
        y_dict (dict): Dictionary of target variables
        scaler (StandardScaler): Fitted scaler for feature scaling
        
    Returns:
        dict: Dictionary of trained models
    """
    print("Training Random Forest models...")
    
    # Dictionary to store models
    rf_models = {}
    
    # Train a model for each target variable
    for target_name, y in y_dict.items():
        print(f"Training model for {target_name}...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Create and train model
        rf = RandomForestRegressor(n_estimators=100, min_samples_split=5, min_samples_leaf=2, random_state=42)
        rf.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = rf.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"  MSE: {mse:.2f}, R²: {r2:.2f}")
        
        # Store model
        rf_models[target_name] = rf
    
    # Save models
    with open(RF_MODEL_PATH, 'wb') as f:
        pickle.dump(rf_models, f)
    
    # Save scaler
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    
    print(f"Random Forest models saved to {RF_MODEL_PATH}")
    
    return rf_models

def train_reinforcement_model(data):
    """
    Train a simplified reinforcement learning model
    
    This is a placeholder for a real RL implementation
    In a real application, you would use more sophisticated RL algorithms
    
    Args:
        data (pandas.DataFrame): Preprocessed data
        
    Returns:
        SimplifiedRLModel: Trained RL model
    """
    print("Training Reinforcement Learning model...")
    
    # Create a simple RL model
    # In a real application, you would properly define states and actions
    state_size = 10  # Simplified state space
    action_size = 5  # Simplified action space (performance levels)
    
    rl_model = SimplifiedRLModel(state_size, action_size)
    
    # In a real RL training loop, you would:
    # 1. Sample states from the environment
    # 2. Choose actions using policy
    # 3. Observe rewards and next states
    # 4. Update Q-values
    # 5. Repeat until convergence
    
    # Save model
    rl_model.save(RL_MODEL_PATH)
    
    print(f"Reinforcement Learning model saved to {RL_MODEL_PATH}")
    
    return rl_model

def main():
    """Main function to train models"""
    try:
        # Check if sample data exists, otherwise generate it
        sample_data_path = os.path.join(DATA_DIR, 'sample_data.json')
        if not os.path.exists(sample_data_path):
            sample_data_path = generate_sample_data()
        
        # Load and preprocess data
        print(f"Loading data from {sample_data_path}...")
        df = load_and_preprocess_data(sample_data_path)
        print(f"Loaded {len(df)} records")
        
        # Split into features and targets
        X, y_dict = split_features_targets(df)
        print(f"Features: {X.shape[1]}, Targets: {len(y_dict)}")
        
        # Scale features
        X_scaled, scaler = scale_features(X)
        
        # Train Random Forest models
        rf_models = train_random_forest_models(X_scaled, y_dict, scaler)
        
        # Train Reinforcement Learning model
        rl_model = train_reinforcement_model(df)
        
        print("Training complete!")
        
    except Exception as e:
        print(f"Error training models: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
