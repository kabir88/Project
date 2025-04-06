const db = require('../config/db');

// Player model class
class Player {
  static async findById(playerId) {
    try {
      const result = await db.query(
        'SELECT * FROM players WHERE player_id = $1',
        [playerId]
      );
      return result.rows[0];
    } catch (error) {
      console.error('Error finding player by ID:', error);
      throw error;
    }
  }

  static async findByName(name) {
    try {
      const result = await db.query(
        "SELECT * FROM players WHERE name ILIKE $1",
        [`%${name}%`]
      );
      return result.rows;
    } catch (error) {
      console.error('Error finding player by name:', error);
      throw error;
    }
  }

  static async create(playerData) {
    try {
      const { player_id, name, team, position, height, weight, data } = playerData;
      
      const result = await db.query(
        `INSERT INTO players (player_id, name, team, position, height, weight, data) 
         VALUES ($1, $2, $3, $4, $5, $6, $7) 
         ON CONFLICT (player_id) 
         DO UPDATE SET 
           name = $2, 
           team = $3, 
           position = $4, 
           height = $5, 
           weight = $6, 
           data = $7,
           updated_at = CURRENT_TIMESTAMP
         RETURNING *`,
        [player_id, name, team, position, height, weight, JSON.stringify(data)]
      );
      
      return result.rows[0];
    } catch (error) {
      console.error('Error creating/updating player:', error);
      throw error;
    }
  }

  static async update(playerId, updateData) {
    try {
      // Build the SET part of the query dynamically based on what's being updated
      const setValues = [];
      const queryParams = [playerId];
      let paramCounter = 2;
      
      for (const [key, value] of Object.entries(updateData)) {
        // Skip player_id as we don't want to update that
        if (key === 'player_id') continue;
        
        // Handle JSONB data field differently
        if (key === 'data') {
          setValues.push(`${key} = $${paramCounter}`);
          queryParams.push(JSON.stringify(value));
        } else {
          setValues.push(`${key} = $${paramCounter}`);
          queryParams.push(value);
        }
        paramCounter++;
      }
      
      // Add updated_at timestamp
      setValues.push(`updated_at = CURRENT_TIMESTAMP`);
      
      if (setValues.length === 0) {
        throw new Error('No valid fields to update');
      }
      
      const query = `
        UPDATE players 
        SET ${setValues.join(', ')} 
        WHERE player_id = $1 
        RETURNING *
      `;
      
      const result = await db.query(query, queryParams);
      return result.rows[0];
    } catch (error) {
      console.error('Error updating player:', error);
      throw error;
    }
  }

  static async delete(playerId) {
    try {
      const result = await db.query(
        'DELETE FROM players WHERE player_id = $1 RETURNING *',
        [playerId]
      );
      return result.rows[0];
    } catch (error) {
      console.error('Error deleting player:', error);
      throw error;
    }
  }
}

module.exports = Player;
