import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        // 如果后端接口没有 /api 前缀，可以重写路径
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
}) 