<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { computed, onMounted } from 'vue'
import { useAuthStore, checkTokenExpiration} from '@/store/authentication.js'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

const authStore = useAuthStore()
const router = useRouter()

const isAuthenticated = computed(() => authStore.isAuthenticated)

onMounted(() => {
  // Check if the user is authenticated and token is valid
  if (!authStore.isAuthenticated || !checkTokenExpiration()) {
    router.push('/')  // Redirect to login if not authenticated or token expired
  }
  else{
    router.push('/users/' + authStore.user_id)
  }
})
</script>

<template>
  <div class="app-container">
    <AppHeader :is-authenticated="isAuthenticated" />

    <main class="main-content">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>

    <AppFooter />
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 2rem 0;
  background-color: #f9f9f9;
}

/* Transition effects */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<style>
/* Global styles */
body {
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
  padding-top: 80px;
  /* Space for fixed header */
}

a {
  text-decoration: none;
  color: #42b983;
}

/* Responsive breakpoints */
@media (max-width: 768px) {
  body {
    padding-top: 60px;
  }
}
</style>