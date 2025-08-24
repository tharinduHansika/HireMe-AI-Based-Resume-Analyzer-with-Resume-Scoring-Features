import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    // If your backend is on 5000 and you want to call /api/* without env:
    // proxy: { '/api': { target: 'http://localhost:5000', changeOrigin: true } }
  },
});

