<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>

  <section class="hero-page">

    <!-- BACKGROUND GLOW -->
    <div class="hero-glow hero-glow-1"></div>
    <div class="hero-glow hero-glow-2"></div>

    <!-- HERO CONTENT -->
    <div class="hero-container">

      <div class="hero-content glass-card">

        <!-- TOP BADGE -->
        <div class="hero-badge">
          ✨ Jamaica's Modern Dating Experience
        </div>

        <!-- TITLE -->
        <h1 class="hero-title">

          Meet Real People.
          <br>

          Build Real Connections.

        </h1>

        <!-- DESCRIPTION -->
        <p class="hero-description">

          Discover meaningful relationships through
          a premium modern dating platform designed
          for authentic connections, compatibility,
          and genuine interaction.

        </p>

        <!-- CTA BUTTONS -->
        <div class="hero-actions">

          <RouterLink
            to="/register"
            class="primary-btn hero-btn"
          >
            Create Account
          </RouterLink>

          <RouterLink
            to="/login"
            class="secondary-btn hero-btn"
          >
            Login
          </RouterLink>

        </div>

        <!-- STATS -->
        <div class="hero-stats">

          <div class="stat-item">
            <h3>5K+</h3>
            <p>Users</p>
          </div>

          <div class="stat-item">
            <h3>1K+</h3>
            <p>Matches</p>
          </div>

          <div class="stat-item">
            <h3>24/7</h3>
            <p>Connections</p>
          </div>

        </div>

      </div>

    </div>

  </section>

</template>

<style scoped>

/* =========================
   HERO PAGE
========================= */

.hero-page {

  position: relative;

  min-height: 100vh;

  overflow: hidden;

  display: flex;

  align-items: center;

  justify-content: center;

  padding: 40px 20px;
}

/* =========================
   BACKGROUND GLOWS
========================= */

.hero-glow {

  position: absolute;

  border-radius: 50%;

  filter: blur(120px);

  opacity: 0.25;

  pointer-events: none;
}

.hero-glow-1 {

  width: 420px;
  height: 420px;

  background: #8b5cf6;

  top: -100px;
  left: -120px;
}

.hero-glow-2 {

  width: 360px;
  height: 360px;

  background: #ec4899;

  bottom: -120px;
  right: -80px;
}

/* =========================
   HERO CONTAINER
========================= */

.hero-container {

  width: 100%;

  max-width: 1200px;

  display: flex;

  justify-content: center;

  align-items: center;

  z-index: 2;
}

/* =========================
   HERO CONTENT
========================= */

.hero-content {

  width: 100%;

  max-width: 720px;

  padding: 60px;

  text-align: center;

  border-radius: 36px;
}

/* =========================
   HERO BADGE
========================= */

.hero-badge {

  display: inline-flex;

  align-items: center;

  justify-content: center;

  padding: 10px 18px;

  margin-bottom: 28px;

  border-radius: 999px;

  background:
    rgba(255,255,255,0.08);

  border:
    1px solid rgba(255,255,255,0.08);

  backdrop-filter: blur(12px);

  color: rgba(255,255,255,0.92);

  font-size: 0.9rem;

  font-weight: 600;
}

/* =========================
   TITLE
========================= */

.hero-title {

  font-size: clamp(3rem, 8vw, 5.8rem);

  font-weight: 800;

  line-height: 1;

  letter-spacing: -0.05em;

  margin-bottom: 24px;

  color: white;
}

/* =========================
   DESCRIPTION
========================= */

.hero-description {

  max-width: 620px;

  margin: 0 auto 42px;

  font-size: 1.15rem;

  line-height: 1.8;

  color:
    rgba(255,255,255,0.72);
}

/* =========================
   BUTTONS
========================= */

.hero-actions {

  display: flex;

  justify-content: center;

  gap: 18px;

  margin-bottom: 52px;

  flex-wrap: wrap;
}

.hero-btn {

  min-width: 180px;

  padding: 16px 24px;

  font-size: 1rem;

  font-weight: 700;

  border-radius: 20px;

  text-align: center;
}

/* SECONDARY BUTTON */

.secondary-btn {

  background:
    rgba(255,255,255,0.08);

  color: white;

  border:
    1px solid rgba(255,255,255,0.1);

  backdrop-filter: blur(12px);

  transition: all 0.35s ease;
}

.secondary-btn:hover {

  background:
    rgba(255,255,255,0.14);

  transform:
    translateY(-3px);
}

/* =========================
   STATS
========================= */

.hero-stats {

  display: flex;

  justify-content: center;

  gap: 60px;

  flex-wrap: wrap;
}

.stat-item {

  text-align: center;
}

.stat-item h3 {

  font-size: 2rem;

  font-weight: 800;

  color: white;

  margin-bottom: 4px;
}

.stat-item p {

  color:
    rgba(255,255,255,0.65);

  font-size: 0.95rem;
}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 768px) {

  .hero-content {

    padding: 40px 28px;
  }

  .hero-title {

    font-size: 3.2rem;
  }

  .hero-description {

    font-size: 1rem;
  }

  .hero-stats {

    gap: 28px;
  }

  .hero-actions {

    flex-direction: column;
  }

  .hero-btn {

    width: 100%;
  }
}

</style>