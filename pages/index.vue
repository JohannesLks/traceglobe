<template>
  <div class="min-h-screen bg-gradient-to-b from-black to-gray-900 p-6 md:p-12">
    <div class="max-w-6xl mx-auto space-y-8">
      <!-- Header Section -->
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-500 to-cyan-400 bg-clip-text text-transparent">
          Globe Tracker
        </h1>
      </div>

      <!-- Login Button -->
      <div class="flex justify-center">
        <button @click="loginWithGoogle" 
                class="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-800 text-white rounded-lg
                       hover:from-blue-700 hover:to-blue-900 transform hover:scale-105 transition-all
                       shadow-lg shadow-blue-500/20 flex items-center space-x-2">
          <span>🔐</span>
          <span>Mit Google anmelden</span>
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8 text-xl text-blue-400">
        <div class="animate-pulse">⏳ Lade Anbieterinformationen...</div>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" 
           class="bg-red-900/50 border border-red-500 text-red-200 p-4 rounded-lg text-center">
        ⚠️ {{ errorMessage }}
      </div>

      <!-- Providers List -->
      <div v-else-if="providers.length" class="bg-gray-800/50 rounded-2xl p-6 backdrop-blur-sm">
        <h2 class="text-2xl font-semibold mb-4 text-blue-400">📦 Gefundene Anbieter</h2>
        <ul class="space-y-2">
          <li v-for="provider in providers" 
              :key="provider"
              class="bg-gray-700/30 p-3 rounded-lg hover:bg-gray-700/50 transition-colors">
            {{ provider.label }} 
            <span class="text-blue-400">({{ provider.country }} – {{ provider.asn }})</span>
          </li>
        </ul>

        <button @click="downloadJSON" 
                class="mt-6 px-4 py-2 bg-gradient-to-r from-green-600 to-green-800 text-white rounded-lg
                       hover:from-green-700 hover:to-green-900 transform hover:scale-105 transition-all
                       shadow-lg shadow-green-500/20">
          📥 JSON herunterladen
        </button>
      </div>

      <!-- Globe Map -->
      <div class="rounded-2xl overflow-hidden bg-gray-800/30 backdrop-blur-sm">
        <client-only fallback-tag="div" fallback="🗺️ Lade Globus...">
          <GlobeMap v-if="geoData.length" :points="geoData" />
        </client-only>
      </div>
    </div>
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