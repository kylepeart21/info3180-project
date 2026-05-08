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

  top: 18px;

  left: 0;

  width: 100%;

  z-index: 2000;

  display: flex;

  justify-content: center;

  padding: 0 20px;
}

/* =========================
   NAVBAR
========================= */

.modern-navbar {

  width: 100%;

  max-width: 1400px;

  height: 78px;

  padding: 0 26px;

  display: flex;

  align-items: center;

  justify-content: space-between;

  border-radius: 30px;

  background:
    linear-gradient(
      135deg,
      rgba(8,12,24,0.82),
      rgba(15,23,42,0.72)
    );

  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);

  border:
    1px solid rgba(255,255,255,0.08);

  box-shadow:
    0 10px 40px rgba(0,0,0,0.35),
    inset 0 1px 0 rgba(255,255,255,0.05);
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

  color: white;

  font-size: 1.4rem;

  font-weight: 800;

  letter-spacing: -0.03em;

  opacity: 0.96;
}

/* =========================
   NAVIGATION
========================= */

.nav-container {

  display: flex;

  align-items: center;

  gap: 10px;
}

/* =========================
   LINKS
========================= */

.nav-link {

  position: relative;

  padding: 13px 18px;

  border-radius: 18px;

  color:
    rgba(255,255,255,0.72);

  font-size: 0.95rem;

  font-weight: 600;

  text-decoration: none;

  transition: all 0.28s ease;
}

/* HOVER */

.nav-link:hover {

  background:
    rgba(255,255,255,0.08);

  color: white;

  transform:
    translateY(-2px);
}

/* ACTIVE */

.nav-link.router-link-active {

  background:
    linear-gradient(
      135deg,
      rgba(139,92,246,0.22),
      rgba(236,72,153,0.16)
    );

  color: white;

  box-shadow:
    0 0 24px rgba(139,92,246,0.24);
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
    0 8px 26px rgba(139,92,246,0.32);
}

.login-btn:hover {

  transform:
    translateY(-3px);

  box-shadow:
    0 12px 30px rgba(139,92,246,0.45);
}

/* =========================
   LOGOUT BUTTON
========================= */

.logout-btn {

  background:
    rgba(239,68,68,0.14);

  color: #fca5a5;

  border:
    1px solid rgba(239,68,68,0.12);
}

.logout-btn:hover {

  background:
    rgba(239,68,68,0.22);
}

/* =========================
   MOBILE BUTTON
========================= */

.mobile-toggle {

  display: none;

  width: 48px;
  height: 48px;

  border-radius: 16px;

  border: none;

  background:
    rgba(255,255,255,0.08);

  color: white;

  font-size: 1.15rem;

  cursor: pointer;

  transition: all 0.3s ease;
}

.mobile-toggle:hover {

  background:
    rgba(255,255,255,0.12);
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

    top: 92px;
    left: 0;

    width: 100%;

    flex-direction: column;

    gap: 14px;

    padding: 24px;

    border-radius: 28px;

    background:
      rgba(8,12,24,0.92);

    backdrop-filter: blur(28px);

    border:
      1px solid rgba(255,255,255,0.08);

    opacity: 0;

    pointer-events: none;

    transform:
      translateY(-12px);

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