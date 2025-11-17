import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy API calls to backend (adjust if your backend port is different)
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
});
