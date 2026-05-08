<script setup>

import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/store/authentication.js'

import apiClient from '@/http.js'

const username = ref('')
const password = ref('')

const loading = ref(false)

const errorMessage = ref('')

const router = useRouter()

const authStore = useAuthStore()

/* =========================
   LOGIN
========================= */

const loginUser = async () => {

  try {

    loading.value = true

    errorMessage.value = ''

    const response = await apiClient.post(
      '/api/auth/login',
      {
        username: username.value,
        password: password.value
      }
    )

    const data = response.data

    authStore.login(
      data.access_token,
      data.user,
      data.user.id
    )

    await router.push(
      '/users/' + authStore.user_id
    )

  } catch (error) {

    if (error.response) {

      errorMessage.value =
        error.response.data?.error ||
        'Login failed. Please try again.'

    } else {

      errorMessage.value =
        'An unexpected error occurred.'
    }

  } finally {

    loading.value = false
  }
}

</script>

<template>

  <section class="login-page">

    <!-- GLOWS -->
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>

    <!-- CARD -->
    <div class="login-card">

      <!-- LOGO -->
      <div class="brand">

        <div class="brand-dot"></div>

        <span>JamDate</span>

      </div>

      <!-- TITLE -->
      <h1 class="title">
        Welcome Back
      </h1>

      <p class="subtitle">
        Continue building meaningful
        connections with real people.
      </p>

      <!-- ERROR -->
      <div
        v-if="errorMessage"
        class="error-box"
      >
        {{ errorMessage }}
      </div>

      <!-- FORM -->
      <form
        @submit.prevent="loginUser"
        class="login-form"
      >

        <!-- USERNAME -->
        <div class="form-group">

          <label>
            Username
          </label>

          <input
            v-model="username"
            type="text"
            placeholder="Enter your username"
            required
            class="modern-input"
          >

        </div>

        <!-- PASSWORD -->
        <div class="form-group">

          <label>
            Password
          </label>

          <input
            v-model="password"
            type="password"
            placeholder="Enter your password"
            required
            class="modern-input"
          >

        </div>

        <!-- BUTTON -->
        <button
          type="submit"
          class="login-btn"
          :disabled="loading"
        >

          <span v-if="!loading">
            Login
          </span>

          <span v-else>
            Signing In...
          </span>

        </button>

      </form>

      <!-- FOOTER -->
      <div class="footer-text">

        Don’t have an account?

        <RouterLink to="/register">
          Create One
        </RouterLink>

      </div>

    </div>

  </section>

</template>

<style scoped>

/* =========================
   PAGE
========================= */

.login-page {

  position: relative;

  min-height: 100vh;

  display: flex;

  align-items: center;

  justify-content: center;

  padding: 40px 20px;

  overflow: hidden;

  background:
    radial-gradient(
      circle at top left,
      rgba(139,92,246,0.16),
      transparent 25%
    ),

    radial-gradient(
      circle at bottom right,
      rgba(236,72,153,0.12),
      transparent 25%
    ),

    #050816;
}

/* =========================
   GLOWS
========================= */

.glow {

  position: absolute;

  border-radius: 50%;

  filter: blur(120px);

  opacity: 0.22;

  z-index: 0;
}

.glow-1 {

  width: 420px;
  height: 420px;

  background: #8b5cf6;

  top: -120px;
  left: -120px;
}

.glow-2 {

  width: 360px;
  height: 360px;

  background: #ec4899;

  bottom: -120px;
  right: -100px;
}

/* =========================
   CARD
========================= */

.login-card {

  position: relative;

  z-index: 2;

  width: 100%;

  max-width: 520px;

  padding: 52px 42px;

  border-radius: 38px;

  background:
    linear-gradient(
      135deg,
      rgba(12,18,32,0.78),
      rgba(18,24,42,0.62)
    );

  backdrop-filter: blur(28px);

  border:
    1px solid rgba(255,255,255,0.08);

  box-shadow:
    0 25px 50px rgba(0,0,0,0.42);
}

/* =========================
   BRAND
========================= */

.brand {

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 10px;

  margin-bottom: 28px;

  font-weight: 800;

  font-size: 1.25rem;

  color: white;
}

.brand-dot {

  width: 14px;
  height: 14px;

  border-radius: 50%;

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #ec4899
    );

  box-shadow:
    0 0 18px rgba(139,92,246,0.7);
}

/* =========================
   TITLE
========================= */

.title {

  text-align: center;

  font-size: 3rem;

  font-weight: 800;

  color: white;

  margin-bottom: 12px;

  letter-spacing: -0.04em;
}

.subtitle {

  text-align: center;

  color:
    rgba(255,255,255,0.68);

  margin-bottom: 36px;

  line-height: 1.7;
}

/* =========================
   ERROR
========================= */

.error-box {

  padding: 16px 18px;

  border-radius: 20px;

  background:
    rgba(239,68,68,0.14);

  border:
    1px solid rgba(239,68,68,0.2);

  color: #fecaca;

  margin-bottom: 24px;

  text-align: center;

  font-weight: 600;
}

/* =========================
   FORM
========================= */

.login-form {

  display: flex;

  flex-direction: column;

  gap: 24px;
}

/* =========================
   FORM GROUP
========================= */

.form-group {

  display: flex;

  flex-direction: column;

  gap: 10px;
}

.form-group label {

  color:
    rgba(255,255,255,0.82);

  font-size: 0.92rem;

  font-weight: 700;
}

/* =========================
   INPUTS
========================= */

.modern-input {

  width: 100%;

  height: 58px;

  padding: 0 18px;

  border-radius: 20px;

  border:
    1px solid rgba(255,255,255,0.08);

  background:
    rgba(255,255,255,0.06);

  color: white;

  outline: none;

  font-size: 0.96rem;

  transition: all 0.3s ease;

  backdrop-filter: blur(18px);
}

.modern-input::placeholder {

  color:
    rgba(255,255,255,0.42);
}

.modern-input:focus {

  border-color:
    rgba(139,92,246,0.5);

  box-shadow:
    0 0 24px rgba(139,92,246,0.22);
}

/* =========================
   BUTTON
========================= */

.login-btn {

  width: 100%;

  height: 60px;

  border: none;

  border-radius: 22px;

  margin-top: 10px;

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #6d28d9
    );

  color: white;

  font-size: 1rem;

  font-weight: 700;

  cursor: pointer;

  transition: all 0.3s ease;

  box-shadow:
    0 12px 28px rgba(139,92,246,0.3);
}

.login-btn:hover:not(:disabled) {

  transform:
    translateY(-2px);

  box-shadow:
    0 16px 34px rgba(139,92,246,0.4);
}

.login-btn:disabled {

  opacity: 0.6;

  cursor: not-allowed;
}

/* =========================
   FOOTER
========================= */

.footer-text {

  margin-top: 30px;

  text-align: center;

  color:
    rgba(255,255,255,0.6);
}

.footer-text a {

  color: white;

  font-weight: 700;

  margin-left: 6px;

  text-decoration: none;
}

/* =========================
   MOBILE
========================= */

@media (max-width: 768px) {

  .login-card {

    padding: 40px 24px;
  }

  .title {

    font-size: 2.4rem;
  }
}

</style>