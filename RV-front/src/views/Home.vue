<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import FileUpload from '../components/FileUpload.vue'
import ImageCard from '../components/ImageCard.vue'
import { predictionService, type PredictionResult } from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const result = ref<PredictionResult | null>(null)
const error = ref<string | null>(null)
const localImageUrl = ref<string | null>(null)
const showPlantList = ref(false)

const selectedFile = ref<File | null>(null)

const handleFileSelected = (files: FileList) => {
  if (files.length > 0) {
    selectedFile.value = files[0]
    result.value = null
    error.value = null
  }
}

const startPrediction = async () => {
  if (!selectedFile.value) return

  const file = selectedFile.value
  if (file.size > 10 * 1024 * 1024) {
    error.value = 'Slika je prevelika. Maksimalna veličina je 10MB.'
    return
  }

  loading.value = true
  error.value = null
  result.value = null
  if (localImageUrl.value) {
    URL.revokeObjectURL(localImageUrl.value)
  }
  localImageUrl.value = URL.createObjectURL(file)

  try {
    const predictionData = await predictionService.uploadImage(file, true)
    result.value = {
      _id: new Date().toISOString(),
      disease: predictionData.disease,
      filename: predictionData.filename,
      image_url: localImageUrl.value,
      created_at: new Date().toISOString()
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Greška pri analizi slike'
  } finally {
    loading.value = false
  }
}

const navigateToAuth = (route: string) => {
  router.push(route)
}
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 sm:pt-20 pb-16">
      <div class="text-center mb-8 sm:mb-16">
        <h1 class="text-3xl sm:text-4xl md:text-6xl font-bold text-gray-900 mb-4 sm:mb-6 leading-tight">
          Prepoznavanje 
          <span class="text-primary-600">Bolesti Biljaka</span>
        </h1>
        <p class="text-base sm:text-lg md:text-xl text-gray-600 max-w-3xl mx-auto mb-6 sm:mb-8 px-2">
          Koristite naš napredni AI model za trenutno prepoznavanje bolesti na vašim biljkama. 
          Jednostavno priložite sliku i dobijte dijagnozu u nekoliko sekundi.
        </p>
        
        <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center px-4">
          <template v-if="!authStore.isAuthenticated">
            <button @click="navigateToAuth('/register')" class="btn-primary w-full sm:w-auto">
              Registrirajte se besplatno
            </button>
            <button @click="navigateToAuth('/login')" class="btn-secondary w-full sm:w-auto">
              Prijavite se
            </button>
          </template>
          <template v-else>
            <button @click="router.push('/dashboard')" class="btn-primary w-full sm:w-auto">
              Idite na Dashboard
            </button>
          </template>
        </div>
      </div>

      <div class="max-w-2xl mx-auto px-4">
        <div class="bg-white rounded-2xl shadow-xl p-4 sm:p-8 mb-8">
          <h2 class="text-xl sm:text-2xl font-bold text-gray-900 mb-4 sm:mb-6 text-center">
            Probajte besplatno
          </h2>
          
          <FileUpload 
            :loading="loading"
            @file-selected="handleFileSelected"
          />

          <div v-if="selectedFile && !result" class="mt-6 text-center">
            <button 
              @click="startPrediction" 
              class="btn-primary w-full"
              :disabled="loading"
            >
              <span v-if="loading">Analiziram...</span>
              <span v-else>Analiziraj sliku</span>
            </button>
          </div>

          <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-700 text-sm">{{ error }}</p>
          </div>
        </div>

        <div v-if="result" class="max-w-md mx-auto">
          <h3 class="text-lg sm:text-xl font-semibold text-gray-900 mb-4 text-center">
            Rezultat analize
          </h3>
          <ImageCard :prediction="result" />
          
          <div class="mt-6 text-center px-4">
            <p class="text-gray-600 mb-4 text-sm sm:text-base">
              Želite sačuvati rezultate? Registrirajte se za potpunu funkcionalnost!
            </p>
            <button @click="navigateToAuth('/register')" class="btn-primary w-full sm:w-auto">
              Registracija
            </button>
          </div>
        </div>
      </div>

      <div class="max-w-4xl mx-auto mt-12 sm:mt-16 px-4">
        <div class="text-center mb-6 sm:mb-8">
          <div class="inline-flex items-center justify-center cursor-pointer hover:bg-gray-50 rounded-lg px-4 py-3 transition-colors duration-200 w-full sm:w-auto" @click="showPlantList = !showPlantList">
            <div class="text-center flex-1 sm:flex-none">
              <h3 class="text-base sm:text-lg font-medium text-gray-700 mb-1">Koje biljke podržavamo?</h3>
              <p class="text-xs sm:text-sm text-gray-500">Kliknite da vidite punu listu od 14 vrsta biljaka</p>
            </div>
            <div class="ml-3 transition-transform duration-200 flex-shrink-0" :class="{ 'rotate-180': showPlantList }">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </div>
          </div>
        </div>
        
        <div v-if="showPlantList" class="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-4 sm:p-6 transition-all duration-500 ease-in-out">
          <div class="grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 sm:gap-4">

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🍎</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Jabuka</h4>
              <p class="text-xs text-gray-500">4 stanja</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🫐</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Borovnica</h4>
              <p class="text-xs text-gray-500">1 stanje</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🍒</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Trešnja</h4>
              <p class="text-xs text-gray-500">2 stanja</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🌽</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Kukuruz</h4>
              <p class="text-xs text-gray-500">4 stanja</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🍇</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Grožđe</h4>
              <p class="text-xs text-gray-500">4 stanja</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🍊</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Naranča</h4>
              <p class="text-xs text-gray-500">1 stanje</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🍑</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Breskva</h4>
              <p class="text-xs text-gray-500">2 stanja</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🌶️</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Paprika</h4>
              <p class="text-xs text-gray-500">2 stanja</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🥔</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Krumpir</h4>
              <p class="text-xs text-gray-500">3 stanja</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🍇</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Malina</h4>
              <p class="text-xs text-gray-500">1 stanje</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🌱</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Soja</h4>
              <p class="text-xs text-gray-500">1 stanje</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🎃</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Tikva</h4>
              <p class="text-xs text-gray-500">1 stanje</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🍓</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Jagoda</h4>
              <p class="text-xs text-gray-500">2 stanja</p>
            </div>

            <div class="text-center p-3 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="text-2xl mb-1">🍅</div>
              <h4 class="font-medium text-gray-800 text-sm mb-1">Rajčica</h4>
              <p class="text-xs text-gray-500">10 stanja</p>
            </div>
          </div>
          
          <div class="mt-4 sm:mt-6 text-center">
            <p class="text-xs sm:text-sm text-gray-500">
              Svaka biljka može biti zdrava ili imati specifične bolesti koje naš AI model prepoznaje
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>