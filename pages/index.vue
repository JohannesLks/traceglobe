<template>
  <div class="min-h-screen bg-black text-white font-jetbrains">
    <!-- Hero Section -->
    <div class="relative h-screen flex flex-col items-center justify-center px-6 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-b from-red-500/10 to-transparent pointer-events-none"></div>
      
      <h1 class="text-4xl md:text-6xl font-bold text-center mb-6 tracking-tight">
        <span class="bg-gradient-to-r from-white to-red-500 bg-clip-text text-transparent">
          TraceGlobe
        </span>
      </h1>
      
      <p class="text-lg md:text-xl text-gray-400 text-center max-w-2xl mb-8 leading-relaxed">
        Discover where your data travels. Automated provider analysis from your inbox.
      </p>

      <button @click="loginWithGoogle"
              class="group relative px-8 py-3 bg-red-500 rounded-lg overflow-hidden transition-all duration-300 hover:scale-105"
              :class="{ 'animate-pulse': loading }">
        <span class="absolute inset-0 bg-gradient-to-r from-red-600 to-red-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
        <span class="relative flex items-center gap-2 text-black font-medium">
          <span class="text-xl">🔐</span>
          Login with Google
        </span>
      </button>
    </div>

    <!-- Features Section -->
    <div class="container mx-auto px-6 py-16 space-y-16">
      <div class="grid md:grid-cols-3 gap-8">
        <div v-for="(feature, index) in features" :key="index"
             class="p-6 rounded-xl backdrop-blur-lg bg-white/5 border border-red-500/10 transform hover:scale-105 transition-all duration-300"
             :class="{ 'hover:border-red-500/30': !loading }">
          <div class="text-2xl mb-4">{{ feature.icon }}</div>
          <h3 class="text-xl font-semibold mb-2 text-red-500">{{ feature.title }}</h3>
          <p class="text-gray-400">{{ feature.description }}</p>
        </div>
      </div>

      <!-- Globe Section -->
      <div class="relative">
        <div v-if="loading" 
             class="absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-10 rounded-xl">
          <div class="text-red-500 text-xl animate-pulse">Loading provider data...</div>
        </div>
        
        <div v-if="errorMessage" 
             class="absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-10 rounded-xl">
          <div class="text-red-500 text-xl">{{ errorMessage }}</div>
        </div>

        <client-only>
          <GlobeMap v-if="geoData.length" :points="geoData" />
        </client-only>
      </div>

      <!-- Providers Section -->
      <div v-if="providers.length" 
           class="bg-white/5 p-8 rounded-xl backdrop-blur-lg border border-red-500/10 transform hover:border-red-500/20 transition-all duration-300">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-2xl font-bold bg-gradient-to-r from-white to-red-500 bg-clip-text text-transparent">
            Provider Analysis
          </h2>
          <button @click="downloadJSON"
                  class="px-6 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-500 rounded-lg transition-all duration-300 flex items-center gap-2">
            <span>Export Data</span>
            <span class="text-lg">📥</span>
          </button>
        </div>
        
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="p in providers" :key="p.label"
               class="p-4 rounded-lg bg-white/5 hover:bg-white/10 border border-red-500/10 hover:border-red-500/20 transition-all duration-300">
            <div class="font-semibold text-lg mb-1">{{ p.label }}</div>
            <div class="text-sm text-red-400">{{ p.country }} – {{ p.asn }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="border-t border-red-500/10 mt-16">
      <div class="container mx-auto px-6 py-8">
        <div class="text-center text-gray-500 text-sm">
          © 2025 TraceGlobe. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { gsap } from 'gsap'
import GlobeMap from '~/components/GlobeMap.vue'

const config = useRuntimeConfig()
const providers = ref([])
const geoData = ref([])
const loading = ref(false)
const errorMessage = ref("")

const features = [
  {
    icon: "🔒",
    title: "Email Analysis",
    description: "Secure login and automated inbox scanning for provider detection"
  },
  {
    icon: "🌐",
    title: "Global Tracking",
    description: "Real-time visualization of server locations worldwide"
  },
  {
    icon: "🛡️",
    title: "Privacy Insights",
    description: "Detailed analysis of your email providers' data practices"
  }
]

onMounted(() => {
  window.addEventListener("message", handleAuthMessage)
  animateContent()
})

onUnmounted(() => {
  window.removeEventListener("message", handleAuthMessage)
})

function animateContent() {
  gsap.from('h1', {
    y: 30,
    opacity: 0,
    duration: 1,
    ease: 'expo.out'
  })
  
  gsap.from('p', {
    y: 20,
    opacity: 0,
    duration: 1,
    delay: 0.2,
    ease: 'expo.out'
  })
  
  gsap.from('button', {
    y: 20,
    opacity: 0,
    duration: 1,
    delay: 0.4,
    ease: 'expo.out'
  })

  gsap.from('.grid > div', {
    y: 30,
    opacity: 0,
    duration: 1,
    stagger: 0.1,
    delay: 0.6,
    ease: 'expo.out'
  })
}

function loginWithGoogle() {
  const popup = window.open(
    `${config.public.backendUrl}/auth/login`,
    "_blank",
    "width=500,height=600,left=100,top=100"
  )
  const checkClosed = setInterval(() => {
    if (popup?.closed) {
      clearInterval(checkClosed)
      fetchData()
    }
  }, 500)
}

function handleAuthMessage(event) {
  if (event.data === "google-auth-success") fetchData()
}

async function fetchData() {
  loading.value = true
  try {
    const res = await fetch(`${config.public.backendUrl}/gmail/providers`, {
      credentials: "include"
    })
    const data = await res.json()
    geoData.value = (data.geodata || []).map(e => ({
      ...e,
      lat: Number(e.lat),
      lng: Number(e.lng)
    }))
    providers.value = data.geodata || []
    if (!geoData.value.length) errorMessage.value = "No providers found."
  } catch (err) {
    errorMessage.value = "Error loading data."
  } finally {
    loading.value = false
  }
}

function downloadJSON() {
  window.open(`${config.public.backendUrl}/results/download`, "_blank")
}
</script>