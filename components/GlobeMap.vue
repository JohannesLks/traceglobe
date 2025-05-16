<template>
  <div id="globeViz" style="height: 600px;"></div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import Globe from 'globe.gl'

const props = defineProps({
  points: Array
})

watch(() => props.points, drawGlobe, { immediate: true })

function drawGlobe() {
  const globe = Globe()(document.getElementById('globeViz'))
  globe
    .pointOfView({ lat: 20, lng: 0, altitude: 2 })
    .pointsData(props.points)
    .pointLabel('label')
    .pointLat('lat')
    .pointLng('lng')
    .pointColor(() => 'rgba(0,200,255,0.8)')
    .pointAltitude(0.01)
}
</script>
