import { defineStore } from 'pinia'
import { getCurrentUser as getCurrentUserHttp } from '@/http/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: {},
  }),
  actions: {
    async getCurrentUser() {
      const { data } = await getCurrentUserHttp()
      this.currentUser = data
    },
  },
})
