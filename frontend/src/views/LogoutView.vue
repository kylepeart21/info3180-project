<script setup>
import { useAuthStore } from '@/store/authentication.js';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '@/http.js';

const authStore = useAuthStore();
const router = useRouter();

onMounted(async () => {
    const token = localStorage.getItem('jwt');

    if (token) {
        try {
            const response = await apiClient.post('/api/auth/logout', {}, {
                headers: {
                  'Content-Type': 'application/json',
                  Authorization: `Bearer ${token}`,
                }
            });

            if (response.status !== 200) {
                console.warn('Backend logout failed');
            }
        } catch (error) {
            console.error("Logout error:", error);
        }
    }

    authStore.logout(); // Clear frontend state and localStorage
    await router.push('/'); // Redirect to login
});
</script>

<template>
  <div>Logging you out...</div>
</template>

<style scoped>
div {
  text-align: center;
  margin-top: 2rem;
}
</style>
