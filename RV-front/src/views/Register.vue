<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const error = ref<string | null>(null)

const handleSubmit = async () => {
  error.value = null

  if (!form.username || !form.email || !form.password) {
    error.value = 'Molim popunite sva polja'
    return
  }

  if (form.password !== form.confirmPassword) {
    error.value = 'Lozinke se ne slažu'
    return
  }

  if (form.password.length < 8) {
    error.value = 'Lozinka mora imati najmanje 8 karaktera'
    return
  }

  const result = await authStore.register({
    username: form.username,
    email: form.email,
    password: form.password,
    password_confirmation: form.confirmPassword
  })
  
  if (result.success) {
    router.push('/dashboard')
  } else {
    error.value = result.error
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
       <div class="flex justify-center">
        <div class="w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center">
          <span class="text-white font-bold text-xl">🌱</span>
        </div>
      </div>
      <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">
        Registrirajte se
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Ili
        <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-500">
          prijavite se s postojećim računom
        </router-link>
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="card p-8">
        <form class="space-y-6" @submit.prevent="handleSubmit">
          <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-700 text-sm">{{ error }}</p>
          </div>

          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Korisničko ime
            </label>
            <div class="mt-1">
              <input
                id="username"
                v-model="form.username"
                name="username"
                type="text"
                autocomplete="username"
                required
                class="input-field"
                placeholder="korisnik123"
              />
            </div>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Email adresa
            </label>
            <div class="mt-1">
              <input
                id="email"
                v-model="form.email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="input-field"
                placeholder="vas@email.com"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Lozinka
            </label>
            <div class="mt-1">
              <input
                id="password"
                v-model="form.password"
                name="password"
                type="password"
                autocomplete="new-password"
                required
                class="input-field"
                placeholder="••••••••"
              />
            </div>
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">
              Potvrdite lozinku
            </label>
            <div class="mt-1">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                name="confirmPassword"
                type="password"
                autocomplete="new-password"
                required
                class="input-field"
                placeholder="••••••••"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="authStore.loading"
              class="w-full btn-primary disabled:opacity-50"
            >
              <span v-if="authStore.loading">Registracija...</span>
              <span v-else>Registrirajte se</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>