import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const apiService = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

apiService.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

apiService.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export interface PredictionResult {
  _id: string
  image_url: string
  disease: string
  filename: string
  created_at: string
}

export const predictionService = {
  uploadImage: async (imageFile: File, isAnonymous = false): Promise<any> => {
    const formData = new FormData()
    formData.append('file', imageFile)

    const endpoint = isAnonymous ? '/predict/anonymous' : '/predict'
    const response = await apiService.post(endpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return response.data
  },

  getHistory: async (): Promise<PredictionResult[]> => {
    const response = await apiService.get('/predictions/history')
    return response.data
  },

  deletePrediction: async (id: string): Promise<void> => {
    await apiService.delete(`/predictions/${id}`);
  }
}