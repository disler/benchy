import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import UnoCSS from 'unocss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), UnoCSS()],
  server: {
    proxy: {
      '/prompt': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/tool-prompt': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/iso-speed-bench': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/thought-prompt': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    }
  }
})
