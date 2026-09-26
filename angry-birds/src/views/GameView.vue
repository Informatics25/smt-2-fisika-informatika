<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { initPhysics, destroyPhysics, setAmmoEngine, reloadProjectile } from '../engine/physics'
import { useScoreStore } from '../stores/scoreStore'

import TutorialModal from '../components/TutorialModal.vue'

const router = useRouter()
const route = useRoute()
const scoreStore = useScoreStore()

const isPhysicsReady = ref(false)
const isReloading = ref(false)
const showTutorial = ref(true)

const planetDatabase = {
  '1': {
    name: 'Bumi', g_text: '9.8 m/s²', matter_g: 1.0,
    bg: 'bg-gradient-to-b from-blue-900 via-sky-900 to-slate-900'
  },
  '2': {
    name: 'Bulan', g_text: '1.6 m/s²', matter_g: 0.16,
    bg: 'bg-gradient-to-b from-black via-zinc-900 to-stone-900'
  },
  '3': {
    name: 'Jupiter', g_text: '24.7 m/s²', matter_g: 2.5,
    bg: 'bg-gradient-to-b from-orange-950 via-red-950 to-amber-950'
  }
}

const currentPlanetId = route.query.planet || '1'
const activePlanet = planetDatabase[currentPlanetId]

const score = ref(0)

const ammos = ref([
  { type: 'kayu', count: 3, color: 'bg-amber-700', density: '0.04 g/cm³', bounce: '0.40' },
  { type: 'batu', count: 3, color: 'bg-stone-500', density: '0.10 g/cm³', bounce: '0.20' },
  { type: 'besi', count: 3, color: 'bg-slate-400', density: '0.50 g/cm³', bounce: '0.05' }
])
const selectedAmmo = ref('kayu')
const activeAmmoStats = computed(() => ammos.value.find(a => a.type === selectedAmmo.value))

const showModal = ref(false)
const isVictory = ref(false)
const modalTitle = ref('')
const earnedStars = ref(0)

const isGameEnded = ref(false)
const isWaitingForDebris = ref(false)
const targetsRemaining = ref(4)

const triggerGameOver = async (win) => {
  if (isGameEnded.value) return
  isGameEnded.value = true
  showModal.value = true
  isVictory.value = win

  const totalAmmoRemaining = ammos.value.reduce((sum, ammo) => sum + ammo.count, 0)

  if (win) {
    modalTitle.value = 'LEVEL CLEARED!'
    const bonusPoin = totalAmmoRemaining * 500
    score.value += bonusPoin
  } else {
    modalTitle.value = 'LEVEL FAILED'
  }

  if (score.value >= 6000) { earnedStars.value = 3 }
  else if (score.value >= 4000) { earnedStars.value = 2 }
  else if (score.value >= 1000) { earnedStars.value = 1 }
  else { earnedStars.value = 0 }

  if (score.value > 0) {
    await scoreStore.submitScore(currentPlanetId, score.value)
  }
}

const checkGameState = () => {
  if (isGameEnded.value) return

  if (targetsRemaining.value <= 0) {
    triggerGameOver(true)
    return
  }

  const totalAmmo = ammos.value.reduce((sum, ammo) => sum + ammo.count, 0)

  if (totalAmmo === 0 && !isWaitingForDebris.value) {
    isWaitingForDebris.value = true
    setTimeout(() => {
      if (!isGameEnded.value) {
        if (targetsRemaining.value <= 0) {
          triggerGameOver(true)
        } else {
          triggerGameOver(false)
        }
      }
    }, 3500)
  }
}

const handleScoreUpdate = (points, label) => {
  if (isGameEnded.value) return
  score.value += points
  if (label === 'target') {
    targetsRemaining.value -= 1
  }
  checkGameState()
}

const handleAmmoUsed = () => {
  if (isGameEnded.value) return

  isReloading.value = true

  const currentAmmoIndex = ammos.value.findIndex(a => a.type === selectedAmmo.value)
  if (currentAmmoIndex !== -1 && ammos.value[currentAmmoIndex].count > 0) {
    ammos.value[currentAmmoIndex].count -= 1
  }

  if (ammos.value[currentAmmoIndex].count === 0) {
    const nextAvailableAmmo = ammos.value.find(a => a.count > 0)
    if (nextAvailableAmmo) {
      selectedAmmo.value = nextAvailableAmmo.type
    }
  }

  checkGameState()

  setTimeout(() => {
    const totalAmmo = ammos.value.reduce((sum, ammo) => sum + ammo.count, 0)
    if (!isGameEnded.value && totalAmmo > 0) {
      reloadProjectile(selectedAmmo.value)
      isReloading.value = false
    }
  }, 1500)
}

const selectAmmo = (ammoType) => {
  if (isGameEnded.value) return
  const ammoData = ammos.value.find(a => a.type === ammoType)

  if (ammoData && ammoData.count > 0) {
    selectedAmmo.value = ammoType
    if (!isReloading.value) {
      setAmmoEngine(ammoType)
    }
  }
}

const initGameIfLandscape = () => {
  if (window.innerWidth > window.innerHeight) {
    const canvasContainer = document.getElementById('game-canvas')
    if (canvasContainer && !isPhysicsReady.value) {
      initPhysics(canvasContainer, currentPlanetId, activePlanet.matter_g, handleScoreUpdate, handleAmmoUsed)
      setTimeout(() => { isPhysicsReady.value = true }, 500)
    }
  }
}

const handleResize = () => {
  setTimeout(initGameIfLandscape, 300)
}

onMounted(() => {
  initGameIfLandscape()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  destroyPhysics()
})

const exitGame = () => router.push('/')
const restartGame = () => window.location.reload()
</script>

<template>
  <div id="portrait-warning" class="fixed inset-0 z-[100] bg-slate-950 flex-col items-center justify-center text-center p-8 hidden">
    <svg class="w-20 h-20 text-blue-500 mb-6 animate-[spin_3s_linear_infinite]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
    <h2 class="text-2xl font-black text-white mb-3 tracking-widest">PUTAR LAYAR KAMU</h2>
    <p class="text-slate-400">Game ini membutuhkan ruang lintasan yang panjang. Silakan putar HP kamu ke mode <b>Mendatar (Landscape)</b> untuk bermain.</p>
  </div>

  <div id="game-container" :class="['relative w-full h-screen overflow-hidden bg-black flex flex-col']">

    <div class="absolute inset-0 z-0 pointer-events-none" :class="activePlanet.bg"></div>
    <div class="stars stars-small"></div>
    <div class="stars stars-medium"></div>
    <div class="stars stars-large"></div>

    <div v-if="currentPlanetId === '1'" class="absolute inset-0 z-0 pointer-events-none opacity-60">
      <div class="absolute top-20 left-20 w-64 h-20 bg-white rounded-full blur-2xl opacity-20"></div>
      <div class="absolute bottom-10 right-32 w-[120%] h-32 bg-sky-400 rounded-t-[100%] blur-3xl opacity-10"></div>
    </div>

    <div v-else-if="currentPlanetId === '2'" class="absolute inset-0 z-0 pointer-events-none opacity-40">
      <div class="absolute bottom-5 left-10 w-32 h-8 bg-zinc-800 rounded-[100%] border-t border-zinc-600 blur-[2px]"></div>
      <div class="absolute bottom-12 right-40 w-48 h-10 bg-zinc-800 rounded-[100%] border-t border-zinc-600 blur-[3px]"></div>
    </div>

    <div v-else-if="currentPlanetId === '3'" class="absolute inset-0 z-0 pointer-events-none opacity-70">
      <div class="absolute top-[20%] -left-10 w-[120%] h-60 bg-red-700 blur-[80px] rounded-[100%] opacity-40 transform -rotate-2"></div>
      <div class="absolute top-[50%] right-20 w-64 h-24 bg-orange-600 blur-[60px] rounded-[100%] opacity-50 transform rotate-6"></div>
    </div>

    <div v-if="!isPhysicsReady" class="absolute inset-0 z-40 bg-slate-950 flex flex-col items-center justify-center">
      <div class="relative w-16 h-16 md:w-24 md:h-24 mb-6">
        <div class="absolute w-full h-full border-4 border-slate-800 rounded-full"></div>
        <div class="absolute w-full h-full border-4 border-emerald-500 rounded-full border-t-transparent animate-spin"></div>
      </div>
      <p class="text-emerald-400 text-sm md:text-base font-bold tracking-widest uppercase animate-pulse">Menyiapkan Gravitasi...</p>
    </div>

    <div id="game-canvas" class="absolute inset-0 z-10 opacity-100 w-full h-full"></div>

    <div class="absolute inset-0 z-20 pointer-events-none p-2 md:p-6">

      <div class="flex justify-between items-start w-full">

        <div class="flex flex-wrap gap-1.5 md:gap-3 items-start max-w-[70%] pointer-events-auto origin-top-left transform scale-[0.65] sm:scale-80 md:scale-100">

          <button @click="exitGame" class="p-2 md:p-3 bg-white/10 backdrop-blur border border-white/20 rounded-xl hover:bg-white/20 transition-colors shadow-lg">
            <svg class="w-4 h-4 md:w-6 md:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          </button>

          <button @click="showTutorial = true" class="p-2 md:p-3 bg-blue-500/20 backdrop-blur border border-blue-500/50 rounded-xl hover:bg-blue-500/40 transition-colors shadow-lg flex items-center justify-center">
            <svg class="w-4 h-4 md:w-6 md:h-6 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          </button>

          <div class="bg-white/10 backdrop-blur border border-white/20 shadow-lg rounded-xl p-1.5 px-3 md:p-3 md:px-5 flex flex-col h-fit">
            <span class="text-[8px] md:text-xs font-bold text-slate-300 uppercase tracking-wider mb-0.5">Sektor</span>
            <div class="flex items-center gap-1 md:gap-3 text-xs md:text-lg">
              <span class="font-bold text-white">{{ activePlanet.name }}</span>
              <span class="text-white/50">|</span>
              <span class="font-mono text-slate-200">{{ activePlanet.g_text }}</span>
            </div>
          </div>

          <div class="flex bg-slate-900/60 backdrop-blur-md border border-sky-500/30 shadow-lg rounded-xl p-1.5 px-3 md:p-3 md:px-5 flex-col w-fit h-fit">
            <span class="text-[8px] md:text-[10px] font-bold text-sky-400 uppercase tracking-widest mb-0.5 md:mb-2 flex items-center gap-1">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 3h6v6H9V9z"></path></svg>
              Telemetry
            </span>
            <div class="grid grid-cols-2 gap-x-3 md:gap-x-6 gap-y-0.5 md:gap-y-1 text-[9px] md:text-xs font-mono">
              <span class="text-slate-400">Tipe:</span>
              <span class="text-white font-bold capitalize">{{ activeAmmoStats?.type || '-' }}</span>
              <span class="text-slate-400">Padat:</span>
              <span class="text-amber-400 font-bold">{{ activeAmmoStats?.density || '-' }}</span>
            </div>
          </div>
        </div>

        <div class="bg-white/10 backdrop-blur border border-white/20 shadow-lg rounded-xl p-1.5 px-3 md:p-3 md:px-6 text-right pointer-events-auto origin-top-right transform scale-[0.65] sm:scale-80 md:scale-100">
          <span class="text-[8px] md:text-xs font-bold text-slate-300 uppercase tracking-wider mb-0.5">Skor</span>
          <div class="text-sm md:text-3xl font-black text-white font-mono">{{ score.toString().padStart(5, '0') }}</div>
        </div>

      </div>

      <div class="absolute bottom-2 md:bottom-6 left-1/2 -translate-x-1/2 flex flex-col items-center gap-0.5 md:gap-1 pointer-events-auto origin-bottom transform scale-[0.75] sm:scale-90 md:scale-100">
        <span v-if="isReloading" class="text-[9px] md:text-xs font-bold text-yellow-400 animate-pulse tracking-widest bg-slate-900/80 px-3 py-0.5 rounded-full shadow-lg">MEMUAT...</span>
        <span v-else class="text-[9px] md:text-xs font-bold text-slate-300 uppercase tracking-wider drop-shadow-md bg-slate-900/60 px-4 py-0.5 rounded-t-lg shadow-lg">AMUNISI</span>

        <div class="bg-slate-900/90 backdrop-blur-xl border border-slate-600 p-1 md:p-2 rounded-xl flex gap-1 md:gap-3 shadow-2xl">
          <button
              v-for="ammo in ammos"
              :key="ammo.type"
              @click="selectAmmo(ammo.type)"
              :disabled="ammo.count === 0 || showModal"
              class="relative px-2 py-1 md:px-5 md:py-2 rounded-lg transition-all border-2 flex flex-col items-center min-w-[50px] md:min-w-[90px] disabled:opacity-30 disabled:cursor-not-allowed"
              :class="selectedAmmo === ammo.type ? 'border-blue-500 bg-slate-800 scale-105' : 'border-slate-800 bg-slate-950/50 hover:bg-slate-800'"
          >
            <div class="absolute -top-1.5 -right-1.5 md:-top-3 md:-right-3 w-5 h-5 md:w-7 md:h-7 rounded-full bg-slate-800 border-2 border-slate-600 flex items-center justify-center text-[9px] md:text-xs font-bold text-white shadow-lg">
              {{ ammo.count }}
            </div>
            <div class="w-3 h-3 md:w-7 md:h-7 rounded-full mb-0.5 md:mb-1 shadow-[inset_0_2px_4px_rgba(0,0,0,0.6)]" :class="ammo.color"></div>
            <span class="text-[10px] md:text-sm font-bold capitalize text-white">{{ ammo.type }}</span>
          </button>
        </div>
      </div>

    </div>

    <TutorialModal :show="showTutorial" @close="showTutorial = false" />

    <div v-if="showModal" class="absolute inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-2 overflow-y-auto pointer-events-auto">
      <div class="bg-slate-900 border-2 border-slate-700 p-4 md:p-8 rounded-2xl md:rounded-3xl shadow-[0_0_50px_rgba(0,0,0,0.8)] text-center max-w-sm md:max-w-md w-full transform transition-all scale-100">

        <h2 class="text-lg sm:text-xl md:text-3xl font-black mb-2 md:mb-6 drop-shadow-lg" :class="isVictory ? 'text-emerald-400' : 'text-red-500'">
          {{ modalTitle }}
        </h2>

        <div class="flex justify-center gap-1 md:gap-2 mb-2 md:mb-6">
          <svg v-for="n in 3" :key="n"
               class="w-8 h-8 sm:w-10 sm:h-10 md:w-16 md:h-16 transform transition-all duration-500"
               :class="n <= earnedStars ? 'text-yellow-400 scale-110 drop-shadow-[0_0_10px_rgba(250,204,21,0.6)]' : 'text-slate-700'"
               fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        </div>

        <div class="bg-slate-950/50 rounded-lg md:rounded-2xl p-2 md:p-4 mb-3 md:mb-8 border border-slate-800">
          <p class="text-slate-400 font-bold uppercase tracking-widest text-[8px] md:text-xs mb-0.5 md:mb-1">Total Skor</p>
          <p class="text-2xl sm:text-3xl md:text-5xl font-mono font-black text-white drop-shadow-md">{{ score.toString().padStart(5, '0') }}</p>
        </div>

        <div class="flex flex-row gap-2 md:gap-3 justify-center">
          <button @click="exitGame" class="flex-1 py-1.5 md:py-4 rounded-lg md:rounded-xl font-bold text-[9px] sm:text-[10px] md:text-base text-slate-300 bg-slate-800 hover:bg-slate-700 hover:text-white transition-all">
            KEMBALI KE MENU
          </button>
          <button @click="restartGame" class="flex-1 py-1.5 md:py-4 rounded-lg md:rounded-xl font-bold text-[9px] sm:text-[10px] md:text-base text-white shadow-lg transform transition-all active:scale-95" :class="isVictory ? 'bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400' : 'bg-gradient-to-r from-orange-600 to-red-500 hover:from-orange-500 hover:to-red-400'">
            {{ isVictory ? 'MAINKAN LAGI' : 'COBA LAGI' }}
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
@media screen and (max-width: 800px) and (orientation: portrait) {
  #portrait-warning { display: flex !important; }
  #game-container { display: none !important; }
}

.stars {
  position: absolute;
  top: 0;
  left: 0;
  width: 200%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.stars-small {
  background-image:
      radial-gradient(1px 1px at 20px 30px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(1px 1px at 40px 70px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(1px 1px at 50px 160px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(1px 1px at 90px 40px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(1px 1px at 130px 80px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(1px 1px at 160px 120px, #ffffff, rgba(0,0,0,0));
  background-repeat: repeat;
  background-size: 200px 200px;
  animation: moveStarsHorizontal 60s linear infinite;
  opacity: 0.4;
}

.stars-medium {
  background-image:
      radial-gradient(2px 2px at 100px 150px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(2px 2px at 60px 50px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(2px 2px at 180px 80px, #ffffff, rgba(0,0,0,0));
  background-repeat: repeat;
  background-size: 300px 300px;
  animation: moveStarsHorizontal 40s linear infinite;
  opacity: 0.6;
}

.stars-large {
  background-image:
      radial-gradient(3px 3px at 50px 200px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(3px 3px at 200px 60px, #ffffff, rgba(0,0,0,0));
  background-repeat: repeat;
  background-size: 400px 400px;
  animation: moveStarsHorizontal 20s linear infinite;
  opacity: 0.9;
}

@keyframes moveStarsHorizontal {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

#game-container {
  touch-action: none;
  user-select: none;
  -webkit-user-select: none;
  -webkit-touch-callout: none;
}
</style>

