import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
// vite.config.js configura Vite y el plugin de React
// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
})
