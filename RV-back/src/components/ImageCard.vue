<script setup lang="ts">
import { computed } from 'vue'
import type { PredictionResult } from '../services/api'

interface Props {
  prediction: PredictionResult
}

const props = defineProps<Props>()

// Funkcija za formatiranje naziva bolesti
const formattedDisease = computed(() => {
  if (!props.prediction.disease) return ''
  
  let formatted = props.prediction.disease.replace(/___/g, ': ');
  
  formatted = formatted.replace(/_/g, ' ');
  formatted = formatted.replace(/\(maize\)/g, '(Kukuruz)');
  formatted = formatted.replace(/\(including sour\)/g, '(Višnja/Trešnja)');

  return formatted;
});

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('hr-HR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="card">
    <div class="aspect-w-16 aspect-h-12 bg-gray-100">
      <img
        :src="prediction.image_url"
        :alt="`Slika - ${prediction.disease}`"
        class="w-full h-40 sm:h-48 object-cover"
        loading="lazy"
      />
    </div>
    
    <div class="p-3 sm:p-4 space-y-2 sm:space-y-3">
      <div>
        <h3 class="text-sm sm:text-lg font-semibold text-gray-900 mb-1 leading-tight">
          {{ formattedDisease }}
        </h3>
        <p class="text-xs sm:text-sm text-gray-600">
          {{ formatDate(prediction.created_at) }}
        </p>
      </div>
    </div>
  </div>
</template>