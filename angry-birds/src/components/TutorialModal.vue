<script setup>
defineProps({
  show: Boolean
})
defineEmits(['close'])
</script>

<template>
  <div v-if="show" class="fixed inset-0 z-[60] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 overflow-y-auto pointer-events-auto">
    <div class="bg-slate-900 border-2 border-blue-500/50 p-5 md:p-8 rounded-2xl md:rounded-3xl shadow-[0_0_50px_rgba(59,130,246,0.3)] max-w-sm md:max-w-xl w-full transform transition-all scale-100 text-left relative overflow-hidden">

      <div class="absolute inset-0 opacity-10 pointer-events-none" style="background-image: linear-gradient(#3b82f6 1px, transparent 1px), linear-gradient(90deg, #3b82f6 1px, transparent 1px); background-size: 20px 20px;"></div>

      <div class="flex justify-between items-center mb-4 md:mb-6 border-b border-slate-800 pb-3 md:pb-4 relative z-10">
        <h2 class="text-xl sm:text-2xl md:text-3xl font-black text-blue-400 drop-shadow-lg tracking-widest">
          CARA BERMAIN
        </h2>
        <div class="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center text-blue-400 shadow-[0_0_15px_rgba(59,130,246,0.5)] animate-pulse">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
        </div>
      </div>

      <div class="space-y-4 md:space-y-5 mb-6 md:mb-8 relative z-10">

        <div class="flex items-center gap-3 md:gap-4 bg-slate-800/80 p-3 md:p-4 rounded-xl border border-slate-700 shadow-lg">
          <div class="w-16 h-16 shrink-0 bg-slate-950 rounded-lg flex items-center justify-center border border-slate-600 relative overflow-hidden">
            <div class="w-2 h-8 bg-slate-600 absolute bottom-2 left-4 rounded-sm"></div>
            <div class="w-3 h-3 bg-amber-700 rounded-full absolute ketapel-peluru"></div>
            <svg class="absolute inset-0 w-full h-full pointer-events-none ketapel-tali" viewBox="0 0 64 64"><path d="M 20 40 L 32 32" stroke="#94a3b8" stroke-width="2"/></svg>
          </div>
          <div>
            <h3 class="font-bold text-white text-sm md:text-base">Tarik & Lepas Ketapel</h3>
            <p class="text-[11px] md:text-xs text-slate-400 mt-0.5 leading-snug">Sentuh peluru di sisi kiri layar, tarik ke belakang untuk mengukur tenaga, lalu lepaskan.</p>
          </div>
        </div>

        <div class="flex items-center gap-3 md:gap-4 bg-slate-800/80 p-3 md:p-4 rounded-xl border border-slate-700 shadow-lg">
          <div class="w-16 h-16 shrink-0 bg-slate-950 rounded-lg flex items-center justify-center border border-slate-600 relative overflow-hidden">
            <div class="w-16 h-2 bg-slate-700 absolute bottom-2"></div>
            <div class="w-4 h-12 bg-amber-800 absolute bottom-4 right-4 animate-block-fall"></div>
            <div class="w-4 h-4 bg-red-500 rounded-full absolute bottom-4 right-8 animate-target-squash"></div>
          </div>
          <div>
            <h3 class="font-bold text-white text-sm md:text-base">Hancurkan Target</h3>
            <p class="text-[11px] md:text-xs text-slate-400 mt-0.5 leading-snug">Runtuhkan struktur bangunan agar menimpa target merah. Hancurkan semua target untuk menang!</p>
          </div>
        </div>

        <div class="flex items-center gap-3 md:gap-4 bg-slate-800/80 p-3 md:p-4 rounded-xl border border-slate-700 shadow-lg">
          <div class="w-16 h-16 shrink-0 bg-slate-950 rounded-lg flex flex-col items-center justify-center border border-slate-600 relative">
            <div class="flex gap-1">
              <div class="w-4 h-4 border border-slate-500 rounded bg-slate-800 flex items-center justify-center animate-btn-click">
                <div class="w-2 h-2 rounded-full bg-stone-500"></div>
              </div>
              <div class="w-4 h-4 border border-slate-500 rounded bg-slate-800 flex items-center justify-center">
                <div class="w-2 h-2 rounded-full bg-slate-400"></div>
              </div>
            </div>
            <svg class="w-4 h-4 text-white absolute bottom-4 right-4 animate-cursor-click drop-shadow-md" fill="currentColor" viewBox="0 0 24 24"><path d="M13.149 22.812l-2.028-6.195-5.385 5.586a.5.5 0 01-.84-.442l4.243-19.98a.5.5 0 01.942-.047l7.713 16.143a.5.5 0 01-.803.553l-4.526-3.79-1.844 5.632a.5.5 0 01-.948.16l-.524-1.62z"/></svg>
          </div>
          <div>
            <h3 class="font-bold text-white text-sm md:text-base">Ganti Amunisi</h3>
            <p class="text-[11px] md:text-xs text-slate-400 mt-0.5 leading-snug">Klik tombol amunisi. <b>Batu/Besi</b> menghancurkan beton, <b>Kayu</b> untuk kaca rapuh.</p>
          </div>
        </div>

      </div>

      <button @click="$emit('close')" class="relative z-10 w-full py-3 md:py-4 rounded-xl font-black text-xs sm:text-sm md:text-base text-white bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 shadow-[0_0_20px_rgba(59,130,246,0.4)] transform transition-all active:scale-95 tracking-widest uppercase border border-blue-400/50">
        SIAP, KOMANDAN!
      </button>
    </div>
  </div>
</template>

<style scoped>
.ketapel-peluru {
  animation: pull-release 3s infinite ease-in-out;
}
.ketapel-tali path {
  animation: stretch-string 3s infinite ease-in-out;
}

@keyframes pull-release {
  0%, 10% { transform: translate(20px, 20px); opacity: 1; }
  40%, 50% { transform: translate(5px, 35px); opacity: 1; }
  55% { transform: translate(50px, -10px); opacity: 0; }
  100% { transform: translate(20px, 20px); opacity: 0; }
}

@keyframes stretch-string {
  0%, 10% { d: path('M 20 40 L 26 26'); }
  40%, 50% { d: path('M 20 40 L 11 41'); }
  55% { d: path('M 20 40 L 30 20'); }
  100% { d: path('M 20 40 L 26 26'); }
}

.animate-block-fall {
  animation: block-fall 3s infinite ease-in;
  transform-origin: bottom right;
}
.animate-target-squash {
  animation: target-squash 3s infinite;
  transform-origin: bottom;
}

@keyframes block-fall {
  0%, 30% { transform: rotate(0deg); }
  40% { transform: rotate(-45deg); }
  50%, 100% { transform: rotate(-90deg) translate(-10px, 0); }
}

@keyframes target-squash {
  0%, 45% { transform: scaleY(1); opacity: 1; }
  50%, 80% { transform: scaleY(0.2) scaleX(1.5); opacity: 0.5; background-color: #7f1d1d; }
  100% { transform: scaleY(1); opacity: 1; }
}

.animate-cursor-click {
  animation: cursor-move 3s infinite ease-in-out;
}
.animate-btn-click {
  animation: btn-press 3s infinite ease-in-out;
}

@keyframes cursor-move {
  0%, 10% { transform: translate(10px, 10px); }
  30%, 50% { transform: translate(-18px, -15px); }
  60%, 100% { transform: translate(10px, 10px); }
}

@keyframes btn-press {
  0%, 35% { transform: scale(1); border-color: #64748b; }
  40%, 45% { transform: scale(0.85); border-color: #3b82f6; background-color: #1e293b; box-shadow: 0 0 10px rgba(59,130,246,0.5); }
  50%, 100% { transform: scale(1); border-color: #64748b; }
}
</style>