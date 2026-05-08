<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>

  <section class="hero-page">

    <!-- DARK OVERLAY -->
    <div class="hero-overlay"></div>

    <!-- BACKGROUND GLOWS -->
    <div class="hero-glow hero-glow-1"></div>
    <div class="hero-glow hero-glow-2"></div>

    <!-- CONTENT -->
    <div class="hero-container">

      <div class="hero-content glass-card">

        <!-- BADGE -->
        <div class="hero-badge">
          ✨ Jamaica's Modern Dating Experience
        </div>

        <!-- TITLE -->
        <h1 class="hero-title">

          Meet Real
          <br>

          People.
          <br>

          Build Real
          <br>

          Connections.

        </h1>

        <!-- DESCRIPTION -->
        <p class="hero-description">

          Discover meaningful relationships through
          a premium modern dating platform designed
          for authentic connections, compatibility,
          and genuine interaction.

        </p>

        <!-- BUTTONS -->
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
   DARK OVERLAY
========================= */

.hero-overlay {

  position: absolute;

  inset: 0;

  background:
    linear-gradient(
      180deg,
      rgba(0,0,0,0.45),
      rgba(0,0,0,0.35)
    );

  z-index: 1;
}

/* =========================
   GLOWS
========================= */

.hero-glow {

  position: absolute;

  border-radius: 50%;

  filter: blur(120px);

  opacity: 0.22;

  pointer-events: none;

  z-index: 0;
}

.hero-glow-1 {

  width: 420px;
  height: 420px;

  background: #8b5cf6;

  top: -120px;
  left: -120px;
}

.hero-glow-2 {

  width: 380px;
  height: 380px;

  background: #ec4899;

  bottom: -140px;
  right: -100px;
}

/* =========================
   CONTAINER
========================= */

.hero-container {

  position: relative;

  z-index: 2;

  width: 100%;

  max-width: 1200px;

  display: flex;

  justify-content: center;

  align-items: center;
}

/* =========================
   HERO CONTENT
========================= */

.hero-content {

  width: 100%;

  max-width: 760px;

  padding: 70px 60px;

  text-align: center;

  border-radius: 36px;

  background:
    linear-gradient(
      135deg,
      rgba(12,18,32,0.78),
      rgba(18,24,42,0.62)
    );

  border:
    1px solid rgba(255,255,255,0.10);

  backdrop-filter: blur(26px);

  box-shadow:
    0 25px 60px rgba(0,0,0,0.55);
}

/* =========================
   BADGE
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

  color:
    rgba(255,255,255,0.92);

  font-size: 0.9rem;

  font-weight: 600;

  backdrop-filter: blur(12px);
}

/* =========================
   TITLE
========================= */

.hero-title {

  font-size:
    clamp(3.5rem, 8vw, 6rem);

  font-weight: 800;

  line-height: 0.95;

  letter-spacing: -0.05em;

  color: white;

  margin-bottom: 30px;

  text-shadow:
    0 10px 30px rgba(0,0,0,0.45);
}

/* =========================
   DESCRIPTION
========================= */

.hero-description {

  max-width: 620px;

  margin: 0 auto 44px;

  font-size: 1.15rem;

  line-height: 1.8;

  color:
    rgba(255,255,255,0.82);
}

/* =========================
   BUTTONS
========================= */

.hero-actions {

  display: flex;

  justify-content: center;

  gap: 18px;

  flex-wrap: wrap;

  margin-bottom: 56px;
}

.hero-btn {

  min-width: 190px;

  padding: 16px 24px;

  border-radius: 20px;

  font-size: 1rem;

  font-weight: 700;

  text-align: center;
}

/* SECONDARY */

.secondary-btn {

  background:
    rgba(255,255,255,0.14);

  color: white;

  border:
    1px solid rgba(255,255,255,0.10);

  backdrop-filter: blur(12px);

  transition: all 0.35s ease;
}

.secondary-btn:hover {

  background:
    rgba(255,255,255,0.18);

  transform:
    translateY(-3px);
}

/* =========================
   STATS
========================= */

.hero-stats {

  display: flex;

  justify-content: center;

  gap: 70px;

  flex-wrap: wrap;
}

.stat-item {

  text-align: center;
}

.stat-item h3 {

  font-size: 2.2rem;

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

    padding: 48px 28px;
  }

  .hero-title {

    font-size: 3.3rem;
  }

  .hero-description {

    font-size: 1rem;
  }

  .hero-actions {

    flex-direction: column;
  }

  .hero-btn {

    width: 100%;
  }

  .hero-stats {

    gap: 28px;
  }
}

</style>