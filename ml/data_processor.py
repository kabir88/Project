#!/usr/bin/env python3
"""
Data processing utilities for NBA player statistics
"""

import os
import sys
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_data(data_file):
    """
    Load player data from JSON file and preprocess it for model training
    
    Args:
        data_file (str): Path to the JSON file containing player data
        
    Returns:
        pandas.DataFrame: Preprocessed data ready for model training
    """
    try:
        # Load data
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Check if data is a list of players or a single player object
        if isinstance(data, dict):
            players_data = [data]
        else:
            players_data = data
        
        all_player_records = []
        
        # Process each player
        for player in players_data:
            player_records = process_player_data(player)
            all_player_records.extend(player_records)
        
        # Convert to DataFrame
        if not all_player_records:
            raise ValueError("No valid player records found in the data")
        
        df = pd.DataFrame(all_player_records)
        
        # Handle missing values
        df = handle_missing_values(df)
        
        # Create feature columns
        df = create_features(df)
        
        return df
    
    except Exception as e:
        print(f"Error processing data: {str(e)}", file=sys.stderr)
        raise

def process_player_data(player):
    """
    Process data for a single player
    
    Args:
        player (dict): Player data including game-by-game stats
        
    Returns:
        list: List of records, each representing features for a game
    """
    player_records = []
    
    # Get basic player info
    player_id = player.get('id')
    player_name = f"{player.get('firstName', '')} {player.get('lastName', '')}"
    
    # Get game-by-game stats
    games = player.get('gameByGame', [])
    
    if not games:
        return []
    
    # Sort games by date if available
    if 'date' in games[0]:
        games = sorted(games, key=lambda g: g.get('date', ''))
    
    # Process each game
    for i, game in enumerate(games):
        if i == 0:
            # Skip first game as we can't calculate pre-game averages
            continue
        
        # Get stats from current game
        record = {
            'player_id': player_id,
            'player_name': player_name,
            'game_id': game.get('gameId'),
            'date': game.get('date'),
            
            # Target variables (what we want to predict)
            'points': game.get('points', 0),
            'rebounds': game.get('rebounds', 0),
            'assists': game.get('assists', 0),
            'steals': game.get('steals', 0),
            'blocks': game.get('blocks', 0),
            'field_goal_percentage': game.get('fieldGoalPercentage', 0),
            'three_point_percentage': game.get('threePointPercentage', 0),
            'free_throw_percentage': game.get('freeThrowPercentage', 0),
            
            # Other game stats
            'minutes': game.get('minutes', 0),
            'turnovers': game.get('turnovers', 0),
            'personal_fouls': game.get('personalFouls', 0),
            'plus_minus': game.get('plusMinus', 0)
        }
        
        # Calculate pre-game averages from previous games
        prev_games = games[:i]
        
        pre_game_stats = {
            'avg_points': np.mean([g.get('points', 0) for g in prev_games]),
            'avg_rebounds': np.mean([g.get('rebounds', 0) for g in prev_games]),
            'avg_assists': np.mean([g.get('assists', 0) for g in prev_games]),
            'avg_steals': np.mean([g.get('steals', 0) for g in prev_games]),
            'avg_blocks': np.mean([g.get('blocks', 0) for g in prev_games]),
            'avg_minutes': np.mean([g.get('minutes', 0) for g in prev_games]),
            'avg_turnovers': np.mean([g.get('turnovers', 0) for g in prev_games]),
            'avg_fg_pct': np.mean([g.get('fieldGoalPercentage', 0) for g in prev_games]),
            'avg_3p_pct': np.mean([g.get('threePointPercentage', 0) for g in prev_games]),
            'avg_ft_pct': np.mean([g.get('freeThrowPercentage', 0) for g in prev_games]),
            
            # Add standard deviations for variability
            'std_points': np.std([g.get('points', 0) for g in prev_games]),
            'std_rebounds': np.std([g.get('rebounds', 0) for g in prev_games]),
            'std_assists': np.std([g.get('assists', 0) for g in prev_games]),
            
            # Add recent form (last 3 games average)
            'recent_points': np.mean([g.get('points', 0) for g in prev_games[-3:]]),
            'recent_rebounds': np.mean([g.get('rebounds', 0) for g in prev_games[-3:]]),
            'recent_assists': np.mean([g.get('assists', 0) for g in prev_games[-3:]])
        }
        
        # Add pre-game stats to record
        record.update(pre_game_stats)
        
        player_records.append(record)
    
    return player_records

def handle_missing_values(df):
    """Handle missing values in the DataFrame"""
    # Replace NaN with 0 for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    # Replace NaN with empty string for object columns
    object_cols = df.select_dtypes(include=['object']).columns
    df[object_cols] = df[object_cols].fillna('')
    
    return df

def create_features(df):
    """Create additional features for the model"""
    # Ratio features
    df['points_per_minute'] = df.apply(lambda x: x['points'] / x['minutes'] if x['minutes'] > 0 else 0, axis=1)
    df['rebounds_per_minute'] = df.apply(lambda x: x['rebounds'] / x['minutes'] if x['minutes'] > 0 else 0, axis=1)
    df['assists_per_minute'] = df.apply(lambda x: x['assists'] / x['minutes'] if x['minutes'] > 0 else 0, axis=1)
    
    # Consistency features
    df['points_consistency'] = df.apply(lambda x: 1 - (x['std_points'] / x['avg_points']) if x['avg_points'] > 0 else 0, axis=1)
    df['rebounds_consistency'] = df.apply(lambda x: 1 - (x['std_rebounds'] / x['avg_rebounds']) if x['avg_rebounds'] > 0 else 0, axis=1)
    df['assists_consistency'] = df.apply(lambda x: 1 - (x['std_assists'] / x['avg_assists']) if x['avg_assists'] > 0 else 0, axis=1)
    
    # Form features (recent vs average)
    df['points_form'] = df.apply(lambda x: x['recent_points'] / x['avg_points'] if x['avg_points'] > 0 else 1, axis=1)
    df['rebounds_form'] = df.apply(lambda x: x['recent_rebounds'] / x['avg_rebounds'] if x['avg_rebounds'] > 0 else 1, axis=1)
    df['assists_form'] = df.apply(lambda x: x['recent_assists'] / x['avg_assists'] if x['avg_assists'] > 0 else 1, axis=1)
    
    return df

def split_features_targets(df):
    """
    Split DataFrame into features and target variables
    
    Args:
        df (pandas.DataFrame): Preprocessed DataFrame
        
    Returns:
        tuple: (X, y_dict) where X is the feature DataFrame and y_dict is a dictionary
               of target variables
    """
    # Target columns
    target_cols = ['points', 'rebounds', 'assists', 'field_goal_percentage']
    
    # Feature columns (exclude targets and non-feature columns)
    non_feature_cols = target_cols + ['player_id', 'player_name', 'game_id', 'date']
    feature_cols = [col for col in df.columns if col not in non_feature_cols]
    
    # Create X (features)
    X = df[feature_cols]
    
    # Create y_dict (targets)
    y_dict = {target: df[target] for target in target_cols}
    
    return X, y_dict

def scale_features(X, scaler=None, fit=True):
    """
    Scale features using StandardScaler
    
    Args:
        X (pandas.DataFrame): Feature DataFrame
        scaler (StandardScaler, optional): Existing scaler for transform only
        fit (bool): Whether to fit the scaler on X
        
    Returns:
        tuple: (X_scaled, scaler)
    """
    if scaler is None:
        scaler = StandardScaler()
    
    if fit:
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)
    
    return X_scaled, scaler

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) < 2:
        print("Usage: python data_processor.py <data_file>")
        sys.exit(1)
    
    data_file = sys.argv[1]
    
    try:
        df = load_and_preprocess_data(data_file)
        X, y_dict = split_features_targets(df)
        X_scaled, scaler = scale_features(X)
        
        print(f"Processed {len(df)} records with {X.shape[1]} features")
        print(f"Target variables: {list(y_dict.keys())}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
