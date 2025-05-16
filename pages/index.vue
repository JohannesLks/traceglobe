<template>
  <div class="p-6 space-y-6">
    <button @click="loginWithGoogle" class="px-4 py-2 bg-blue-600 text-white rounded">
      🔐 Mit Google anmelden
    </button>

    <div v-if="loading">⏳ Lade Anbieterinformationen...</div>
    <div v-else-if="providers.length">
      <h2 class="text-xl font-semibold">📦 Gefundene Anbieter:</h2>
      <ul class="list-disc pl-6">
        <li v-for="provider in providers" :key="provider">{{ provider }}</li>
      </ul>

      <button @click="downloadJSON" class="mt-4 px-4 py-2 bg-green-600 text-white rounded">
        📥 JSON herunterladen
      </button>
    </div>

    <client-only fallback-tag="div" fallback="🗺️ Lade Globus...">
      <GlobeMap v-if="geoData.length" :points="geoData" />
    </client-only>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import GlobeMap from '~/components/GlobeMap.vue'
const config = useRuntimeConfig()

const providers = ref([])
const geoData = ref([])
const loading = ref(false)

function loginWithGoogle() {
  const width = 500, height = 600
  const left = (window.innerWidth - width) / 2
  const top = (window.innerHeight - height) / 2
  const popup = window.open(`${config.public.backendUrl}/auth/login`, "_blank",
    `popup,width=${width},height=${height},left=${left},top=${top}`)

  window.addEventListener("message", (event) => {
    if (event.data === "google-auth-success") {
      fetchData()
    }
  })
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
  try {
    const res = await fetch(`${config.public.backendUrl}/gmail/providers`, {
      credentials: "include"
    })
    const data = await res.json()
    providers.value = data.providers || []
    geoData.value = data.geodata || []
  } catch (err) {
    console.error("❌ Fehler beim Laden:", err)
  } finally {
    loading.value = false
  }
}

function downloadJSON() {
  window.open(`${config.public.backendUrl}/results/download`, "_blank")
}
</script>
