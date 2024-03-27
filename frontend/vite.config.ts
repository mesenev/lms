import { fileURLToPath, URL } from 'node:url'
import dns from 'dns'
import { defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

dns.setDefaultResultOrder('verbatim')

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
      sourcemap: true,
      rollupOptions: {
      output: {
        entryFileNames: `assets/[name].js`,
        chunkFileNames: `assets/[name].js`,
        assetFileNames: `assets/[name].[ext]`
      }
    }
  },
  server: {
      proxy: {
          '/api': {
              target: 'http://localhost:8000/',
              changeOrigin: true,
          }
      }
  }
})
