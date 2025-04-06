const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

// Initialize the app
const app = express();

// Connect to PostgreSQL database (no-op if it fails)
try {
  require('./backend/config/db');
  console.log('Database connected successfully');
} catch (error) {
  console.warn('Database connection failed:', error.message);
}

// Initialize ML service (no-op if it fails)
try {
  require('./backend/services/mlService');
  console.log('ML service initialized successfully');
} catch (error) {
  console.warn('ML service initialization failed:', error.message);
}

// Configure CORS
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: false, limit: '10mb' }));

// Log requests for debugging
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
  next();
});

// Set up static folder for the public frontend
app.use(express.static(path.join(__dirname, 'public')));

// Define very simple routes without using path-to-regexp
app.get('/api/players/search', (req, res) => {
  try {
    const { query } = req.query;
    const playerController = require('./backend/controllers/playerController');
    playerController.searchPlayers(req, res);
  } catch (error) {
    console.error('Error in search route:', error);
    res.status(500).json({ error: 'Internal server error in search' });
  }
});

app.get('/api/players/:id', (req, res) => {
  try {
    const playerController = require('./backend/controllers/playerController');
    playerController.getPlayerById(req, res);
  } catch (error) {
    console.error('Error in player route:', error);
    res.status(500).json({ error: 'Internal server error in player fetch' });
  }
});

app.get('/api/players/:id/stats', (req, res) => {
  try {
    const playerController = require('./backend/controllers/playerController');
    playerController.getPlayerStats(req, res);
  } catch (error) {
    console.error('Error in stats route:', error);
    res.status(500).json({ error: 'Internal server error in stats fetch' });
  }
});

app.get('/api/players/:id/predictions', (req, res) => {
  try {
    const predictionController = require('./backend/controllers/predictionController');
    predictionController.getPredictions(req, res);
  } catch (error) {
    console.error('Error in predictions route:', error);
    res.status(500).json({ error: 'Internal server error in predictions' });
  }
});

// Default route for the frontend
app.get('*', (req, res) => {
  console.log(`Serving index.html for path: ${req.path}`);
  res.sendFile(path.join(__dirname, 'public/index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error occurred:', err.stack);
  
  res.status(err.status || 500).json({
    message: err.message || 'Something went wrong on the server',
    error: process.env.NODE_ENV === 'production' ? {} : err
  });
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Access the app at http://0.0.0.0:${PORT}`);
  console.log('Server is listening on all network interfaces');
});