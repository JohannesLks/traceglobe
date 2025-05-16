<template>
  <div id="globeViz" 
       ref="globeContainer" 
       class="w-full h-[600px] md:h-[800px] rounded-xl overflow-hidden border border-red-500/20 shadow-xl shadow-red-500/10 transition-all duration-300 hover:border-red-500/30" />
</template>

<script setup>
import { onMounted, onUnmounted, watch, ref } from 'vue'
import Globe from 'globe.gl'
import { gsap } from 'gsap'

const props = defineProps({ points: Array })
const globeContainer = ref(null)
let globe = null

onMounted(() => {
  setTimeout(() => {
    initGlobe()
    animateGlobe()
  }, 50)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  globe?._destructor()
})

function handleResize() {
  if (globe && globeContainer.value) {
    globe.width(globeContainer.value.clientWidth)
    globe.height(globeContainer.value.clientHeight)
  }
}

function animateGlobe() {
  if (!globe) return
  
  gsap.to({}, {
    duration: 180,
    repeat: -1,
    onUpdate: () => {
      const rotation = globe.rotation()
      globe.rotation({ ...rotation, lng: rotation.lng + 0.1 })
    }
  })
}

function initGlobe() {
  if (!globeContainer.value) return

  globe = Globe()(globeContainer.value)
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
    .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
    .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
    .atmosphereColor('#ff2d55')
    .atmosphereAltitude(0.3)
    .pointColor(() => '#ff2d55')
    .pointRadius(0.5)
    .pointAltitude(0.06)
    .pointLabel('label')
    .pointLat('lat')
    .pointLng('lng')
    .pointOfView({ lat: 20, lng: 0, altitude: 2.2 })
    .width(globeContainer.value.clientWidth)
    .height(globeContainer.value.clientHeight)

  // Add glow effect
  globe.pointsMerge(true)
    .pointsTransitionDuration(1000)
}

watch(() => props.points, (newPoints) => {
  if (globe) {
    globe.pointsData([])
    gsap.to({}, {
      duration: 0.5,
      onComplete: () => {
        globe.pointsData(newPoints || [])
      }
    })
  }
}, { deep: true })
</script>