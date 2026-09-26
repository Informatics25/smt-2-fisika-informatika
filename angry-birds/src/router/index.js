import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import MenuView from '../views/MenuView.vue'
import GameView from '../views/GameView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/login', name: 'login', component: LoginView },
        { path: '/', name: 'menu', component: MenuView },
        { path: '/game', name: 'game', component: GameView }
    ]
})

router.beforeEach((to, from, next) => {
    const isLogged = localStorage.getItem('nama_lengkap')

    if (to.name !== 'login' && !isLogged) {
        next({ name: 'login' })
    } else if (to.name === 'login' && isLogged) {
        next({ name: 'menu' })
    } else {
        next()
    }
})

export default router