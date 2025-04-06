const { Pool } = require('pg');
const config = require('./config');

// Create a PostgreSQL connection pool
let pool = null;

try {
  pool = new Pool(config.dbConfig);
  
  // Test the connection
  pool.connect()
    .then(client => {
      console.log('PostgreSQL database connected successfully');
      client.release();
      
      // Initialize the database tables if needed
      initDatabase();
    })
    .catch(err => {
      console.error('PostgreSQL connection error:', err);
      console.log('Application will continue without database functionality');
    });
} catch (error) {
  console.error('Error creating database pool:', error);
  console.log('Application will continue without database functionality');
}

// Function to initialize database tables
const initDatabase = async () => {
  if (!pool) return;
  
  const client = await pool.connect();
  try {
    // ... rest of the initDatabase function ...
  } catch (err) {
    console.error('Error initializing database:', err);
  } finally {
    client.release();
  }
};

// Export the pool to be used in other modules
module.exports = pool || {
  query: () => Promise.resolve({ rows: [] }),
  connect: () => Promise.resolve({ release: () => {} })
};