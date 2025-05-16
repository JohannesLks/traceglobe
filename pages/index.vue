<template>
  <div class="min-h-screen bg-black text-white">
    <!-- Hero Section -->
    <section class="relative min-h-screen flex items-center justify-center px-4 overflow-hidden">
      <!-- Background Effects -->
      <div class="absolute inset-0">
        <div class="absolute inset-0 bg-gradient-to-b from-red-500/10 via-black to-black"></div>
        <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-red-500/20 rounded-full blur-[120px] opacity-20"></div>
      </div>

      <div class="relative z-10 max-w-4xl mx-auto text-center">
        <h1 class="text-5xl md:text-7xl font-bold mb-8 text-gradient tracking-tight">
          TraceGlobe
        </h1>
        
        <p class="text-xl md:text-2xl text-gray-400 mb-12 leading-relaxed max-w-2xl mx-auto">
          Discover the journey of your data through a revolutionary visual experience
        </p>

        <button @click="loginWithGoogle"
                class="group relative inline-flex items-center justify-center gap-3 px-8 py-4 bg-gradient-to-r from-red-500 to-red-600 rounded-full overflow-hidden transition-all duration-500 hover:scale-105 hover:shadow-[0_0_30px_rgba(255,45,85,0.3)]"
                :class="{ 'animate-pulse': loading }">
          <span class="absolute inset-0 w-full h-full bg-gradient-to-r from-red-600 to-red-400 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></span>
          <span class="relative text-white font-medium text-lg">Connect with Google</span>
          <svg class="w-5 h-5 relative" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </button>
      </div>
    </section>

    <!-- Features Grid -->
    <section class="relative py-24 px-4">
      <div class="max-w-7xl mx-auto grid md:grid-cols-3 gap-8">
        <div v-for="(feature, index) in features" 
             :key="index"
             class="glass-panel p-8 rounded-2xl hover-glow">
          <div class="text-3xl mb-6">{{ feature.icon }}</div>
          <h3 class="text-xl font-semibold mb-4 text-gradient">{{ feature.title }}</h3>
          <p class="text-gray-400 leading-relaxed">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- Globe Visualization -->
    <section class="relative py-24 px-4">
      <div class="max-w-7xl mx-auto">
        <div class="relative">
          <div v-if="loading" 
               class="absolute inset-0 flex items-center justify-center bg-black/80 backdrop-blur-sm z-10 rounded-2xl">
            <div class="flex items-center gap-3">
              <div class="w-3 h-3 bg-red-500 rounded-full animate-bounce"></div>
              <div class="w-3 h-3 bg-red-500 rounded-full animate-bounce [animation-delay:0.2s]"></div>
              <div class="w-3 h-3 bg-red-500 rounded-full animate-bounce [animation-delay:0.4s]"></div>
            </div>
          </div>
          
          <div v-if="errorMessage" 
               class="absolute inset-0 flex items-center justify-center bg-black/80 backdrop-blur-sm z-10 rounded-2xl">
            <div class="text-red-500 text-xl">{{ errorMessage }}</div>
          </div>

          <client-only>
            <GlobeMap v-if="geoData.length" :points="geoData" />
          </client-only>
        </div>
      </div>
    </section>

    <!-- Providers Analysis -->
    <section v-if="providers.length" class="relative py-24 px-4">
      <div class="max-w-7xl mx-auto">
        <div class="glass-panel p-12 rounded-2xl">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12">
            <h2 class="text-3xl font-bold text-gradient">Provider Analysis</h2>
            <button @click="downloadJSON"
                    class="group flex items-center gap-3 px-6 py-3 rounded-full bg-red-500/10 hover:bg-red-500/20 transition-all duration-300">
              <span class="text-red-500">Export Data</span>
              <svg class="w-5 h-5 text-red-500 transition-transform duration-300 group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </button>
          </div>
          
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="p in providers" 
                 :key="p.label"
                 class="glass-panel p-6 rounded-xl hover-glow">
              <div class="font-semibold text-xl mb-2">{{ p.label }}</div>
              <div class="text-red-400">{{ p.country }} – {{ p.asn }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-12 px-4 border-t border-white/5">
      <div class="max-w-7xl mx-auto text-center">
        <p class="text-gray-500">© 2025 TraceGlobe. All rights reserved.</p>
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
    title: "Secure Analysis",
    description: "Advanced encryption and secure protocols ensure your data remains protected during analysis"
  },
  {
    icon: "🌍",
    title: "Global Tracking",
    description: "Real-time visualization of data flow patterns across our interconnected digital world"
  },
  {
    icon: "📊",
    title: "Privacy Insights",
    description: "Comprehensive analysis of data handling practices and privacy implications"
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
  const tl = gsap.timeline({ defaults: { ease: "expo.out" } })
  
  tl.from('h1', {
    y: 50,
    opacity: 0,
    duration: 1.5
  })
  .from('p', {
    y: 30,
    opacity: 0,
    duration: 1.2
  }, "-=1.2")
  .from('button', {
    y: 30,
    opacity: 0,
    duration: 1
  }, "-=1")
  .from('.glass-panel', {
    y: 50,
    opacity: 0,
    duration: 1,
    stagger: 0.1
  }, "-=0.8")
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
  errorMessage.value = ""
  
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
    
    if (!geoData.value.length) {
      errorMessage.value = "No providers found in analysis."
    }
  } catch (err) {
    errorMessage.value = "Error analyzing providers. Please try again."
  } finally {
    loading.value = false
  }
}

function downloadJSON() {
  window.open(`${config.public.backendUrl}/results/download`, "_blank")
}
</script>