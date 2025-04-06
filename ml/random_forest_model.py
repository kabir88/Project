#!/usr/bin/env python3
"""
Random Forest model for NBA player performance prediction
"""

import os
import sys
import json
import argparse
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

# Define paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(SCRIPT_DIR, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

# Model file paths
RF_MODEL_PATH = os.path.join(MODEL_DIR, 'random_forest_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

def load_models():
    """Load the trained models and scalers"""
    try:
        with open(RF_MODEL_PATH, 'rb') as f:
            rf_models = pickle.load(f)
        
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        
        return rf_models, scaler
    except FileNotFoundError:
        print("Model files not found. Please train the models first.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        sys.exit(1)

def prepare_features(player_stats):
    """Extract and prepare features from player stats"""
    # Use recent game data as features
    recent_games = player_stats.get('gameByGame', [])
    
    if not recent_games:
        raise ValueError("No game data available for prediction")
    
    # Create a DataFrame from the recent games
    games_df = pd.DataFrame(recent_games)
    
    # Calculate basic stats from last N games (use max 10 games)
    n_games = min(10, len(games_df))
    recent_n_games = games_df.head(n_games)
    
    # Extract features
    features = {
        'avg_points': recent_n_games['points'].mean(),
        'avg_rebounds': recent_n_games['rebounds'].mean(),
        'avg_assists': recent_n_games['assists'].mean(),
        'avg_steals': recent_n_games['steals'].mean() if 'steals' in recent_n_games else 0,
        'avg_blocks': recent_n_games['blocks'].mean() if 'blocks' in recent_n_games else 0,
        'avg_fg_pct': recent_n_games['fieldGoalPercentage'].mean() if 'fieldGoalPercentage' in recent_n_games else 0,
        'avg_3p_pct': recent_n_games['threePointPercentage'].mean() if 'threePointPercentage' in recent_n_games else 0,
        'avg_ft_pct': recent_n_games['freeThrowPercentage'].mean() if 'freeThrowPercentage' in recent_n_games else 0,
        'avg_minutes': recent_n_games['minutes'].mean() if 'minutes' in recent_n_games else 0,
        'std_points': recent_n_games['points'].std(),
        'points_trend': get_trend(recent_n_games['points']),
        'rebounds_trend': get_trend(recent_n_games['rebounds']),
        'assists_trend': get_trend(recent_n_games['assists']),
    }
    
    # Add season averages
    features['season_ppg'] = player_stats.get('pointsPerGame', 0)
    features['season_rpg'] = player_stats.get('reboundsPerGame', 0)
    features['season_apg'] = player_stats.get('assistsPerGame', 0)
    features['season_fg_pct'] = player_stats.get('fieldGoalPercentage', 0)
    features['season_3p_pct'] = player_stats.get('threePointPercentage', 0)
    
    # Convert to numpy array and reshape for model input
    X = np.array(list(features.values())).reshape(1, -1)
    feature_names = list(features.keys())
    
    return X, feature_names, features

def get_trend(series):
    """Calculate the trend in a series using linear regression slope"""
    if len(series) < 2:
        return 0
        
    x = np.arange(len(series))
    y = series.values
    
    # Calculate slope
    if np.std(y) == 0:
        return 0  # No variation, no trend
    
    # Simple linear regression slope
    slope = np.polyfit(x, y, 1)[0]
    
    # Normalize by the mean to get relative trend
    mean_y = np.mean(y)
    if mean_y != 0:
        normalized_slope = slope / mean_y
    else:
        normalized_slope = 0
        
    return normalized_slope

def make_predictions(player_id, player_stats):
    """Generate predictions using the trained models"""
    try:
        # Load models
        rf_models, scaler = load_models()
        
        # Prepare features
        X, feature_names, feature_dict = prepare_features(player_stats)
        
        # Scale features
        X_scaled = scaler.transform(X)
        
        # Make predictions for different stats
        predictions = {}
        confidence = {}
        
        # Target stats to predict
        target_stats = ['points', 'rebounds', 'assists', 'fieldGoalPercentage']
        
        for stat in target_stats:
            if stat in rf_models:
                # Predict with Random Forest
                rf_pred = rf_models[stat].predict(X_scaled)[0]
                
                # Get prediction intervals (rough confidence estimate)
                rf_confidence = get_confidence_estimate(rf_models[stat], X_scaled, stat)
                
                predictions[stat] = float(rf_pred)
                confidence[stat] = float(rf_confidence)
            else:
                # Fallback to average if model not available
                predictions[stat] = float(feature_dict.get(f'avg_{stat}', 0))
                confidence[stat] = 0.5  # Medium confidence
        
        # Calculate season trends
        season_trend = {
            'points': float(feature_dict['points_trend']),
            'rebounds': float(feature_dict['rebounds_trend']),
            'assists': float(feature_dict['assists_trend']),
            'overall': float((feature_dict['points_trend'] + 
                            feature_dict['rebounds_trend'] + 
                            feature_dict['assists_trend']) / 3)
        }
        
        # Compile results
        result = {
            'playerId': player_id,
            'nextGame': {
                'points': predictions.get('points', 0),
                'rebounds': predictions.get('rebounds', 0),
                'assists': predictions.get('assists', 0),
                'fieldGoalPercentage': predictions.get('fieldGoalPercentage', 0)
            },
            'confidence': confidence,
            'seasonTrend': season_trend,
            'model': 'random_forest'
        }
        
        return result
    
    except Exception as e:
        print(f"Error making predictions: {str(e)}", file=sys.stderr)
        # Return a default prediction with error message
        return {
            'playerId': player_id,
            'error': str(e),
            'nextGame': {
                'points': player_stats.get('pointsPerGame', 0),
                'rebounds': player_stats.get('reboundsPerGame', 0),
                'assists': player_stats.get('assistsPerGame', 0),
                'fieldGoalPercentage': player_stats.get('fieldGoalPercentage', 0)
            },
            'confidence': {
                'points': 0.3,
                'rebounds': 0.3,
                'assists': 0.3,
                'fieldGoalPercentage': 0.3
            },
            'seasonTrend': {
                'points': 0,
                'rebounds': 0,
                'assists': 0,
                'overall': 0
            },
            'model': 'fallback_average'
        }

def get_confidence_estimate(model, X, stat):
    """Generate a confidence estimate for the prediction"""
    # For Random Forest, we could use the standard deviation of predictions across trees
    # This is a simplified version
    
    # Get predictions from all trees
    predictions = [tree.predict(X)[0] for tree in model.estimators_]
    std_dev = np.std(predictions)
    
    # Convert std dev to a confidence score between 0 and 1
    # Lower std dev = higher confidence
    if stat == 'fieldGoalPercentage':
        # For percentages, scale accordingly
        max_std = 0.1  # 10% variance in FG% is high
    else:
        # For counting stats, scale based on typical values
        typical_values = {'points': 10, 'rebounds': 5, 'assists': 3}
        max_std = typical_values.get(stat, 5)
    
    # Calculate confidence (1 = high confidence, 0 = low confidence)
    confidence = max(0, min(1, 1 - (std_dev / max_std)))
    
    return confidence

def main():
    """Main function to parse arguments and run the prediction"""
    parser = argparse.ArgumentParser(description='NBA Player Performance Prediction')
    parser.add_argument('--player_id', required=True, help='Player ID')
    parser.add_argument('--stats_file', required=True, help='JSON file with player stats')
    
    args = parser.parse_args()
    
    try:
        # Load player stats from file
        with open(args.stats_file, 'r') as f:
            player_stats = json.load(f)
        
        # Make predictions
        predictions = make_predictions(args.player_id, player_stats)
        
        # Print predictions as JSON to stdout
        print(json.dumps(predictions))
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
