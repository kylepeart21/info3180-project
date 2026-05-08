<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/authentication.js'
import apiClient from '@/http.js';

const username = ref('');
const password = ref('');
const router = useRouter();
const authStore = useAuthStore();

// Handle login
const loginUser = async () => {
    try {
        const response = await apiClient.post('/api/auth/login', {
            username: username.value,
            password: password.value
        });

        const data = response.data;

        // Save tokens, update store
        authStore.login(data.access_token, data.user, data.user.id);

        // Redirect
        await router.push('/users/' + authStore.user_id);
    } catch (error) {
        if (error.response) {
            console.error("Login failed:", error.response.data);
            alert("Login failed. Please try again.");
        } else {
            console.error('Error:', error.message);
            alert("An error occurred during login.");
        }
    }
};

</script>

<template>
    <div class="container mt-4">
        <form id="loginForm" @submit.prevent="loginUser">
            <div class="form-group mb-3">
                <label for="username" class="form-label">Username</label>
                <input v-model="username" type="text" name="username" class="form-control" required />
            </div>

            <div class="form-group mb-3">
                <label for="password" class="form-label">Password</label>
                <input v-model="password" type="password" name="password" class="form-control" required />
            </div>

            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</template>



<style scoped>
.container {
    max-width: 600px;
    margin: auto;
}
</style>