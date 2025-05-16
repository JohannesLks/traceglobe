export default defineNuxtConfig({
  ssr: false, // Wichtig für Vercel: SPA mit Client-Side Routing
  runtimeConfig: {
    public: {
      backendUrl: process.env.BACKEND_URL || 'https://traceglobebackend.onrender.com'
    }
  },
  modules: ['@vueuse/nuxt'],
  devtools: false
})
