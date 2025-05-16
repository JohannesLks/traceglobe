export default defineNuxtConfig({
  ssr: false, // wichtig für Vercel mit clientseitigem Routing (SPA)
  runtimeConfig: {
    public: {
      backendUrl: process.env.BACKEND_URL || 'https://traceglobebackend.onrender.com'
    }
  },
  modules: ['@vueuse/nuxt'],
  devtools: false
})
