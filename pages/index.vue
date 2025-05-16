<template>
  <div class="bg-black text-white min-h-screen font-sans selection:bg-red-500/30 selection:text-white">
    <!-- Hero -->
    <section class="min-h-screen flex flex-col items-center justify-center text-center px-6 relative overflow-hidden">
      <!-- Background glow -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-red-500/20 rounded-full blur-[120px] opacity-20 z-0 animate-float" />
      <div class="relative z-10 max-w-3xl">
        <h1 class="text-5xl md:text-7xl font-bold text-gradient mb-6 tracking-tight">TraceGlobe</h1>
        <p class="text-xl text-gray-400 leading-relaxed mb-10">
          Discover where your email data really travels – visualized in realtime across the globe.
        </p>
        <button @click="loginWithGoogle"
                class="group px-8 py-4 bg-gradient-to-r from-red-500 to-red-600 rounded-full text-white font-semibold text-lg transition-all hover:scale-105 hover:shadow-[0_0_30px_rgba(255,45,85,0.3)]">
           Connect with Google
        </button>
      </div>
    </section>

    <!-- Globe Section -->
    <section class="px-6 py-20 max-w-7xl mx-auto w-full">
      <div class="glass-panel rounded-2xl overflow-hidden relative">
        <client-only>
          <GlobeMap v-if="geoData.length" :points="geoData" />
        </client-only>
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-black/80 backdrop-blur-sm z-10">
          <div class="animate-pulse text-red-500 text-xl">⏳ Loading providers...</div>
        </div>
        <div v-if="errorMessage" class="absolute inset-0 flex items-center justify-center bg-black/80 backdrop-blur-sm z-10">
          <div class="text-red-500 text-lg">{{ errorMessage }}</div>
        </div>
      </div>
    </section>

    <!-- Providers -->
    <section v-if="providers.length" class="px-6 pb-24 max-w-7xl mx-auto w-full">
      <div class="flex justify-between items-center mb-8">
        <h2 class="text-2xl font-bold text-gradient"> Providers Found</h2>
        <button @click="downloadJSON"
                class="px-5 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-500 rounded-full font-medium transition">
           Export JSON
        </button>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="p in providers" :key="p.label"
             class="glass-panel p-6 rounded-xl hover:shadow-[0_0_30px_rgba(255,45,85,0.1)] transition">
          <div class="text-xl font-semibold mb-1">{{ p.label }}</div>
          <div class="text-red-400 text-sm">{{ p.country }} – {{ p.asn }}</div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="text-center text-gray-500 text-sm py-10 border-t border-white/5">
      © 2025 TraceGlobe by CyberVision Labs
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import GlobeMap from '~/components/GlobeMap.vue'

const config = useRuntimeConfig()
const providers = ref([])
const geoData = ref([])
const loading = ref(false)
const errorMessage = ref("")

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
    if (!geoData.value.length) errorMessage.value = "No providers found."
  } catch {
    errorMessage.value = "Error loading provider data."
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  window.addEventListener("message", handleAuthMessage)
})
onUnmounted(() => {
  window.removeEventListener("message", handleAuthMessage)
})
</script>
