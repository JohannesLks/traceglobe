export default defineNuxtConfig({
  ssr: false,
  runtimeConfig: {
    public: {
      backendUrl: process.env.BACKEND_URL || 'https://traceglobebackend.onrender.com'
    }
  },
  modules: ['@vueuse/nuxt'],
  devtools: false,
  css: ['@/assets/css/main.css'],
  app: {
    head: {
      title: 'TraceGlobe',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ],
      link: [
        {
          rel: 'stylesheet',
          href: 'https://rsms.me/inter/inter.css'
        },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap'
        }
      ]
    }
  },
  vite: {
    server: {
      hmr: { overlay: false },
      watch: { usePolling: true }
    }
  }
})