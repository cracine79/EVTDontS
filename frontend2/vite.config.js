import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy API requests to Flask backend
      '/api': {
        target: process.env.ENV === 'production' ? 'https://evtds-b5fec09435ac.herokuapp.com/' : 'http://127.0.0.1:3000', // Flask server address
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // Adjust path if needed
      },
    },
  },

    build: {
    outDir: '../backend/static/build', // Build output directory for Flask
    emptyOutDir: true, // Clears the output directory before building
  },
})
