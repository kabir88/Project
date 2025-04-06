const Analysis = require('../models/Analysis');
const Player = require('../models/Player');

// Get all saved analyses
exports.getAllAnalyses = async (req, res) => {
  try {
    const analyses = await Analysis.findAll();
    res.json(analyses);
  } catch (error) {
    console.error('Error fetching analyses:', error);
    res.status(500).json({ message: 'Error fetching saved analyses', error: error.message });
  }
};

// Get analysis by ID
exports.getAnalysisById = async (req, res) => {
  try {
    const analysis = await Analysis.findById(req.params.id);
    
    if (!analysis) {
      return res.status(404).json({ message: 'Analysis not found' });
    }
    
    res.json(analysis);
  } catch (error) {
    console.error('Error fetching analysis:', error);
    res.status(500).json({ message: 'Error fetching analysis', error: error.message });
  }
};

// Create a new analysis
exports.createAnalysis = async (req, res) => {
  try {
    const { player_id, title, description, stats, predictions } = req.body;
    
    if (!player_id || !title) {
      return res.status(400).json({ message: 'Player ID and title are required' });
    }
    
    // Verify player exists
    const player = await Player.findById(player_id);
    if (!player) {
      return res.status(404).json({ message: 'Player not found' });
    }
    
    const newAnalysis = await Analysis.create({
      player_id,
      title,
      description,
      stats,
      predictions
    });
    
    res.status(201).json(newAnalysis);
  } catch (error) {
    console.error('Error creating analysis:', error);
    res.status(500).json({ message: 'Error saving analysis', error: error.message });
  }
};

// Update an existing analysis
exports.updateAnalysis = async (req, res) => {
  try {
    const { player_id, title, description, stats, predictions } = req.body;
    
    if (player_id) {
      // Verify player exists if player_id is being updated
      const player = await Player.findById(player_id);
      if (!player) {
        return res.status(404).json({ message: 'Player not found' });
      }
    }
    
    const updatedAnalysis = await Analysis.update(
      req.params.id,
      {
        player_id,
        title,
        description,
        stats,
        predictions
      }
    );
    
    if (!updatedAnalysis) {
      return res.status(404).json({ message: 'Analysis not found' });
    }
    
    res.json(updatedAnalysis);
  } catch (error) {
    console.error('Error updating analysis:', error);
    res.status(500).json({ message: 'Error updating analysis', error: error.message });
  }
};

// Delete an analysis
exports.deleteAnalysis = async (req, res) => {
  try {
    const analysis = await Analysis.delete(req.params.id);
    
    if (!analysis) {
      return res.status(404).json({ message: 'Analysis not found' });
    }
    
    res.json({ message: 'Analysis deleted successfully' });
  } catch (error) {
    console.error('Error deleting analysis:', error);
    res.status(500).json({ message: 'Error deleting analysis', error: error.message });
  }
};
