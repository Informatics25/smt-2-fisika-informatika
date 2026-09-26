<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { useScoreStore } from "../stores/scoreStore.js"

const planets = computed(() => {
  const earthStars = scoreStore.userHighScores['1']?.stars || 0
  const moonStars = scoreStore.userHighScores['2']?.stars || 0
  const isJupiterUnlocked = earthStars > 0 && moonStars > 0

  return [
    { id: '1', name: 'Bumi', gravity: '9.8 m/s²', color: 'from-blue-500 to-cyan-400', locked: false },
    { id: '2', name: 'Bulan', gravity: '1.6 m/s²', color: 'from-slate-400 to-slate-600', locked: false },
    { id: '3', name: 'Jupiter', gravity: '24.7 m/s²', color: 'from-orange-500 to-amber-600', locked: !isJupiterUnlocked }
  ]
})

const selectedPlanet = ref('1')

const router = useRouter()
const authStore = useAuthStore()
const scoreStore = useScoreStore()

const showLeaderboard = ref(false)

const openLeaderboard = async () => {
  showLeaderboard.value = true
  await scoreStore.fetchLeaderboard(selectedPlanet.value)
}

onMounted(async () => {
  if (!authStore.user) {
    await authStore.initialize()
  }
  if (authStore.user) {
    await scoreStore.fetchUserHighScores()
  }
})

const playGame = () => {
  router.push(`/game?planet=${selectedPlanet.value}`)
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen p-4 md:p-8 flex flex-col bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-800 via-slate-950 to-black text-slate-100 relative overflow-x-hidden">

    <div class="stars stars-small"></div>
    <div class="stars stars-medium"></div>
    <div class="stars stars-large"></div>

    <div class="fixed top-[-10%] left-[-10%] w-72 h-72 md:w-96 md:h-96 bg-blue-600/10 rounded-full blur-[80px] md:blur-[100px] animate-float-1 pointer-events-none"></div>
    <div class="fixed bottom-[-10%] right-[-10%] w-72 h-72 md:w-96 md:h-96 bg-emerald-600/10 rounded-full blur-[80px] md:blur-[100px] animate-float-2 pointer-events-none"></div>

    <header
        v-motion
        :initial="{ opacity: 0, y: -30 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 100, duration: 600, type: 'spring' } }"
        class="flex flex-col md:flex-row justify-between items-center gap-6 mb-10 md:mb-16 relative z-10"
    >
      <h1 class="text-3xl md:text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-emerald-400 to-teal-300 drop-shadow-lg tracking-wider text-center">
        AstroSling
      </h1>

      <div class="flex flex-wrap justify-center items-center gap-3 w-full md:w-auto">
        <button @click="openLeaderboard" class="flex items-center justify-center p-2.5 bg-slate-900/60 backdrop-blur-md border border-yellow-500/50 text-yellow-400 rounded-full hover:bg-yellow-500/20 hover:text-yellow-300 transition-all hover:scale-110 shadow-[0_0_15px_rgba(234,179,8,0.2)]" title="Leaderboard Global">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path></svg>
        </button>

        <div class="flex items-center gap-2 md:gap-3 bg-slate-900/60 backdrop-blur-md px-4 py-2 rounded-full border border-slate-700/50 shadow-lg">
          <div class="w-6 h-6 md:w-8 md:h-8 rounded-full bg-gradient-to-tr from-blue-600 to-emerald-500 flex items-center justify-center font-bold text-xs md:text-base text-white shadow-inner">
            {{ authStore.namaLengkap ? authStore.namaLengkap.charAt(0).toUpperCase() : 'U' }}
          </div>
          <span class="font-bold text-xs md:text-sm tracking-wide text-slate-200">{{ authStore.namaLengkap || 'Space Cadet' }}</span>
        </div>

        <button @click="handleLogout" class="p-2.5 bg-slate-900/60 backdrop-blur-md border border-red-900/50 text-red-400 rounded-full hover:bg-red-900/80 hover:text-red-300 transition-all hover:scale-110 shadow-lg" title="Keluar Sistem">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
        </button>
      </div>
    </header>

    <main class="flex-1 flex flex-col items-center justify-start md:justify-center max-w-5xl mx-auto w-full relative z-10 pb-10 mt-4 md:mt-0">

      <div
          v-motion
          :initial="{ opacity: 0, scale: 0.8 }"
          :enter="{ opacity: 1, scale: 1, transition: { delay: 300, type: 'spring' } }"
          class="inline-block px-4 py-2 md:px-6 md:py-2 mb-8 md:mb-10 rounded-full border border-slate-700/50 bg-slate-800/30 backdrop-blur-sm"
      >
        <h2 class="text-lg md:text-2xl font-black text-center tracking-widest text-slate-300 uppercase">Pilih Sektor Planet</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 w-full mb-10 md:mb-16 px-4 md:px-0">
        <button
            v-for="(planet, index) in planets"
            :key="planet.id"
            v-motion
            :initial="{ opacity: 0, y: 50 }"
            :enter="{ opacity: 1, y: 0, transition: { delay: 400 + (index * 150), type: 'spring', stiffness: 200, damping: 20 } }"
            @click="!planet.locked && (selectedPlanet = planet.id)"
            :disabled="planet.locked"
            class="relative p-6 md:p-8 rounded-3xl border border-slate-700/50 transition-all duration-300 text-left overflow-hidden group disabled:opacity-40 disabled:cursor-not-allowed bg-slate-900/40 backdrop-blur-md flex flex-col"
            :class="selectedPlanet === planet.id ? 'ring-2 ring-blue-500 shadow-[0_0_40px_rgba(59,130,246,0.2)] transform md:scale-105 bg-slate-800/60' : 'hover:border-slate-500 hover:bg-slate-800/50'"
        >
          <div class="absolute -right-12 -top-12 w-48 h-48 rounded-full opacity-40 bg-gradient-to-br blur-2xl group-hover:opacity-60 transition-opacity" :class="planet.color"></div>
          <div class="absolute -right-4 -top-4 w-20 h-20 md:w-24 md:h-24 rounded-full opacity-80 bg-gradient-to-br" :class="planet.color"></div>

          <div v-if="!planet.locked" class="relative z-10 flex gap-1 mb-3">
            <svg v-for="n in 3" :key="n"
                 class="w-5 h-5 drop-shadow-md transition-colors"
                 :class="n <= (scoreStore.userHighScores[planet.id]?.stars || 0) ? 'text-yellow-400' : 'text-slate-700/80'"
                 fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>

          <h3 class="text-2xl md:text-3xl font-black mb-2 md:mb-3 relative z-10 drop-shadow-md">{{ planet.name }}</h3>

          <div class="relative z-10 flex items-center gap-2 mt-auto">
            <span class="text-slate-400 text-[10px] md:text-xs uppercase tracking-widest font-bold">Gravitasi</span>
            <span class="font-mono font-bold text-xs md:text-sm text-slate-200 bg-slate-950/50 px-2 py-1 rounded">{{ planet.gravity }}</span>
          </div>

          <div v-if="planet.locked" class="absolute top-4 right-4 md:top-6 md:right-6 text-slate-400 z-10 bg-slate-900 p-2 rounded-full shadow-inner">
            <svg class="w-5 h-5 md:w-6 md:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
          </div>
          <div v-else-if="selectedPlanet === planet.id" class="absolute top-4 right-4 md:top-6 md:right-6 text-blue-400 z-10 bg-blue-900/30 p-2 rounded-full border border-blue-500/50">
            <svg class="w-5 h-5 md:w-6 md:h-6 drop-shadow-[0_0_8px_rgba(96,165,250,1)]" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
          </div>
        </button>
      </div>

      <button
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 900, type: 'spring' } }"
          @click="playGame"
          class="w-[90%] md:w-auto relative px-10 md:px-20 py-4 md:py-5 bg-gradient-to-r from-blue-600 to-emerald-500 hover:from-blue-500 hover:to-emerald-400 text-white text-lg md:text-xl font-black tracking-widest rounded-2xl overflow-hidden group shadow-[0_0_30px_rgba(16,185,129,0.3)] transform transition-all active:scale-95"
      >
        <span class="relative z-10">LUNCURKAN</span>
        <div class="absolute inset-0 h-full w-full bg-white/20 group-hover:translate-x-full transition-transform duration-500 -translate-x-full skew-x-12"></div>
      </button>
    </main>

    <div v-if="showLeaderboard" class="absolute inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm px-4 fixed">
      <div
          v-motion
          :initial="{ opacity: 0, scale: 0.9 }"
          :enter="{ opacity: 1, scale: 1, transition: { type: 'spring', stiffness: 250, damping: 20 } }"
          class="bg-slate-900 border border-slate-700 p-6 md:p-8 rounded-3xl shadow-2xl w-full max-w-lg"
      >
        <div class="flex justify-between items-center mb-6 border-b border-slate-800 pb-4">
          <h2 class="text-xl md:text-2xl font-black text-yellow-400 flex items-center gap-2 md:gap-3">
            <svg class="w-6 h-6 md:w-7 md:h-7 drop-shadow-[0_0_10px_rgba(250,204,21,0.5)]" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
            LEADERBOARD
          </h2>
          <button @click="showLeaderboard = false" class="text-slate-500 hover:text-white bg-slate-800 hover:bg-slate-700 p-2 rounded-full transition-all">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <div class="bg-slate-950 rounded-xl p-4 md:p-6 border border-slate-800/50 min-h-[250px] md:min-h-[300px]">
          <div v-if="scoreStore.isLoadingLeaderboard" class="flex flex-col items-center justify-center h-full gap-4 pt-10">
            <svg class="w-10 h-10 text-yellow-500 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            <p class="text-slate-400 font-mono text-xs md:text-sm animate-pulse">Menghubungkan ke satelit...</p>
          </div>

          <div v-else-if="scoreStore.leaderboardData.length === 0" class="flex flex-col items-center justify-center h-full gap-3 pt-10 opacity-60">
            <svg class="w-12 h-12 md:w-16 md:h-16 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
            <p class="text-slate-400 font-mono text-xs md:text-sm text-center">Belum ada komandan yang menaklukkan sektor ini.</p>
          </div>

          <div v-else class="space-y-3 max-h-[250px] md:max-h-[300px] overflow-y-auto pr-2">
            <div v-for="(item, index) in scoreStore.leaderboardData" :key="item.id"
                 class="flex justify-between items-center bg-slate-900/80 p-3 rounded-xl border border-slate-800">
              <div class="flex items-center gap-3 md:gap-4">
                <div class="font-black text-lg md:text-xl w-5 md:w-6 text-center drop-shadow-md"
                     :class="index === 0 ? 'text-yellow-400' : index === 1 ? 'text-slate-300' : index === 2 ? 'text-amber-600' : 'text-slate-600'">
                  {{ index + 1 }}
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-5 h-5 md:w-6 md:h-6 rounded-full bg-gradient-to-tr from-slate-700 to-slate-600 flex items-center justify-center text-[9px] md:text-[10px] font-bold text-white">
                    {{ item.profiles?.nama_lengkap ? item.profiles.nama_lengkap.charAt(0).toUpperCase() : '?' }}
                  </div>
                  <span class="font-bold text-slate-200 text-xs md:text-sm tracking-wide truncate max-w-[100px] md:max-w-none">{{ item.profiles?.nama_lengkap || 'Kadet Angkasa' }}</span>
                </div>
              </div>
              <div class="font-mono text-emerald-400 font-black text-base md:text-lg drop-shadow-[0_0_5px_rgba(52,211,153,0.4)]">
                {{ item.score.toString().padStart(5, '0') }}
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.stars {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 200%;
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
  animation: moveStars 60s linear infinite;
  opacity: 0.3;
}

.stars-medium {
  background-image:
      radial-gradient(2px 2px at 100px 150px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(2px 2px at 60px 50px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(2px 2px at 180px 80px, #ffffff, rgba(0,0,0,0));
  background-repeat: repeat;
  background-size: 300px 300px;
  animation: moveStars 40s linear infinite;
  opacity: 0.6;
}

.stars-large {
  background-image:
      radial-gradient(3px 3px at 50px 200px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(3px 3px at 200px 60px, #ffffff, rgba(0,0,0,0));
  background-repeat: repeat;
  background-size: 400px 400px;
  animation: moveStars 20s linear infinite;
  opacity: 0.9;
}

@keyframes moveStars {
  from { transform: translateY(0); }
  to { transform: translateY(-50%); }
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}
.animate-float-1 { animation: float 12s ease-in-out infinite; }
.animate-float-2 { animation: float 15s ease-in-out infinite reverse; }
</style>