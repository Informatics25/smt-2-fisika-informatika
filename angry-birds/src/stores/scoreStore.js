import { defineStore } from 'pinia'
import { supabase } from "../composables/useSupabase.js"

export const useScoreStore = defineStore('score', {
    state: () => ({
        isSaving: false,
        isLoadingLeaderboard: false,
        leaderboardData: [],
        userHighScores: {}
    }),
    actions: {
        async submitScore(planetId, finalScore) {
            this.isSaving = true
            try {
                const { data: { user }, error: authError } = await supabase.auth.getUser()
                if (authError || !user) throw new Error('Akses ditolak. Pemain tidak terautentikasi.')

                const { error } = await supabase
                    .from('scores')
                    .insert([
                        {
                            user_id: user.id,
                            planet_id: planetId.toString(),
                            score: finalScore
                        }
                    ])

                if (error) throw error
                return { success: true }
            } catch (error) {
                console.error('Gagal mengirim skor:', error.message)
                return { success: false, message: error.message }
            } finally {
                this.isSaving = false
            }
        },

        async fetchLeaderboard(planetId) {
            this.isLoadingLeaderboard = true
            this.leaderboardData = []
            try {
                const { data, error } = await supabase
                    .from('scores')
                    .select(`
                        id,
                        score,
                        profiles ( nama_lengkap )
                    `)
                    .eq('planet_id', planetId.toString())
                    .order('score', { ascending: false })
                    .limit(10)

                if (error) throw error
                this.leaderboardData = data
            } catch (error) {
                console.error('Gagal memuat leaderboard:', error.message)
            } finally {
                this.isLoadingLeaderboard = false
            }
        },

        async fetchUserHighScores() {
            try {
                const { data: { user }, error: authError } = await supabase.auth.getUser()
                if (authError || !user) return

                const { data, error } = await supabase
                    .from('scores')
                    .select('planet_id, score')
                    .eq('user_id', user.id)

                if (error) throw error

                const highScores = {}
                data.forEach(item => {
                    const pid = item.planet_id
                    if (!highScores[pid] || item.score > highScores[pid].score) {
                        let stars = 0
                        if (item.score >= 6000) stars = 3
                        else if (item.score >= 4000) stars = 2
                        else if (item.score >= 1000) stars = 1

                        highScores[pid] = { score: item.score, stars: stars }
                    }
                })

                this.userHighScores = highScores
            } catch (error) {
                console.error('Gagal memuat high score user:', error.message)
            }
        }
    }
})