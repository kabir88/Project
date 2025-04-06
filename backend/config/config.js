// Get environment variables with default values
const config = {
  env: process.env.NODE_ENV || 'development',
  port: process.env.PORT || 8000,
  dbConfig: {
    connectionString: process.env.DATABASE_URL || 'postgresql://nba_app:pass1234@localhost:5432/nba_dashboard',
    host: process.env.PGHOST || 'localhost',
    port: process.env.PGPORT || 5432,
    user: process.env.PGUSER || 'nba_app',
    password: process.env.PGPASSWORD || 'pass1234',
    database: process.env.PGDATABASE || 'nba_dashboard'
  },
  jwtSecret: process.env.JWT_SECRET || 'nba-dashboard-secret-key',
  nbaApiKey: process.env.NBA_API_KEY || '',
  apiTimeout: 30000, // 30 seconds
  modelDirectory: process.env.MODEL_DIRECTORY || 'ml/models'
};

module.exports = config;
