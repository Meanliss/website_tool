import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  base: '/',
  server: {
    port: 5173,
    // Proxy chỉ cho development, production dùng VITE_API_URL
    proxy: mode === 'development' ? {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    } : undefined
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  }
}))
