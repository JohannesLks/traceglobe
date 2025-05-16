<template>
  <div id="globeViz" ref="globeContainer" style="height: 600px;"></div>
</template>

<script setup>
import { onMounted, onUnmounted, watch, ref } from 'vue'
import Globe from 'globe.gl'

const props = defineProps({
  points: Array
})

const globeContainer = ref(null)
let globe = null

onMounted(() => {
  initGlobe()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (globe) {
    globe._destructor()
  }
})

function handleResize() {
  if (globe && globeContainer.value) {
    globe.width(globeContainer.value.clientWidth)
    globe.height(globeContainer.value.clientHeight)
  }
}

function initGlobe() {
  if (!globeContainer.value) return
  
  globe = Globe()(globeContainer.value)
  globe
    .pointOfView({ lat: 20, lng: 0, altitude: 2 })
    .pointsData(props.points || [])
    .pointLabel('label')
    .pointLat('lat')
    .pointLng('lng')
    .pointColor(() => 'rgba(0,200,255,0.8)')
    .pointAltitude(0.01)
    .width(globeContainer.value.clientWidth)
    .height(globeContainer.value.clientHeight)
}

watch(() => props.points, (newPoints) => {
  if (globe) {
    globe.pointsData(newPoints || [])
  }
}, { deep: true })
</script>