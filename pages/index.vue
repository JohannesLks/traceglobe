<template>
  <div class="relative">
    <!-- Hero Section -->
    <section class="min-h-screen relative px-6 md:px-12 pt-12 pb-24">
      <div class="max-w-6xl mx-auto">
        <div class="text-center space-y-6 relative z-10">
          <h1 class="text-5xl md:text-7xl font-bold">
            <span class="bg-gradient-to-r from-red-500 to-red-300 bg-clip-text text-transparent">TraceGlobe</span>
          </h1>
          <p class="text-xl md:text-2xl text-gray-400 max-w-2xl mx-auto">
            Entdecke, wohin deine Daten reisen. Automatisierte Anbieteranalyse aus deinem Posteingang.
          </p>
          
          <!-- Login Button -->
          <div class="mt-12">
            <button @click="loginWithGoogle" 
                    class="group px-8 py-4 bg-gradient-to-r from-red-600 to-red-800 rounded-xl
                           hover:from-red-500 hover:to-red-700 transform hover:scale-105 transition-all
                           shadow-lg shadow-red-500/20 flex items-center space-x-3 mx-auto">
              <span class="text-2xl">🔐</span>
              <span class="text-lg font-medium">Mit Google anmelden</span>
              <span class="group-hover:translate-x-1 transition-transform">→</span>
            </button>
          </div>
        </div>

        <!-- Features Grid -->
        <div class="grid md:grid-cols-3 gap-8 mt-24 px-4">
          <div class="bg-black/40 backdrop-blur-sm p-6 rounded-2xl border border-red-900/20 hover:border-red-500/30 transition-colors">
            <div class="text-2xl mb-3">📧</div>
            <h3 class="text-lg font-semibold text-red-400 mb-2">E-Mail-Analyse per Login</h3>
            <p class="text-gray-400">Sichere Analyse deines Posteingangs mit modernster Technologie.</p>
          </div>
          <div class="bg-black/40 backdrop-blur-sm p-6 rounded-2xl border border-red-900/20 hover:border-red-500/30 transition-colors">
            <div class="text-2xl mb-3">🔍</div>
            <h3 class="text-lg font-semibold text-red-400 mb-2">Datenschutz-Scans</h3>
            <p class="text-gray-400">Automatische Erkennung von Datenweitergaben und Tracking.</p>
          </div>
          <div class="bg-black/40 backdrop-blur-sm p-6 rounded-2xl border border-red-900/20 hover:border-red-500/30 transition-colors">
            <div class="text-2xl mb-3">🌍</div>
            <h3 class="text-lg font-semibold text-red-400 mb-2">Globale Serverstandorte</h3>
            <p class="text-gray-400">Visualisierung der Datenflüsse in Echtzeit auf unserem 3D-Globus.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Loading State -->
    <div v-if="loading" 
         class="fixed inset-0 bg-black/90 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="text-center space-y-4">
        <div class="animate-spin text-4xl">⚡</div>
        <div class="text-xl text-red-400">Analysiere Anbieterinformationen...</div>
      </div>
    </div>

    <!-- Results Section -->
    <section v-if="!loading && (providers.length || errorMessage)" 
             class="px-6 md:px-12 pb-24">
      <div class="max-w-6xl mx-auto space-y-12">
        <!-- Error Message -->
        <div v-if="errorMessage" 
             class="bg-red-950/50 border border-red-800 text-red-200 p-6 rounded-xl text-center backdrop-blur-sm">
          ⚠️ {{ errorMessage }}
        </div>

        <!-- Globe Visualization -->
        <div v-if="geoData.length" 
             class="rounded-3xl overflow-hidden bg-black/60 backdrop-blur-sm border border-red-900/20">
          <client-only fallback-tag="div" 
                      class="flex items-center justify-center py-12 text-xl text-red-400"
                      fallback="🌍 Initialisiere Globus...">
            <GlobeMap :points="geoData" />
          </client-only>
        </div>

        <!-- Providers List -->
        <div v-if="providers.length" 
             class="bg-black/60 rounded-3xl p-8 backdrop-blur-sm border border-red-900/20">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-semibold text-red-400">📦 Gefundene Anbieter</h2>
            <button @click="downloadJSON" 
                    class="px-4 py-2 bg-gradient-to-r from-red-600 to-red-800 rounded-lg
                           hover:from-red-500 hover:to-red-700 transform hover:scale-105 transition-all
                           shadow-lg shadow-red-500/20 flex items-center space-x-2">
              <span>📥</span>
              <span>JSON Export</span>
            </button>
          </div>
          
          <div class="space-y-2 max-h-[400px] overflow-y-auto custom-scrollbar">
            <div v-for="provider in providers" 
                 :key="provider"
                 class="bg-black/40 p-4 rounded-xl hover:bg-red-950/20 transition-colors
                        border border-red-900/10 hover:border-red-500/20">
              <div class="font-medium">{{ provider.label }}</div>
              <div class="text-sm text-red-400">{{ provider.country }} – {{ provider.asn }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-black/60 border-t border-red-900/20 py-8 mt-12">
      <div class="max-w-6xl mx-auto px-6 md:px-12 flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="text-red-400">© 2025 TraceGlobe</div>
        <div class="flex items-center space-x-6 text-sm text-gray-400">
          <a href="#" class="hover:text-red-400 transition-colors">Impressum</a>
          <a href="#" class="hover:text-red-400 transition-colors">Datenschutz</a>
          <a href="#" class="hover:text-red-400 transition-colors">GitHub</a>
        </div>
      </div>
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
  const width = 500
  const height = 600
  const left = (window.innerWidth - width) / 2
  const top = (window.innerHeight - height) / 2
  const popup = window.open(
    `${config.public.backendUrl}/auth/login`,
    "_blank",
    `popup,width=${width},height=${height},left=${left},top=${top}`
  )

  const checkClosed = setInterval(() => {
    if (popup?.closed) {
      clearInterval(checkClosed)
      fetchData()
    }
  }, 500)
}

function handleAuthMessage(event) {
  if (event.data === "google-auth-success") {
    console.log("✅ Authentifizierung erfolgreich – lade Daten...")
    fetchData()
  }
}

onMounted(() => {
  window.addEventListener("message", handleAuthMessage)
})

onUnmounted(() => {
  window.removeEventListener("message", handleAuthMessage)
})

async function fetchData() {
  loading.value = true
  errorMessage.value = ""
  try {
    const res = await fetch(`${config.public.backendUrl}/gmail/providers`, {
      credentials: "include"
    })

    if (!res.ok) {
      const errText = await res.text()
      console.error("❌ Backend-Fehler:", res.status, errText)
      throw new Error(`Backend: ${res.status}`)
    }

    const data = await res.json()
    console.log("📦 Serverantwort:", data)

    providers.value = data.geodata || []
    geoData.value = data.geodata || []

    if (!geoData.value.length) {
      errorMessage.value = "Keine Anbieter gefunden – Posteingang möglicherweise leer oder Analyse nicht abgeschlossen."
    }
  } catch (err) {
    console.error("❌ Fehler beim Laden:", err)
    errorMessage.value = "Fehler beim Laden der Anbieterinformationen."
  } finally {
    loading.value = false
  }
}

function downloadJSON() {
  window.open(`${config.public.backendUrl}/results/download`, "_blank")
}
</script>

<style>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgb(185 28 28 / 0.5) transparent;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgb(185 28 28 / 0.5);
  border-radius: 20px;
}
</style>