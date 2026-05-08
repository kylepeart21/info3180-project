<template>
  <div class="profile-card glass-card">

    <!-- IMAGE -->
    <div class="profile-image-wrapper">

      <img
        :src="profile.photo || '/default-profile.jpg'"
        :alt="profile.name"
        class="profile-image"
      >

      <!-- OVERLAY -->
      <div class="image-overlay"></div>

      <!-- TOP BADGES -->
      <div class="top-badges">

        <div
          v-if="showFavoriteCount"
          class="glass-pill favourite-pill"
        >
          ❤ {{ profile.favourite_count }}
        </div>

        <div
          v-if="isMutualMatch"
          class="glass-pill mutual-pill"
        >
          💚 Mutual Match
        </div>

      </div>

      <!-- PROFILE CONTENT -->
      <div class="profile-content">

        <div class="profile-main">

          <h2 class="profile-name">
            {{ profile.name }}
          </h2>

          <p class="profile-meta">
            {{ calculateAge(profile.birth_year) }}
            •
            {{ profile.parish || 'Jamaica' }}
          </p>

        </div>

        <!-- INTERESTS -->
        <div
          v-if="profile.interests && profile.interests.length"
          class="interests-list"
        >

          <span
            v-for="interest in profile.interests.slice(0, 3)"
            :key="interest"
            class="interest-pill"
          >
            {{ interest }}
          </span>

        </div>

        <!-- EXPANDED INFO -->
        <div
          v-if="expanded"
          class="expanded-section"
        >

          <div class="info-row">
            <span>Sex</span>
            <p>{{ profile.sex }}</p>
          </div>

          <div class="info-row">
            <span>Race</span>
            <p>{{ profile.race }}</p>
          </div>

          <div
            v-if="profile.fav_cuisine"
            class="info-row"
          >
            <span>Favorite Cuisine</span>
            <p>{{ profile.fav_cuisine }}</p>
          </div>

          <div
            v-if="profile.compatibility"
            class="compatibility-box"
          >
            Compatibility
            <strong>{{ profile.compatibility }}%</strong>
          </div>

        </div>

        <!-- ACTIONS -->
        <div class="card-actions">

          <router-link
            :to="`/profiles/${profile.id}`"
            class="details-btn"
          >
            {{ detailsButtonText }}
          </router-link>

          <div class="action-buttons">

            <button
              v-if="showPassButton"
              @click="$emit('pass-profile', profile.user_id_fk)"
              class="pass-btn"
            >
              ✕
            </button>

            <heart-button
              :value="isFavourited"
              :profile-id="profile.id"
              @toggle="$emit('toggle-favourite', profile.user_id_fk)"
            />

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import HeartButton from './HeartButton.vue'

export default {
  name: 'ProfileCard',

  components: {
    HeartButton
  },

  emits: [
    'toggle-favourite',
    'pass-profile'
  ],

  props: {
    profile: {
      type: Object,
      required: true
    },

    isFavourited: {
      type: Boolean,
      default: false
    },

    isMutualMatch: {
      type: Boolean,
      default: false
    },

    expanded: {
      type: Boolean,
      default: false
    },

    showFavoriteCount: {
      type: Boolean,
      default: false
    },

    showPassButton: {
      type: Boolean,
      default: false
    },

    detailsButtonText: {
      type: String,
      default: 'View Profile'
    }
  },

  methods: {

    calculateAge(birthYear) {

      if (!birthYear) return '—'

      return new Date().getFullYear() - birthYear
    }
  }
}
</script>

<style scoped>

.profile-card {

  width: 100%;

  min-height: 560px;

  overflow: hidden;

  border-radius: 34px;

  transition: all 0.45s ease;
}

.profile-card:hover {

  transform:
    translateY(-10px)
    scale(1.015);
}

.profile-image-wrapper {

  position: relative;

  width: 100%;

  height: 560px;
}

.profile-image {

  width: 100%;
  height: 100%;

  object-fit: cover;

  transition:
    transform 0.7s ease;
}

.profile-card:hover .profile-image {

  transform: scale(1.06);
}

/* OVERLAY */

.image-overlay {

  position: absolute;

  inset: 0;

  background:
    linear-gradient(
      to top,
      rgba(0,0,0,0.92) 0%,
      rgba(0,0,0,0.18) 45%,
      rgba(0,0,0,0.08) 100%
    );
}

/* BADGES */

.top-badges {

  position: absolute;

  top: 18px;
  left: 18px;
  right: 18px;

  display: flex;

  justify-content: space-between;

  z-index: 3;
}

.glass-pill {

  padding: 8px 14px;

  border-radius: 999px;

  backdrop-filter: blur(14px);

  background:
    rgba(255,255,255,0.14);

  border:
    1px solid rgba(255,255,255,0.12);

  font-size: 0.8rem;

  font-weight: 700;

  color: white;
}

.mutual-pill {

  background:
    rgba(34,197,94,0.25);
}

/* CONTENT */

.profile-content {

  position: absolute;

  bottom: 0;

  width: 100%;

  padding: 28px;

  z-index: 3;
}

.profile-name {

  font-size: 2rem;

  font-weight: 800;

  color: white;

  margin-bottom: 4px;
}

.profile-meta {

  color:
    rgba(255,255,255,0.78);

  font-size: 1rem;
}

/* INTERESTS */

.interests-list {

  display: flex;

  flex-wrap: wrap;

  gap: 10px;

  margin-top: 18px;
}

.interest-pill {

  padding: 8px 14px;

  border-radius: 999px;

  background:
    rgba(255,255,255,0.12);

  backdrop-filter: blur(10px);

  border:
    1px solid rgba(255,255,255,0.08);

  color: white;

  font-size: 0.82rem;

  font-weight: 600;
}

/* EXPANDED */

.expanded-section {

  margin-top: 22px;

  padding-top: 18px;

  border-top:
    1px solid rgba(255,255,255,0.08);
}

.info-row {

  display: flex;

  justify-content: space-between;

  margin-bottom: 10px;
}

.info-row span {

  color:
    rgba(255,255,255,0.62);

  font-size: 0.9rem;
}

.info-row p {

  color: white;

  font-weight: 600;
}

.compatibility-box {

  margin-top: 18px;

  padding: 14px;

  border-radius: 18px;

  background:
    rgba(255,255,255,0.08);

  text-align: center;

  color: white;
}

.compatibility-box strong {

  color: #22c55e;

  margin-left: 8px;
}

/* ACTIONS */

.card-actions {

  display: flex;

  justify-content: space-between;

  align-items: center;

  margin-top: 26px;
}

.details-btn {

  flex: 1;

  text-align: center;

  padding: 14px 18px;

  border-radius: 18px;

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #6d28d9
    );

  color: white;

  font-weight: 700;

  transition: all 0.3s ease;

  box-shadow:
    0 8px 22px rgba(139,92,246,0.32);
}

.details-btn:hover {

  transform:
    translateY(-2px);

  box-shadow:
    0 10px 28px rgba(139,92,246,0.42);
}

.action-buttons {

  display: flex;

  align-items: center;

  gap: 12px;

  margin-left: 16px;
}

.pass-btn {

  width: 52px;
  height: 52px;

  border-radius: 50%;

  border: none;

  background:
    rgba(255,255,255,0.12);

  backdrop-filter: blur(12px);

  color: white;

  font-size: 1.2rem;

  cursor: pointer;

  transition: all 0.3s ease;
}

.pass-btn:hover {

  background:
    rgba(239,68,68,0.28);

  transform:
    scale(1.08);
}

@media (max-width: 768px) {

  .profile-card {

    min-height: 500px;
  }

  .profile-image-wrapper {

    height: 500px;
  }

  .profile-name {

    font-size: 1.7rem;
  }

  .card-actions {

    flex-direction: column;

    gap: 14px;
  }

  .action-buttons {

    margin-left: 0;
  }
}

</style>