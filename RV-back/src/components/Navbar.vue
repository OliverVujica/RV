<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const mobileMenuOpen = ref(false)

const handleLogout = () => {
  authStore.logout()
  router.push('/')
  mobileMenuOpen.value = false
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}
</script>

<template>
  <nav class="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div class="flex items-center space-x-4">
          <router-link to="/" class="flex items-center space-x-2" @click="mobileMenuOpen = false">
            <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold">🌱</span>
            </div>
            <span class="text-xl font-bold text-gray-900 hidden sm:block">PlantDoctor</span>
            <span class="text-lg font-bold text-gray-900 sm:hidden">PD</span>
          </router-link>
        </div>

        <!-- Desktop Navigacija -->
        <div class="hidden md:flex items-center space-x-4">
          <router-link 
            to="/" 
            class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors duration-200"
          >
            Početna
          </router-link>

          <template v-if="!authStore.isAuthenticated">
            <router-link 
              to="/login" 
              class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors duration-200"
            >
              Prijava
            </router-link>
            <router-link 
              to="/register" 
              class="btn-primary text-sm"
            >
              Registracija
            </router-link>
          </template>

          <template v-else>
            <router-link 
              to="/dashboard" 
              class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors duration-200"
            >
              Dashboard
            </router-link>
            <div class="flex items-center space-x-3">
              <span class="text-sm text-gray-600 hidden lg:block">{{ authStore.user?.name }}</span>
              <button 
                @click="handleLogout"
                class="text-gray-500 hover:text-red-600 text-sm font-medium transition-colors duration-200"
              >
                Odjava
              </button>
            </div>
          </template>
        </div>

        <!-- Za telefone -->
        <div class="md:hidden">
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            type="button"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-primary-600 hover:bg-gray-100 transition-colors duration-200"
            aria-controls="mobile-menu"
            :aria-expanded="mobileMenuOpen"
          >
            <span class="sr-only">Otvori glavni meni</span>

            <svg 
              :class="{ 'hidden': mobileMenuOpen, 'block': !mobileMenuOpen }"
              class="h-6 w-6" 
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>

            <svg 
              :class="{ 'block': mobileMenuOpen, 'hidden': !mobileMenuOpen }"
              class="h-6 w-6" 
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <div 
        :class="{ 'block': mobileMenuOpen, 'hidden': !mobileMenuOpen }"
        class="md:hidden border-t border-gray-200 bg-white"
        id="mobile-menu"
      >
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link 
            to="/" 
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-50 rounded-md transition-colors duration-200"
          >
            Početna
          </router-link>

          <template v-if="!authStore.isAuthenticated">
            <router-link 
              to="/login" 
              @click="mobileMenuOpen = false"
              class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-50 rounded-md transition-colors duration-200"
            >
              Prijava
            </router-link>
            <router-link 
              to="/register" 
              @click="mobileMenuOpen = false"
              class="block px-3 py-2 text-base font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-md transition-colors duration-200"
            >
              Registracija
            </router-link>
          </template>

          <template v-else>
            <router-link 
              to="/dashboard" 
              @click="mobileMenuOpen = false"
              class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-50 rounded-md transition-colors duration-200"
            >
              Dashboard
            </router-link>
            <div class="px-3 py-2">
              <div class="text-sm text-gray-600 mb-2">Dobrodošli, {{ authStore.user?.name }}</div>
              <button 
                @click="handleLogout"
                class="text-red-600 hover:text-red-700 text-sm font-medium transition-colors duration-200"
              >
                Odjava
              </button>
            </div>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>