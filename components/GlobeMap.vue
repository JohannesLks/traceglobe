<template>
  <div id="globeViz" ref="globeContainer" class="h-[600px] md:h-[800px] w-full"></div>
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
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
    .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
    .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
    .pointOfView({ lat: 20, lng: 0, altitude: 2.5 })
    .pointsData(props.points || [])
    .pointLabel('label')
    .pointLat('lat')
    .pointLng('lng')
    .pointColor(() => '#00ffff')
    .pointAltitude(0.1)
    .pointRadius(0.5)
    .atmosphereColor('#1d4ed8')
    .atmosphereAltitude(0.25)
    .width(globeContainer.value.clientWidth)
    .height(globeContainer.value.clientHeight)
}
  
watch(() => props.points, (newPoints) => {
  if (globe) {
    globe.pointsData(newPoints || [])
  }
}, { deep: true })
</script>