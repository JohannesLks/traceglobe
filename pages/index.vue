<template>
  <div class="p-6 space-y-8 max-w-7xl mx-auto">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-white tracking-tight">TraceGlobe</h1>
      <button @click="loginWithGoogle"
              class="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded transition flex items-center gap-2">
        🔐 Mit Google anmelden
      </button>
    </div>

    <div v-if="loading" class="text-red-400 text-center">⏳ Lade Anbieterinformationen...</div>
    <div v-if="errorMessage" class="text-red-400 text-center">{{ errorMessage }}</div>

    <div v-if="geoData.length" class="border border-red-900/40 rounded-xl overflow-hidden">
      <client-only fallback-tag="div" class="text-center py-12 text-red-400">
        🌍 Initialisiere Globus...
      </client-only>
      <GlobeMap :points="geoData" />
    </div>

    <div v-if="providers.length" class="space-y-2">
      <div class="flex justify-between items-center">
        <h2 class="text-lg text-red-400 font-semibold">📦 Anbieter ({{ providers.length }})</h2>
        <button @click="downloadJSON"
                class="bg-red-700 hover:bg-red-600 px-4 py-1 rounded text-sm text-white transition">
          📥 JSON exportieren
        </button>
      </div>
      <ul class="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
        <li v-for="p in providers" :key="p.label"
            class="bg-black/40 border border-red-900/30 hover:border-red-500/30 p-4 rounded-lg transition">
          <div class="font-semibold">{{ p.label }}</div>
          <div class="text-sm text-red-400">{{ p.country }} – {{ p.asn }}</div>
        </li>
      </ul>
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
  const w = 500, h = 600
  const left = (window.innerWidth - w) / 2
  const top = (window.innerHeight - h) / 2
  const popup = window.open(
    `${config.public.backendUrl}/auth/login`,
    "_blank",
    `popup,width=${w},height=${h},left=${left},top=${top}`
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

onMounted(() => window.addEventListener("message", handleAuthMessage))
onUnmounted(() => window.removeEventListener("message", handleAuthMessage))

async function fetchData() {
  loading.value = true
  errorMessage.value = ""
  try {
    const res = await fetch(`${config.public.backendUrl}/gmail/providers`, {
      credentials: "include"
    })
    if (!res.ok) throw new Error("Fehler vom Server")
    const data = await res.json()
    geoData.value = (data.geodata || []).map(e => ({
      ...e,
      lat: Number(e.lat),
      lng: Number(e.lng)
    }))
    providers.value = data.geodata || []
    if (!geoData.value.length) errorMessage.value = "Keine Anbieter gefunden."
  } catch (err) {
    errorMessage.value = "Fehler beim Laden der Daten."
  } finally {
    loading.value = false
  }
}

function downloadJSON() {
  window.open(`${config.public.backendUrl}/results/download`, "_blank")
}
</script>
