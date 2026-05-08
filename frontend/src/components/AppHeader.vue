<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" :to="isAuthenticated ? `/users/${authStore.user_id}` : '/'">
          VueJS with Flask
        </RouterLink>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
          aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">

            <!-- Register/Login -->
            <template v-if="!isAuthenticated">
              <!-- Home -->
              <li class="nav-item">
                <RouterLink class="nav-link" to="/">Home</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/register">Register</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/login">Login</RouterLink>
              </li>
            </template>

            <!-- Authenticated Navigation -->
            <template v-else>
              <li class="nav-item">
                <RouterLink class="nav-link" :to="`/users/${authStore.user_id}`">Browse</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/profiles/new">Add Profile</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/profiles/edit">Edit Profile</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/profiles/favourites">Favourites</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/messages">Messages</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/store/authentication'
import { computed } from 'vue'

const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<style scoped>
.navbar-nav .nav-link.active {
  font-weight: bold;
}
</style>
