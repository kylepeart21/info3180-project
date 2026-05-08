<template>

  <header class="header-wrapper">

    <nav class="modern-navbar glass-card">

      <!-- LOGO -->
      <RouterLink
        class="brand"
        :to="isAuthenticated
          ? `/users/${authStore.user_id}`
          : '/'"
      >

        <div class="brand-glow"></div>

        <span class="brand-text">
         DriftDater
        </span>

      </RouterLink>

      <!-- MOBILE TOGGLE -->
      <button
        class="mobile-toggle"
        @click="menuOpen = !menuOpen"
      >
        ☰
      </button>

      <!-- NAVIGATION -->
      <div
        class="nav-container"
        :class="{ open: menuOpen }"
      >

        <!-- NOT AUTHENTICATED -->
        <template v-if="!isAuthenticated">

          <RouterLink
            class="nav-link"
            to="/"
          >
            Home
          </RouterLink>

          <RouterLink
            class="nav-link"
            to="/register"
          >
            Register
          </RouterLink>

          <RouterLink
            class="nav-link login-btn"
            to="/login"
          >
            Login
          </RouterLink>

        </template>

        <!-- AUTHENTICATED -->
        <template v-else>

          <RouterLink
            class="nav-link"
            :to="`/users/${authStore.user_id}`"
          >
            Browse
          </RouterLink>

          <RouterLink
            class="nav-link"
            to="/profiles/new"
          >
            Create
          </RouterLink>

          <RouterLink
            class="nav-link"
            to="/profiles/edit"
          >
            Edit Profile
          </RouterLink>

          <RouterLink
            class="nav-link"
            to="/profiles/favourites"
          >
            Favourites
          </RouterLink>

          <RouterLink
            class="nav-link"
            to="/messages"
          >
            Messages
          </RouterLink>

          <RouterLink
            class="nav-link logout-btn"
            to="/logout"
          >
            Logout
          </RouterLink>

        </template>

      </div>

    </nav>

  </header>

</template>

<script setup>

import { RouterLink } from 'vue-router'

import { useAuthStore }
from '@/store/authentication'

import {
  computed,
  ref
} from 'vue'

const authStore = useAuthStore()

const isAuthenticated =
  computed(() => authStore.isAuthenticated)

const menuOpen = ref(false)

</script>

<style scoped>

/* =========================
   HEADER WRAPPER
========================= */

.header-wrapper {

  position: fixed;

  top: 20px;

  left: 0;

  width: 100%;

  z-index: 1000;

  padding: 0 20px;

  display: flex;

  justify-content: center;
}

/* =========================
   NAVBAR
========================= */

.modern-navbar {

  width: 100%;

  max-width: 1380px;

  padding: 16px 26px;

  display: flex;

  align-items: center;

  justify-content: space-between;

  border-radius: 28px;

  backdrop-filter: blur(24px);

  background:
    rgba(255,255,255,0.06);

  border:
    1px solid rgba(255,255,255,0.08);
}

/* =========================
   BRAND
========================= */

.brand {

  position: relative;

  display: flex;

  align-items: center;

  gap: 12px;

  text-decoration: none;
}

.brand-glow {

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
    0 0 18px rgba(139,92,246,0.8);
}

.brand-text {

  font-size: 1.4rem;

  font-weight: 800;

  letter-spacing: -0.03em;

  color: white;
}

/* =========================
   NAVIGATION
========================= */

.nav-container {

  display: flex;

  align-items: center;

  gap: 12px;
}

/* =========================
   NAV LINKS
========================= */

.nav-link {

  position: relative;

  padding: 12px 18px;

  border-radius: 16px;

  color:
    rgba(255,255,255,0.82);

  font-weight: 600;

  text-decoration: none;

  transition: all 0.3s ease;
}

/* HOVER */

.nav-link:hover {

  background:
    rgba(255,255,255,0.08);

  color: white;

  transform:
    translateY(-2px);
}

/* ACTIVE LINK */

.nav-link.router-link-active {

  background:
    rgba(139,92,246,0.18);

  color: white;

  box-shadow:
    0 0 22px rgba(139,92,246,0.24);
}

/* =========================
   LOGIN BUTTON
========================= */

.login-btn {

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #6d28d9
    );

  color: white !important;

  box-shadow:
    0 8px 24px rgba(139,92,246,0.28);
}

.login-btn:hover {

  transform:
    translateY(-3px);

  box-shadow:
    0 10px 28px rgba(139,92,246,0.4);
}

/* =========================
   LOGOUT BUTTON
========================= */

.logout-btn {

  background:
    rgba(239,68,68,0.14);

  color: #fca5a5;
}

/* =========================
   MOBILE TOGGLE
========================= */

.mobile-toggle {

  display: none;

  width: 46px;
  height: 46px;

  border-radius: 14px;

  border: none;

  background:
    rgba(255,255,255,0.08);

  color: white;

  font-size: 1.2rem;

  cursor: pointer;
}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 900px) {

  .mobile-toggle {

    display: flex;

    align-items: center;

    justify-content: center;
  }

  .nav-container {

    position: absolute;

    top: 85px;
    left: 0;

    width: 100%;

    flex-direction: column;

    padding: 20px;

    border-radius: 24px;

    background:
      rgba(15,23,42,0.92);

    backdrop-filter: blur(24px);

    border:
      1px solid rgba(255,255,255,0.08);

    opacity: 0;

    pointer-events: none;

    transform:
      translateY(-10px);

    transition: all 0.3s ease;
  }

  .nav-container.open {

    opacity: 1;

    pointer-events: auto;

    transform:
      translateY(0);
  }

  .nav-link {

    width: 100%;

    text-align: center;
  }
}

</style>