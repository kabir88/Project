const express = require('express');
const router = express.Router();

// Import controllers
const playerController = require('../controllers/playerController');
const analysisController = require('../controllers/analysisController');
const predictionController = require('../controllers/predictionController');

// Player routes
// Support both /api/players/search?query= and /api/players/search?q= for compatibility
router.get('/players/search', (req, res, next) => {
  // If q parameter is present but query is not, copy q to query
  if (req.query.q && !req.query.query) {
    req.query.query = req.query.q;
  }
  next();
}, playerController.searchPlayers);
router.get('/players/:id', playerController.getPlayerById);
router.get('/players/:id/stats', playerController.getPlayerStats);

// Analysis routes
router.get('/analyses', analysisController.getAllAnalyses);
router.get('/analyses/:id', analysisController.getAnalysisById);
router.post('/analyses', analysisController.createAnalysis);
router.put('/analyses/:id', analysisController.updateAnalysis);
router.delete('/analyses/:id', analysisController.deleteAnalysis);

// Prediction routes
router.get('/players/:id/predictions', predictionController.getPredictions);

// Player Comparison route
router.get('/players/compare/:id1/:id2', playerController.comparePlayersById);

// Top players route
router.get('/players/top/:count', playerController.getTopPlayers);

// MVP prediction route
router.get('/predictions/mvp', predictionController.getMVPPredictions);

// Model effectiveness route
router.get('/models/effectiveness', predictionController.getModelEffectiveness);

module.exports = router;
