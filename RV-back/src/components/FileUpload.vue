<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  loading?: boolean
  accept?: string
  multiple?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  accept: 'image/*',
  multiple: false
})

const emit = defineEmits<{
  'file-selected': [files: FileList]
}>()

const dragOver = ref(false)
const fileInput = ref<HTMLInputElement>()
const selectedFiles = ref<FileList | null>(null)

const isDragActive = computed(() => dragOver.value)

const handleDragEnter = (e: DragEvent) => {
  e.preventDefault()
  dragOver.value = true
}

const handleDragLeave = (e: DragEvent) => {
  e.preventDefault()
  dragOver.value = false
}

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  dragOver.value = false
  
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    selectedFiles.value = files
    // Promjena: Emitira se 'file-selected'
    emit('file-selected', files)
  }
}

const handleFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  const files = target.files
  if (files && files.length > 0) {
    selectedFiles.value = files
    emit('file-selected', files)
  }
}

const openFileDialog = () => {
  fileInput.value?.click()
}
</script>

<template>
  <div class="w-full">
    <div
      :class="[
        'relative border-2 border-dashed rounded-lg p-4 sm:p-8 text-center transition-all duration-200',
        isDragActive ? 'border-primary-400 bg-primary-50' : 'border-gray-300 hover:border-primary-400',
        loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
      ]"
      @dragenter="handleDragEnter"
      @dragleave="handleDragLeave"
      @dragover="handleDragOver"
      @drop="handleDrop"
      @click="openFileDialog"
    >
      <input
        ref="fileInput"
        type="file"
        :accept="accept"
        :multiple="multiple"
        :disabled="loading"
        class="hidden"
        @change="handleFileSelect"
      />

      <div class="space-y-3 sm:space-y-4">
        <div class="flex justify-center">
          <div v-if="loading" class="animate-spin rounded-full h-8 w-8 sm:h-12 sm:w-12 border-b-2 border-primary-600"></div>
          <div v-else class="text-3xl sm:text-4xl">📷</div>
        </div>

        <div class="space-y-2">
          <p v-if="loading" class="text-sm text-gray-600">
            Analiziranje slike...
          </p>
          <template v-else-if="selectedFiles && selectedFiles.length > 0">
             <p class="text-base sm:text-lg font-medium text-gray-900">
              Slika je spremna za analizu
            </p>
            <p class="text-sm text-gray-600">
              Kliknite na gumb "Analiziraj sliku"
            </p>
          </template>
          <template v-else>
            <p class="text-base sm:text-lg font-medium text-gray-900">
              Priložite sliku biljke
            </p>
            <p class="text-sm text-gray-600 px-2">
              <span class="hidden sm:inline">Povucite i ispustite sliku ovdje ili </span>kliknite za odabir datoteke
            </p>
            <p class="text-xs text-gray-500">
              Podržani formati: JPG, PNG, WEBP (max 10MB)
            </p>
          </template>
        </div>

        <div v-if="selectedFiles && selectedFiles.length > 0 && !loading" class="text-sm text-primary-600 px-2 break-all">
          <span class="font-medium">Odabrana datoteka:</span> 
          <span class="block sm:inline">{{ selectedFiles[0].name }}</span>
        </div>
      </div>
    </div>
  </div>
</template>