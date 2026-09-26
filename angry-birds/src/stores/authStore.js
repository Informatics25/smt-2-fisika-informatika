import { defineStore } from 'pinia'
import { supabase } from '../composables/useSupabase'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        session: null,
        namaLengkap: localStorage.getItem('nama_lengkap') || '',
        loading: false,
        errorMessage: ''
    }),

    actions: {
        async initialize() {
            const { data: { session } } = await supabase.auth.getSession()
            this.session = session
            this.user = session?.user || null

            if (this.user?.user_metadata?.nama_lengkap) {
                this.namaLengkap = this.user.user_metadata.nama_lengkap
                localStorage.setItem('nama_lengkap', this.namaLengkap)
            }
        },

        async register(email, password, username, nama_lengkap) {
            this.loading = true
            this.errorMessage = ''
            try {
                const { data, error } = await supabase.auth.signUp({
                    email,
                    password,
                    options: {
                        data: { username, nama_lengkap } // Mengamankan metadata sejak awal
                    }
                })
                if (error) throw error
                return { success: true }
            } catch (error) {
                this.errorMessage = error.message
                return { success: false }
            } finally {
                this.loading = false
            }
        },

        async login(email, password) {
            this.loading = true
            this.errorMessage = ''
            try {
                const { data, error } = await supabase.auth.signInWithPassword({
                    email,
                    password
                })
                if (error) throw error

                this.session = data.session
                this.user = data.user

                if (this.user?.user_metadata?.nama_lengkap) {
                    this.namaLengkap = this.user.user_metadata.nama_lengkap
                    localStorage.setItem('nama_lengkap', this.namaLengkap)
                }
                return { success: true }
            } catch (error) {
                this.errorMessage = error.message
                return { success: false }
            } finally {
                this.loading = false
            }
        },

        async logout() {
            await supabase.auth.signOut()
            this.user = null
            this.session = null
            this.namaLengkap = ''
            localStorage.removeItem('nama_lengkap')
        }
    }
})

