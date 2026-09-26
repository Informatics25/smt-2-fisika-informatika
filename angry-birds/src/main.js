import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import { MotionPlugin } from '@vueuse/motion'

const pinia = createPinia()
const app = createApp(App)

app.use(MotionPlugin)
app.use(pinia)
app.use(router)
app.mount('#app')