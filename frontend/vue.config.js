module.exports = {
  publicPath: '/',
  devServer: {
    port: 5000,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
}
