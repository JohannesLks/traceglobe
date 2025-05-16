<template>
  <div ref="globeContainer" class="w-full h-[600px] md:h-[800px]" />
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import Globe from 'globe.gl'

const props = defineProps({ points: Array })
const globeContainer = ref(null)
let globe = null

function handleResize() {
  if (globe && globeContainer.value) {
    globe.width(globeContainer.value.clientWidth)
    globe.height(globeContainer.value.clientHeight)
  }
}

function initGlobe() {
  if (!globeContainer.value) return

  globe = Globe()(globeContainer.value)
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
    .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
    .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
    .atmosphereColor('#ff2d55')
    .atmosphereAltitude(0.25)
    .pointColor(() => '#ff2d55')
    .pointRadius(0.6)
    .pointAltitude(0.08)
    .pointLabel('label')
    .pointLat('lat')
    .pointLng('lng')
    .pointOfView({ lat: 30, lng: 0, altitude: 2.5 })
    .width(globeContainer.value.clientWidth)
    .height(globeContainer.value.clientHeight)

  // auto rotate
  const rotate = () => {
    if (!globe) return
    const rotation = globe.controls().autoRotate = true
    globe.controls().autoRotateSpeed = 0.3
  }
  rotate()
}

watch(() => props.points, (newPoints) => {
  if (globe) globe.pointsData(newPoints || [])
}, { deep: true })

onMounted(() => {
  setTimeout(() => initGlobe(), 50)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  globe?._destructor()
})
</script>
