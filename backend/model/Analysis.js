const db = require('../config/db');

// Analysis model class
class Analysis {
  static async findById(id) {
    try {
      const result = await db.query(
        'SELECT * FROM analyses WHERE id = $1',
        [id]
      );
      return result.rows[0];
    } catch (error) {
      console.error('Error finding analysis by ID:', error);
      throw error;
    }
  }

  static async findByPlayerId(playerId) {
    try {
      const result = await db.query(
        'SELECT * FROM analyses WHERE player_id = $1 ORDER BY created_at DESC',
        [playerId]
      );
      return result.rows;
    } catch (error) {
      console.error('Error finding analyses by player ID:', error);
      throw error;
    }
  }

  static async findAll() {
    try {
      const result = await db.query(
        'SELECT a.*, p.name as player_name FROM analyses a JOIN players p ON a.player_id = p.player_id ORDER BY a.created_at DESC'
      );
      return result.rows;
    } catch (error) {
      console.error('Error finding all analyses:', error);
      throw error;
    }
  }

  static async create(analysisData) {
    try {
      const { player_id, title, description, stats, predictions } = analysisData;
      
      const result = await db.query(
        `INSERT INTO analyses (player_id, title, description, stats, predictions) 
         VALUES ($1, $2, $3, $4, $5) 
         RETURNING *`,
        [
          player_id, 
          title, 
          description, 
          JSON.stringify(stats || {}), 
          JSON.stringify(predictions || {})
        ]
      );
      
      return result.rows[0];
    } catch (error) {
      console.error('Error creating analysis:', error);
      throw error;
    }
  }

  static async update(id, updateData) {
    try {
      // Build the SET part of the query dynamically based on what's being updated
      const setValues = [];
      const queryParams = [id];
      let paramCounter = 2;
      
      for (const [key, value] of Object.entries(updateData)) {
        // Handle JSONB fields differently
        if (['stats', 'predictions'].includes(key)) {
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
        UPDATE analyses 
        SET ${setValues.join(', ')} 
        WHERE id = $1 
        RETURNING *
      `;
      
      const result = await db.query(query, queryParams);
      return result.rows[0];
    } catch (error) {
      console.error('Error updating analysis:', error);
      throw error;
    }
  }

  static async delete(id) {
    try {
      const result = await db.query(
        'DELETE FROM analyses WHERE id = $1 RETURNING *',
        [id]
      );
      return result.rows[0];
    } catch (error) {
      console.error('Error deleting analysis:', error);
      throw error;
    }
  }
}

module.exports = Analysis;
