import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'

export function checkTokenExpiration() {
    const token = localStorage.getItem('jwt');
    if (token) {
        try {
            const decoded = jwtDecode(token);
            const now = Date.now() / 1000;
            if (decoded.exp < now) {
                localStorage.removeItem('jwt');
                return false;
            }
            return true;
        } catch (e) {
            localStorage.removeItem('jwt');
            return false;
        }
    }
    return false;
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user_id: null,  // Store user_id separately
    user: null,     // Store user object separately
    token: null,    // Store token separately
  }),
  actions: {
    initialize() {
      const token = localStorage.getItem('jwt')
      const user = JSON.parse(localStorage.getItem('user'))
      const userId = localStorage.getItem('user_id')

      if (token && userId && checkTokenExpiration()) {
        this.isAuthenticated = true
        this.token = token
        this.user = user
        this.user_id = userId
      }
      else {
        this.logout()
      }
    },
    login(token, user, userId) {
      this.isAuthenticated = true
      this.token = token
      this.user = user
      this.user_id = userId
      localStorage.setItem('jwt', token)
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('user_id', userId)
    },
    logout() {
      this.isAuthenticated = false
      this.token = null
      this.user = null
      this.user_id = null
      localStorage.removeItem('jwt')
      localStorage.removeItem('user')
      localStorage.removeItem('user_id')
    }
  }
})