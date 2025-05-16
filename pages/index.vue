<template>
  <div class="min-h-screen p-6 bg-black text-white font-jetbrains space-y-8">
    <div class="flex justify-between items-center">
      <h1 class="text-xl text-red-500 tracking-wider">TraceGlobe</h1>
      <button @click="loginWithGoogle"
              class="bg-red-500 hover:bg-red-400 text-black px-4 py-2 rounded transition">
        🔐 Login
      </button>
    </div>

    <div v-if="loading" class="text-center text-red-500 animate-pulse">⏳ Lade Anbieterinformationen...</div>
    <div v-if="errorMessage" class="text-center text-red-500">{{ errorMessage }}</div>

    <client-only fallback-tag="div" class="text-center text-red-500">
      <GlobeMap v-if="geoData.length" :points="geoData" />
    </client-only>

    <div v-if="providers.length" class="bg-white/5 p-6 rounded-xl backdrop-blur-md border border-red-500/10">
      <div class="flex justify-between mb-4">
        <h2 class="text-red-500 text-lg font-semibold">📦 Anbieter</h2>
        <button @click="downloadJSON"
                class="text-sm px-4 py-1 bg-red-500 hover:bg-red-400 text-black rounded transition">
          📥 JSON export
        </button>
      </div>
      <ul class="grid md:grid-cols-2 gap-3">
        <li v-for="p in providers" :key="p.label"
            class="border border-red-500/10 rounded-lg p-4 hover:bg-red-500/10 transition">
          <div class="text-white font-semibold">{{ p.label }}</div>
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

onMounted(() => window.addEventListener("message", handleAuthMessage))
onUnmounted(() => window.removeEventListener("message", handleAuthMessage))

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
    if (!geoData.value.length) errorMessage.value = "Keine Anbieter gefunden."
  } catch (err) {
    errorMessage.value = "Fehler beim Laden."
  } finally {
    loading.value = false
  }
}

function downloadJSON() {
  window.open(`${config.public.backendUrl}/results/download`, "_blank")
}
</script>
