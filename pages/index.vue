<template>
  <div class="p-6 space-y-6">
    <button @click="loginWithGoogle" class="px-4 py-2 bg-blue-600 text-white rounded">
      🔐 Mit Google anmelden
    </button>

    <div v-if="loading">⏳ Lade Anbieterinformationen...</div>

    <div v-if="errorMessage" class="text-red-600 font-semibold">
      ⚠️ {{ errorMessage }}
    </div>

    <div v-else-if="providers.length">
      <h2 class="text-xl font-semibold">📦 Gefundene Anbieter:</h2>
      <ul class="list-disc pl-6">
        <li v-for="provider in providers" :key="provider">
          {{ provider.label }} ({{ provider.country }} – {{ provider.asn }})
        </li>
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
      fetchData() // Sicherheitsfallback
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
