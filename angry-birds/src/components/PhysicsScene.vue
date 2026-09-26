<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import Matter from 'matter-js'

const props = defineProps({
  gravity: Number,
  mass: Number
})

const sceneRef = ref(null)
const trajectoryPoints = ref([])
const velocity = ref(0)
const momentum = ref(0)
const kineticEnergy = ref(0)

let engine, render, runner, bird, sling, mouseConstraint

const resetBird = () => {
  const { Body, Composite } = Matter
  if (!bird || !sling) return

  Body.setPosition(bird, { x: 200, y: 350 })
  Body.setVelocity(bird, { x: 0, y: 0 })
  Body.setAngularVelocity(bird, 0)

  sling.bodyB = bird
  sling.render.visible = true
}

onMounted(() => {
  const { Engine, Render, Runner, Bodies, Composite, MouseConstraint, Mouse, Constraint, Vector, Body } = Matter

  engine = Engine.create()
  engine.world.gravity.y = props.gravity

  render = Render.create({
    element: sceneRef.value,
    engine: engine,
    options: {
      width: 1000,
      height: 550,
      wireframes: false,
      background: 'transparent',
    }
  })

  const ground = Bodies.rectangle(500, 530, 1200, 60, {
    isStatic: true,
    render: { fillStyle: '#14532d' }
  })

  const stack = []
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 5; j++) {
      stack.push(Bodies.rectangle(750 + i * 45, 450 - j * 45, 40, 40, {
        restitution: 0.3,
        render: { fillStyle: '#b45309', strokeStyle: '#78350f', lineWidth: 2 }
      }))
    }
  }

  bird = Bodies.circle(200, 350, 22, {
    mass: props.mass,
    restitution: 0.6,
    frictionAir: 0.01,
    render: { fillStyle: '#ef4444', strokeStyle: '#7f1d1d', lineWidth: 4 }
  })

  const slingAnchor = { x: 200, y: 350 }
  sling = Constraint.create({
    pointA: slingAnchor,
    bodyB: bird,
    stiffness: 0.05,
    length: 0.5,
    render: { strokeStyle: '#3f1d0d', lineWidth: 6 }
  })

  const mouse = Mouse.create(render.canvas)
  mouseConstraint = MouseConstraint.create(engine, {
    mouse: mouse,
    constraint: { stiffness: 0.1, render: { visible: false } }
  })

  let lastLogTime = 0; // Tambahkan variabel ini di luar onMounted atau di bagian atas script

// Di dalam Matter.Events.on(engine, 'afterUpdate', ...
  Matter.Events.on(engine, 'afterUpdate', () => {
    const speed = bird.speed;
    const currentTime = Date.now();

    // Update variabel HUD tetap real-time
    velocity.value = speed;
    momentum.value = props.mass * speed;
    kineticEnergy.value = 0.5 * props.mass * Math.pow(speed, 2);

    // LOG KONSOL HANYA SETIAP 200ms (Agar tidak buram/berkedip)
    if (currentTime - lastLogTime > 200) {
      if (speed > 0.1 || mouseConstraint.mouse.button !== -1) {
        console.clear();
        console.log("%c--- MONITORING FISIKA ---", "color: #00eaff; font-weight: bold;");
        console.table([
          { Parameter: "Gravitasi (g)", Nilai: props.gravity.toFixed(2), Satuan: "m/s²" },
          { Parameter: "Massa (m)", Nilai: props.mass, Satuan: "kg" },
          { Parameter: "Kecepatan (v)", Nilai: speed.toFixed(2), Satuan: "m/s" },
          { Parameter: "Momentum (p)", Nilai: momentum.value.toFixed(2), Satuan: "kg.m/s" },
          { Parameter: "Energi (Ek)", Nilai: kineticEnergy.value.toFixed(2), Satuan: "Joule" }
        ]);
        lastLogTime = currentTime; // Update waktu log terakhir
      }
    }
  });

  Matter.Events.on(mouseConstraint, 'enddrag', (e) => {
    if (e.body === bird) {
      setTimeout(() => {
        sling.bodyB = null
        sling.render.visible = false
      }, 20)
    }
  })

  Composite.add(engine.world, [ground, ...stack, bird, sling, mouseConstraint])
  Render.run(render)
  runner = Runner.create()
  Runner.run(runner, engine)
})

watch(() => props.gravity, (val) => { if (engine) engine.world.gravity.y = val })
watch(() => props.mass, (val) => { if (bird) Matter.Body.setMass(bird, val) })

onBeforeUnmount(() => {
  Matter.Render.stop(render); Matter.Runner.stop(runner); Matter.Engine.clear(engine);
  if (render.canvas) render.canvas.remove()
})
</script>

<template>
  <div class="relative w-full h-full min-h-[550px] overflow-hidden select-none">
    <div class="absolute inset-0 bg-gradient-to-b from-sky-400 via-sky-200 to-emerald-50"></div>

    <div class="absolute top-6 left-6 z-20 flex flex-col gap-2 font-mono text-[10px] text-white">
      <div class="bg-black/40 backdrop-blur-md p-3 rounded-lg border border-white/10 shadow-xl space-y-1 text-left">
        <p class="font-bold border-b border-white/10 pb-1 mb-1 text-sky-300">Data Telemetry</p>
        <p class="flex justify-between gap-4"><span>Kecepatan</span> <span class="text-sky-400">{{ velocity.toFixed(2) }}</span></p>
        <p class="flex justify-between gap-4"><span>Momentum</span> <span class="text-emerald-400">{{ momentum.toFixed(2) }}</span></p>
        <p class="flex justify-between gap-4"><span>Energy</span> <span class="text-orange-400">{{ kineticEnergy.toFixed(2) }}</span></p>
      </div>
    </div>

    <div ref="sceneRef" class="relative z-10 w-full h-full">
      <svg class="absolute inset-0 pointer-events-none w-full h-full z-20">
        <circle v-for="(p, i) in trajectoryPoints" :key="i" :cx="p.x" :cy="p.y" :r="3.5" fill="rgba(255,255,255,0.7)" />
      </svg>
    </div>
  </div>
</template>