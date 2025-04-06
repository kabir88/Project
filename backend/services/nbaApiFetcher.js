/**
 * NBA API Fetcher - A bridge to the Python NBA API client
 * This module executes the Python nba_data_fetcher.py script to get authentic NBA data
 */

const { spawn } = require('child_process');
const path = require('path');

/**
 * Fetch player statistics directly from the NBA API using the Python script
 * @param {string} playerId - NBA player ID
 * @returns {Promise<Object>} - Player statistics
 */
exports.fetchPlayerStats = async (playerId) => {
  return new Promise((resolve, reject) => {
    console.log(`Fetching stats for player ${playerId} from NBA API...`);
    
    // Create a Python process to execute the script
    const pythonScript = path.join(process.cwd(), 'nba_data_fetcher.py');
    const pythonProcess = spawn('python', [
      '-c', 
      `
import sys
sys.path.append('${process.cwd()}')
from nba_data_fetcher import fetch_player_stats
import json

# Fetch stats for the specified player ID and print as JSON
player_stats = fetch_player_stats('${playerId}')
print(json.dumps(player_stats))
      `
    ]);
    
    let dataString = '';
    let errorString = '';
    
    // Collect data from stdout
    pythonProcess.stdout.on('data', (data) => {
      dataString += data.toString();
    });
    
    // Collect any errors
    pythonProcess.stderr.on('data', (data) => {
      errorString += data.toString();
    });
    
    // Handle process completion
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python process exited with code ${code}`);
        console.error(`Error: ${errorString}`);
        reject(new Error(`Failed to fetch player stats: ${errorString}`));
        return;
      }
      
      try {
        // Parse JSON from Python script output
        const stats = JSON.parse(dataString);
        console.log(`Successfully fetched NBA API stats for player ${playerId}`);
        resolve(stats);
      } catch (error) {
        console.error('Error parsing stats from Python script:', error);
        console.error('Raw output:', dataString);
        reject(error);
      }
    });
  });
};