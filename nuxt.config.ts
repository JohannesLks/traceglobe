export default defineNuxtConfig({
  ssr: false, // important for Vercel with client-side routing (SPA)
  runtimeConfig: {
    public: {
      backendUrl: process.env.BACKEND_URL || 'https://traceglobebackend.onrender.com'
    }
  },
  modules: ['@vueuse/nuxt'],
  devtools: false
})