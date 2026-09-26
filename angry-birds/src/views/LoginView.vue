<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import Swal from 'sweetalert2'

const router = useRouter()
const authStore = useAuthStore()

const isLogin = ref(true)
const form = ref({
  email: '',
  password: '',
  username: '',
  nama_lengkap: ''
})

const handleAuth = async () => {
  authStore.errorMessage = ''

  if (!form.value.email || !form.value.password) {
    authStore.errorMessage = 'Transmisi gagal: Email dan Password wajib diisi!'
    return
  }

  if (!isLogin.value && (!form.value.nama_lengkap || !form.value.username)) {
    authStore.errorMessage = 'Transmisi gagal: Identitas Kadet belum lengkap!'
    return
  }

  let result;
  if (isLogin.value) {
    result = await authStore.login(form.value.email, form.value.password)
  } else {
    result = await authStore.register(
        form.value.email,
        form.value.password,
        form.value.username,
        form.value.nama_lengkap
    )
  }

  if (result.success) {
    Swal.fire({
      title: isLogin.value ? 'Akses Diberikan!' : 'Registrasi Sukses!',
      text: isLogin.value ? 'Selamat datang kembali di AstroSling.' : 'Akun kadet angkasa Anda telah aktif.',
      icon: 'success',
      background: '#0f172a',
      color: '#f8fafc',
      confirmButtonColor: '#3b82f6',
      timer: 2000,
      showConfirmButton: false
    }).then(() => {
      router.push('/')
    })
  } else {
    Swal.fire({
      title: 'Akses Ditolak',
      text: authStore.errorMessage,
      icon: 'error',
      background: '#0f172a',
      color: '#f8fafc',
      confirmButtonColor: '#ef4444'
    })
  }
}
</script>

<template>
  <div class="min-h-[100dvh] flex items-center justify-center bg-slate-950 relative overflow-hidden px-4 py-8">

    <div class="stars stars-small"></div>
    <div class="stars stars-medium"></div>
    <div class="stars stars-large"></div>

    <div class="absolute top-[-10%] left-[-10%] w-72 h-72 md:w-96 md:h-96 bg-blue-600/20 rounded-full blur-[80px] md:blur-[100px] animate-float-1 pointer-events-none"></div>
    <div class="absolute bottom-[-10%] right-[-10%] w-72 h-72 md:w-96 md:h-96 bg-emerald-600/20 rounded-full blur-[80px] md:blur-[100px] animate-float-2 pointer-events-none"></div>

    <div
        v-motion
        :initial="{ opacity: 0, y: 50, scale: 0.95 }"
        :enter="{ opacity: 1, y: 0, scale: 1, transition: { type: 'spring', stiffness: 200, damping: 20, mass: 1 } }"
        class="relative z-10 w-full max-w-md p-6 md:p-8 bg-slate-900/60 backdrop-blur-xl border border-slate-700/50 rounded-3xl shadow-2xl"
    >
      <div
          v-motion
          :initial="{ opacity: 0, y: -20 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 200, duration: 600 } }"
          class="text-center mb-6 md:mb-8"
      >
        <h1 class="text-3xl md:text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 drop-shadow-sm">AstroSling</h1>
        <p class="text-slate-400 mt-1.5 md:mt-2 text-xs md:text-sm font-medium tracking-wide">Planetary Physics Simulator</p>
      </div>

      <transition name="fade">
        <div v-if="authStore.errorMessage" class="mb-4 p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-xs md:text-sm text-center">
          {{ authStore.errorMessage }}
        </div>
      </transition>

      <form @submit.prevent="handleAuth" class="space-y-4 md:space-y-5">
        <div v-if="!isLogin" class="space-y-4 md:space-y-5" v-motion :initial="{ opacity: 0, height: 0 }" :enter="{ opacity: 1, height: 'auto', transition: { duration: 300 } }">
          <div>
            <label class="block text-[10px] md:text-xs font-bold text-slate-400 uppercase tracking-widest mb-1.5">Nama Lengkap</label>
            <input v-model.trim="form.nama_lengkap" type="text" class="w-full px-4 py-3 text-sm md:text-base bg-slate-950/50 border border-slate-700 rounded-xl text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="Masukkan nama lengkap" />
          </div>
          <div>
            <label class="block text-[10px] md:text-xs font-bold text-slate-400 uppercase tracking-widest mb-1.5">Username</label>
            <input v-model.trim="form.username" type="text" class="w-full px-4 py-3 text-sm md:text-base bg-slate-950/50 border border-slate-700 rounded-xl text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="Masukkan Username" />
          </div>
        </div>

        <div v-motion :initial="{ opacity: 0, x: -30 }" :enter="{ opacity: 1, x: 0, transition: { delay: 300 } }">
          <label class="block text-[10px] md:text-xs font-bold text-slate-400 uppercase tracking-widest mb-1.5">Email</label>
          <input v-model.trim="form.email" type="email" class="w-full px-4 py-3 text-sm md:text-base bg-slate-950/50 border border-slate-700 rounded-xl text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="user@gmail.com" />
        </div>

        <div v-motion :initial="{ opacity: 0, x: 30 }" :enter="{ opacity: 1, x: 0, transition: { delay: 400 } }">
          <label class="block text-[10px] md:text-xs font-bold text-slate-400 uppercase tracking-widest mb-1.5">Password</label>
          <input v-model.trim="form.password" type="password" class="w-full px-4 py-3 text-sm md:text-base bg-slate-950/50 border border-slate-700 rounded-xl text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="••••••••" />
        </div>

        <div v-motion :initial="{ opacity: 0, y: 30 }" :enter="{ opacity: 1, y: 0, transition: { delay: 500, type: 'spring' } }">
          <button type="submit" :disabled="authStore.loading" class="w-full py-3.5 md:py-4 mt-2 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 disabled:opacity-50 text-white font-bold text-sm md:text-base rounded-xl shadow-[0_0_15px_rgba(59,130,246,0.5)] transform transition-all active:scale-95">
            {{ authStore.loading ? 'Memproses...' : (isLogin ? 'MASUK KE SISTEM' : 'DAFTARKAN AKUN') }}
          </button>
        </div>
      </form>

      <div
          v-motion
          :initial="{ opacity: 0 }"
          :enter="{ opacity: 1, transition: { delay: 600, duration: 800 } }"
          class="mt-6 md:mt-8 text-center text-xs md:text-sm text-slate-400"
      >
        {{ isLogin ? 'Kadet angkasa baru?' : 'Sudah terdaftar?' }}
        <button @click="isLogin = !isLogin; authStore.errorMessage = ''" type="button" class="text-blue-400 font-bold hover:text-blue-300 ml-1 transition-colors">
          {{ isLogin ? 'Registrasi di sini' : 'Login sekarang' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stars {
  position: absolute;
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

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-10px); }
</style>


