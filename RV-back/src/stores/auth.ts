import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '../services/api'

interface User {
  id: string
  email: string
  name: string
}

interface LoginCredentials {
  email: string
  password: string
}

interface RegisterCredentials {
  username: string
  email: string
  password: string
  password_confirmation: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (credentials: LoginCredentials) => {
    loading.value = true
    try {
      // Backend očekuje 'application/x-www-form-urlencoded' za /token
      const params = new URLSearchParams()
      params.append('username', credentials.email)
      params.append('password', credentials.password)
      
      const response = await apiService.post('/token', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      
      const { access_token, user: userData } = response.data

      token.value = access_token
      user.value = userData
      localStorage.setItem('token', access_token)
      
      return { success: true }
    } catch (error: any) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    } finally {
      loading.value = false
    }
  }

  const register = async (credentials: RegisterCredentials) => {
    loading.value = true
    try {
      const response = await apiService.post('/register', credentials)
      const { access_token, user: userData } = response.data

      token.value = access_token
      user.value = userData
      localStorage.setItem('token', access_token)
      
      return { success: true }
    } catch (error: any) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  const initializeAuth = async () => {
    if (!token.value) return

    try {
      const response = await apiService.get('/auth/me')
      user.value = response.data
    } catch (error) {
      logout()
    }
  }

  return {
    user,
    token,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    initializeAuth
  }
})