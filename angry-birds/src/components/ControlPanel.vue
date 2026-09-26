<script setup>
import { computed } from 'vue';

const props = defineProps(['gravity', 'mass']);
defineEmits(['update:gravity', 'update:mass', 'reset']);

const gravityColor = computed(() => {
  if (props.gravity < 1.0) return 'text-sky-300 border-sky-300/30 bg-sky-500/5';
  if (props.gravity < 2.0) return 'text-sky-400 border-sky-400/50 bg-sky-500/10';
  return 'text-sky-500 border-sky-500 bg-sky-500/20';
});

const massColor = computed(() => {
  if (props.mass < 5) return 'text-emerald-300 border-emerald-300/30 bg-emerald-500/5';
  if (props.mass < 11) return 'text-emerald-400 border-emerald-400/50 bg-emerald-500/10';
  return 'text-emerald-500 border-emerald-500 bg-emerald-500/20';
});
</script>

<template>
  <div class="relative overflow-hidden rounded-3xl border border-white/10 bg-slate-900/70 backdrop-blur-xl shadow-2xl p-6 flex flex-col gap-8 select-none">
    <div class="absolute top-0 right-0 w-40 h-40 bg-sky-500/10 blur-3xl rounded-full"></div>
    <div class="absolute bottom-0 left-0 w-40 h-40 bg-emerald-500/10 blur-3xl rounded-full"></div>

    <div class="relative z-10 border-b border-white/10 pb-4 text-left">
      <h2 class="text-2xl font-black tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-emerald-400">
        Panel Kontrol
      </h2>
      <p class="text-[10px] text-slate-500 font-mono mt-1 tracking-[0.2em] uppercase">Pengaturan Lingkungan</p>
    </div>

    <!-- Gravitasi -->
    <div class="relative z-10 flex flex-col gap-4">
      <div class="flex justify-between items-center text-left">
        <div>
          <h3 class="text-sm font-bold uppercase tracking-wider text-slate-200">Gravitasi</h3>
          <p class="text-[11px] text-slate-500 italic">Percepatan gravitasi ($g$)</p>
        </div>
        <div :class="['px-4 py-1.5 rounded-xl border transition-all duration-300 font-mono font-bold shadow-lg', gravityColor]">
          {{ gravity.toFixed(1) }} <span class="text-[10px] opacity-70">m/s²</span>
        </div>
      </div>
      <input type="range" min="0" max="3" step="0.1" :value="gravity"
             @input="$emit('update:gravity', parseFloat($event.target.value))"
             class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-sky-500" />
      <div class="flex justify-between text-[9px] font-bold text-slate-500 px-1 uppercase tracking-tighter text-left">
        <span>Tanpa Bobot</span>
        <span>Bumi</span>
        <span>Gravitasi Tinggi</span>
      </div>
    </div>

    <!-- Massa -->
    <div class="relative z-10 flex flex-col gap-4">
      <div class="flex justify-between items-center text-left">
        <div>
          <h3 class="text-sm font-bold uppercase tracking-wider text-slate-200">Massa Objek</h3>
          <p class="text-[11px] text-slate-500 italic">Massa proyektil ($m$)</p>
        </div>
        <div :class="['px-4 py-1.5 rounded-xl border transition-all duration-300 font-mono font-bold shadow-lg', massColor]">
          {{ mass }} <span class="text-[10px] opacity-70">kg</span>
        </div>
      </div>
      <input type="range" min="1" max="15" step="1" :value="mass"
             @input="$emit('update:mass', parseInt($event.target.value))"
             class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500" />
      <div class="flex justify-between text-[9px] font-bold text-slate-500 px-1 uppercase tracking-tighter text-left">
        <span>Ringan</span>
        <span>Standar</span>
        <span>Berat</span>
      </div>
    </div>

    <!-- Teori Fisika -->
    <div class="relative z-10 rounded-2xl border border-white/5 bg-black/40 p-4 shadow-inner">
      <h4 class="text-[10px] uppercase tracking-[0.3em] text-slate-500 mb-4 text-left font-bold border-l-2 border-sky-500 pl-2">Teori Fisika</h4>
      <div class="space-y-3 text-sm">
        <div class="flex justify-between items-center text-left">
          <span class="text-slate-400 text-xs">Momentum ($p$)</span>
          <span class="font-mono text-sky-400 text-xs bg-sky-500/10 px-2 py-0.5 rounded">p = mv</span>
        </div>
        <div class="flex justify-between items-center text-left">
          <span class="text-slate-400 text-xs">Energi Kinetik ($E_k$)</span>
          <span class="font-mono text-emerald-400 text-xs bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20 text-left">Ek = ½mv²</span>
        </div>
      </div>
    </div>

    <button @click="$emit('reset')"
            class="relative z-10 py-4 font-black rounded-2xl border border-red-500/30 bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-all uppercase tracking-widest text-xs">
      Atur Ulang Mesin
    </button>
  </div>
</template>