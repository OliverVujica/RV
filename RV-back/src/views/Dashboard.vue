<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import FileUpload from '../components/FileUpload.vue'
import ImageCard from '../components/ImageCard.vue'
import { predictionService, type PredictionResult } from '../services/api'

const authStore = useAuthStore()

const loading = ref(false)
const loadingHistory = ref(false)
const predictions = ref<PredictionResult[]>([])
const error = ref<string | null>(null)
const uploadResult = ref<PredictionResult | null>(null)
const selectedFile = ref<File | null>(null)
const showPlantList = ref(false)

const handleFileSelected = (files: FileList) => {
  if (files.length > 0) {
    selectedFile.value = files[0]
    uploadResult.value = null
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
  uploadResult.value = null

  try {
    const prediction = await predictionService.uploadImage(file, false)
    uploadResult.value = prediction
    predictions.value.unshift(prediction)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Greška pri analizi slike'
  } finally {
    loading.value = false
  }
}

const loadHistory = async () => {
  loadingHistory.value = true
  try {
    predictions.value = await predictionService.getHistory()
  } catch (err: any) {
    console.error('Error loading history:', err)
  } finally {
    loadingHistory.value = false
  }
}

const handleDeletePrediction = async (id: string) => {
  if (window.confirm('Jeste li sigurni da želite obrisati ovu analizu?')) {
    try {
      await predictionService.deletePrediction(id)
      predictions.value = predictions.value.filter(p => p._id !== id)
      if (uploadResult.value && uploadResult.value._id === id) {
        uploadResult.value = null
      }
    } catch (err) {
      alert('Greška pri brisanju analize. Pokušajte ponovno.')
      console.error('Error deleting prediction:', err)
    }
  }
}

onMounted(() => {
  loadHistory()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
      <div class="mb-6 sm:mb-8">
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="text-gray-600 mt-2 text-sm sm:text-base">
          Dobro došli, {{ authStore.user?.name }}! Analizirajte vaše biljke i pratite povijest.
        </p>
      </div>

      <div class="card p-6 mb-8">
        <div class="flex items-center justify-between cursor-pointer" @click="showPlantList = !showPlantList">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Podržane biljke i bolesti</h2>
            <p class="text-sm text-gray-600">Model prepoznaje 14 vrsta biljaka i njihove bolesti</p>
          </div>
          <div class="transition-transform duration-200" :class="{ 'rotate-180': showPlantList }">
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>
        </div>
        
        <div v-if="showPlantList" class="mt-6 transition-all duration-300">
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🍎 Jabuka (Apple)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Krastavost jabuke (Apple Scab)</li>
                <li>• Crna trulež (Black Rot)</li>
                <li>• Hrđa cedrovine i jabuke (Cedar Apple Rust)</li>
                <li>• Zdrav list</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🫐 Borovnica (Blueberry)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Zdrav list</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🍒 Trešnja / Višnja (Cherry)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Pepelnica (Powdery Mildew)</li>
                <li>• Zdrav list</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🌽 Kukuruz (Corn)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Siva pjegavost lista (Cercospora Leaf Spot)</li>
                <li>• Obična hrđa (Common Rust)</li>
                <li>• Sjeverna pjegavost lista (Northern Leaf Blight)</li>
                <li>• Zdrav list</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🍇 Vinova Loza (Grape)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Crna trulež (Black Rot)</li>
                <li>• Eskorioza (Esca / Black Measles)</li>
                <li>• Pjegavost lista (Leaf Blight)</li>
                <li>• Zdrav list</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🍊 Naranča (Orange)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Zelenilo citrusa (Citrus Greening)</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🍑 Breskva (Peach)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Bakterijska pjegavost (Bacterial Spot)</li>
                <li>• Zdrav list</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🌶️ Paprika (Pepper)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Bakterijska pjegavost (Bacterial Spot)</li>
                <li>• Zdrav list</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🥔 Krumpir (Potato)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Rana pjegavost (Early Blight)</li>
                <li>• Kasna pjegavost (Late Blight)</li>
                <li>• Zdrav list</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🍇 Malina (Raspberry)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Zdrav list</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🌱 Soja (Soybean)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Zdrav list</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🎃 Tikva (Squash)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Pepelnica (Powdery Mildew)</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🍓 Jagoda (Strawberry)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Pjegavost lista (Leaf Scorch)</li>
                <li>• Zdrav list</li>
              </ul>
            </div>

            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="font-semibold text-green-700 mb-2">🍅 Rajčica (Tomato)</h3>
              <ul class="text-sm text-gray-600 space-y-1">
                <li>• Bakterijska pjegavost (Bacterial Spot)</li>
                <li>• Rana pjegavost (Early Blight)</li>
                <li>• Kasna pjegavost (Late Blight)</li>
                <li>• Plijesan lista (Leaf Mold)</li>
                <li>• Siva pjegavost lista (Septoria Leaf Spot)</li>
                <li>• Paučinar (Spider Mites)</li>
                <li>• Ciljana pjegavost (Target Spot)</li>
                <li>• Virus žutog uvijanja lista (Yellow Leaf Curl Virus)</li>
                <li>• Virus mozaika rajčice (Mosaic Virus)</li>
                <li>• Zdrav list</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div class="grid lg:grid-cols-2 gap-8 mb-12">
        <div class="card p-8">
          <h2 class="text-xl font-semibold text-gray-900 mb-6">
            Nova analiza
          </h2>
          
          <FileUpload 
            :loading="loading"
            @file-selected="handleFileSelected"
          />

          <div v-if="selectedFile" class="mt-6">
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

        <div v-if="uploadResult" class="card p-8">
          <h2 class="text-xl font-semibold text-gray-900 mb-6">
            Najnoviji rezultat
          </h2>
          <ImageCard :prediction="uploadResult" />
        </div>
      </div>

      <div class="card p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold text-gray-900">
            Povijest analiza
          </h2>
          <button 
            @click="loadHistory"
            :disabled="loadingHistory"
            class="btn-secondary text-sm disabled:opacity-50"
          >
            <span v-if="loadingHistory">Učitavanje...</span>
            <span v-else>Osvježi</span>
          </button>
        </div>

        <div v-if="loadingHistory" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>

        <div v-else-if="predictions.length === 0" class="text-center py-8">
          <div class="text-gray-400 text-4xl mb-4">📱</div>
          <p class="text-gray-500">Još nemate analiziranih slika</p>
        </div>

        <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div 
            v-for="prediction in predictions" 
            :key="prediction._id"
            class="relative"
          >
            <ImageCard :prediction="prediction" />
            <button 
              @click="handleDeletePrediction(prediction._id)"
              class="absolute top-2 right-2 bg-white rounded-full p-2 text-red-500 hover:text-red-700 transition-colors duration-200"
              title="Obriši analizu"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm4 0a1 1 0 112 0v6a1 1 0 11-2 0V8z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>