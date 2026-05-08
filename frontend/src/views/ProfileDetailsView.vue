<script>
import HeartButton from '@/components/HeartButton.vue'
import { useAuthStore } from '@/store/authentication.js'
import apiClient from '@/http.js'
import { nextTick } from "vue"

export default {

  name: 'ProfileDetailsView',

  components: {
    HeartButton
  },

  data() {

    return {

      profile: {},

      loading: true,

      error: null,

      isFavorited: false,

      isMutualMatch: false,

      isPassed: false,

      isBlocked: false,

      showMatches: false,

      showBlockConfirm: false,

      matches: [],

      loadingMatches: false
    }
  },

  created() {

    this.fetchProfileDetails().then(() => {

      this.checkIfFavorited()

      this.checkMutualMatch()
    })
  },

  methods: {

    /* =========================
       FETCH PROFILE
    ========================= */

    async fetchProfileDetails() {

      try {

        const profileId =
          this.$route.params.profile_id

        const token =
          localStorage.getItem('jwt')

        const response =
          await apiClient.get(
            `/api/profiles/${profileId}`,
            {
              headers: {
                'Authorization':
                  `Bearer ${token}`
              }
            }
          )

        this.profile =
          response.data.profile

        this.loading = false

      } catch (err) {

        this.error = err.message

        this.loading = false
      }
    },

    /* =========================
       FAVORITES
    ========================= */

    async checkIfFavorited() {

      try {

        const authStore =
          useAuthStore()

        const token =
          localStorage.getItem('jwt')

        const response =
          await apiClient.get(
            `/api/users/${authStore.user_id}/favourites`,
            {
              headers: {
                'Authorization':
                  `Bearer ${token}`
              }
            }
          )

        const favouriteUserIds =
          response.data.map(u => u.id)

        this.isFavorited =
          favouriteUserIds.includes(
            this.profile.user_id_fk
          )

      } catch (err) {

        console.error(
          'Error checking favorite status:',
          err
        )
      }
    },

    async toggleFavorite() {

      try {

        const token =
          localStorage.getItem('jwt')

        const headers = {
          'Authorization':
            `Bearer ${token}`
        }

        if (this.isFavorited) {

          await apiClient.delete(
            `/api/profiles/${this.profile.user_id_fk}/favourite`,
            { headers }
          )

        } else {

          await apiClient.post(
            `/api/profiles/${this.profile.user_id_fk}/favourite`,
            {},
            { headers }
          )
        }

        this.isFavorited =
          !this.isFavorited

        this.$toast?.success(
          `Profile ${
            this.isFavorited
              ? 'added to'
              : 'removed from'
          } favorites`
        )

      } catch (err) {

        console.error(
          'Error toggling favorite:',
          err
        )

        this.$toast?.error(
          'Favorite action failed'
        )
      }
    },

    /* =========================
       MATCHES
    ========================= */

    async checkMutualMatch() {

      try {

        const token =
          localStorage.getItem('jwt')

        const res =
          await apiClient.get(
            '/api/profiles/mutual-matches',
            {
              headers: {
                'Authorization':
                  `Bearer ${token}`
              }
            }
          )

        const mutualIds =
          res.data.profiles.map(
            p => p.user_id_fk
          )

        this.isMutualMatch =
          mutualIds.includes(
            this.profile.user_id_fk
          )

      } catch (e) {

        console.error(
          'Error checking mutual match:',
          e
        )
      }
    },

    async matchMe() {

      this.showMatches = true

      this.loadingMatches = true

      try {

        const profileId =
          this.$route.params.profile_id

        const token =
          localStorage.getItem('jwt')

        const response =
          await apiClient.get(
            `/api/profiles/matches/${profileId}`,
            {
              headers: {
                'Authorization':
                  `Bearer ${token}`
              }
            }
          )

        this.matches =
          response.data.profiles

        this.loadingMatches = false

        await nextTick()

        const el =
          document.querySelector(
            '.matches-container'
          )

        if (el) {

          el.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          })
        }

      } catch (err) {

        console.error(
          'Error finding matches:',
          err
        )

        this.loadingMatches = false
      }
    },

    /* =========================
       PASS PROFILE
    ========================= */

    async passProfile() {

      try {

        const token =
          localStorage.getItem('jwt')

        await apiClient.post(
          `/api/profiles/${this.profile.user_id_fk}/pass`,
          {},
          {
            headers: {
              'Authorization':
                `Bearer ${token}`
            }
          }
        )

        this.isPassed = true

        this.$toast?.success(
          'Profile passed'
        )

      } catch (e) {

        console.error(
          'Error passing profile:',
          e
        )
      }
    },

    /* =========================
       BLOCK USER
    ========================= */

    async blockUser() {

      try {

        if (
          this.profile.user_id_fk ===
          useAuthStore().user_id
        ) {

          return
        }

        const token =
          localStorage.getItem('jwt')

        await apiClient.post(
          `/api/block/${this.profile.user_id_fk}`,
          {},
          {
            headers: {
              'Authorization':
                `Bearer ${token}`
            }
          }
        )

        this.isBlocked = true

        this.showBlockConfirm = false

        this.matches =
          this.matches.filter(
            m =>
              m.user_id_fk !==
              this.profile.user_id_fk
          )

        this.$toast?.success(
          'User blocked'
        )

        this.$router.push(
          `/users/${useAuthStore().user_id}`
        )

      } catch (error) {

        console.error(
          'Error blocking user:',
          error
        )

        this.$toast?.error(
          'Failed to block user'
        )
      }
    },

    /* =========================
       HELPERS
    ========================= */

    calculateAge(birthYear) {

      const currentYear =
        new Date().getFullYear()

      return currentYear - birthYear
    },

    formatHeight(cm) {

      if (!cm)
        return 'Not specified'

      const totalInches =
        cm / 2.54

      const feet =
        Math.floor(totalInches / 12)

      const inches =
        Math.round(totalInches % 12)

      return `${feet}'${inches}"`
    },

    sendEmail() {

      this.$toast?.info(
        'Email functionality coming soon!'
      )
    }
  }
}
</script>

<template>

  <div class="profile-details">

    <!-- LOADING -->

    <div
      v-if="loading"
      class="loading-container"
    >

      <div class="spinner"></div>

      <p>
        Loading profile...
      </p>

    </div>

    <!-- ERROR -->

    <div
      v-else-if="error"
      class="error-container"
    >

      <div class="error-icon">
        ⚠️
      </div>

      <p>
        {{ error }}
      </p>

      <button
        @click="fetchProfileDetails"
        class="retry-btn"
      >
        Try Again
      </button>

    </div>

    <!-- PROFILE -->

    <div
      v-else
      class="profile-container"
    >

      <!-- HEADER -->

      <div class="profile-header">

        <div class="header-left">

          <h1>
            {{ profile.name }}'s Profile
          </h1>

          <div
            v-if="isMutualMatch"
            class="mutual-badge"
          >
            Mutual Match 💚
          </div>

        </div>

        <!-- ACTIONS -->

        <div class="actions">

          <!-- FAVORITE -->

          <heart-button
            :value="isFavorited"
            :profile-id="profile.id"
            @toggle="toggleFavorite"
          />

          <!-- PASS -->

          <button
            class="action-btn pass-btn"
            @click="passProfile"
            :disabled="isPassed"
          >

            {{ isPassed ? 'Passed' : 'Pass' }}

          </button>

          <!-- MESSAGE -->

          <router-link
            :to="`/messages?userId=${profile.user_id_fk}`"
            class="action-btn msg-btn"
          >

            <span class="btn-icon">
              💬
            </span>

            Message

          </router-link>

          <!-- MATCH -->

          <button
            class="action-btn match-btn"
            @click="matchMe"
          >

            <span class="btn-icon">
              🔄
            </span>

            Match Me

          </button>

          <!-- BLOCK -->

          <button
            v-if="!isBlocked"
            @click="showBlockConfirm = true"
            class="action-btn block-btn"
          >

            Block

          </button>

        </div>

      </div>

      <!-- BODY -->

      <div class="profile-body">

        <!-- IMAGE -->

        <div class="profile-image">

          <img
            :src="profile.photo || '/default-profile.jpg'"
            :alt="profile.name"
          >

        </div>

        <!-- INFO -->

        <div class="profile-info">

          <!-- PERSONAL -->

          <div class="info-section">

            <h2>
              Personal Information
            </h2>

            <div class="info-grid">

              <div class="info-item">

                <span class="info-label">
                  Name:
                </span>

                <span class="info-value">
                  {{ profile.name }}
                </span>

              </div>

              <div class="info-item">

                <span class="info-label">
                  Age:
                </span>

                <span class="info-value">
                  {{ calculateAge(profile.birth_year) }}
                </span>

              </div>

              <div class="info-item">

                <span class="info-label">
                  Sex:
                </span>

                <span class="info-value">
                  {{ profile.sex }}
                </span>

              </div>

              <div class="info-item">

                <span class="info-label">
                  Race:
                </span>

                <span class="info-value">
                  {{ profile.race }}
                </span>

              </div>

              <div class="info-item">

                <span class="info-label">
                  Height:
                </span>

                <span class="info-value">
                  {{ formatHeight(profile.height) }}
                </span>

              </div>

              <div class="info-item">

                <span class="info-label">
                  Parish:
                </span>

                <span class="info-value">
                  {{ profile.parish || 'Not specified' }}
                </span>

              </div>

            </div>

          </div>

          <!-- PREFERENCES -->

          <div class="info-section">

            <h2>
              Preferences
            </h2>

            <div class="info-grid">

              <div class="info-item">

                <span class="info-label">
                  Favorite Cuisine:
                </span>

                <span class="info-value">
                  {{ profile.fav_cuisine }}
                </span>

              </div>

              <div class="info-item">

                <span class="info-label">
                  Favorite Color:
                </span>

                <span class="info-value">
                  {{ profile.fav_colour }}
                </span>

              </div>

              <div class="info-item">

                <span class="info-label">
                  Favorite School Subject:
                </span>

                <span class="info-value">
                  {{ profile.fav_school_subject }}
                </span>

              </div>

            </div>

          </div>

          <!-- VALUES -->

          <div class="info-section">

            <h2>
              Values
            </h2>

            <div class="info-grid">

              <div class="info-item">

                <span class="info-label">
                  Political:
                </span>

                <span class="info-value">
                  {{ profile.political ? 'Yes' : 'No' }}
                </span>

              </div>

              <div class="info-item">

                <span class="info-label">
                  Religious:
                </span>

                <span class="info-value">
                  {{ profile.religious ? 'Yes' : 'No' }}
                </span>

              </div>

              <div class="info-item">

                <span class="info-label">
                  Family Oriented:
                </span>

                <span class="info-value">
                  {{ profile.family_oriented ? 'Yes' : 'No' }}
                </span>

              </div>

            </div>

          </div>

          <!-- BIO -->

          <div
            v-if="profile.biography"
            class="info-section"
          >

            <h2>
              Biography
            </h2>

            <p class="biography">
              {{ profile.biography }}
            </p>

          </div>

        </div>

      </div>

      <!-- MATCHES -->

      <div
        v-if="showMatches"
        class="matches-container"
      >

        <h2>
          Your Matches
        </h2>

        <!-- LOADING -->

        <div
          v-if="loadingMatches"
          class="loading-matches"
        >

          <div class="spinner"></div>

          <p>
            Finding matches...
          </p>

        </div>

        <!-- NO MATCHES -->

        <div
          v-else-if="matches.length === 0"
          class="no-matches"
        >

          <p>
            No matches found.
            Your perfect match might not be on DriftDater yet!
          </p>

        </div>

        <!-- MATCH LIST -->

        <div
          v-else
          class="matches-list"
        >

          <div
            v-for="match in matches"
            :key="match.id"
            class="match-card"
          >

            <div class="match-image">

              <img
                :src="match.photo || '/default-profile.jpg'"
                :alt="match.name"
              >

              <div class="compatibility-badge">

                {{ match.compatibility }}%

              </div>

            </div>

            <div class="match-info">

              <h3>
                {{ match.name }}
              </h3>

              <p>
                Age:
                {{ calculateAge(match.birth_year) }}
              </p>

              <p>
                {{ match.sex }},
                {{ match.parish }}
              </p>

              <!-- MATCH ATTRIBUTES -->

              <div class="matching-attributes">

                <p>
                  Matching on:
                </p>

                <ul class="attribute-list">

                  <li
                    v-if="match.fav_cuisine === profile.fav_cuisine"
                  >
                    Cuisine
                  </li>

                  <li
                    v-if="match.fav_colour === profile.fav_colour"
                  >
                    Color
                  </li>

                  <li
                    v-if="match.fav_school_subject === profile.fav_school_subject"
                  >
                    School Subject
                  </li>

                  <li
                    v-if="match.political === profile.political"
                  >
                    Political Views
                  </li>

                  <li
                    v-if="match.religious === profile.religious"
                  >
                    Religious Views
                  </li>

                  <li
                    v-if="match.family_oriented === profile.family_oriented"
                  >
                    Family Values
                  </li>

                </ul>

              </div>

              <!-- VIEW PROFILE -->

              <router-link
                :to="`/profiles/${match.id}`"
                class="view-btn"
              >

                View Profile

              </router-link>

            </div>

          </div>

        </div>

      </div>

    </div>

    <!-- BLOCK MODAL -->

    <div
      v-if="showBlockConfirm"
      class="modal-overlay"
    >

      <div class="block-modal">

        <h2>
          Block {{ profile.name }}?
        </h2>

        <p>
          You will no longer see each other,
          send messages,
          or appear in matches.
        </p>

        <div class="modal-actions">

          <button
            class="cancel-btn"
            @click="showBlockConfirm = false"
          >

            Cancel

          </button>

          <button
            class="confirm-block-btn"
            @click="blockUser"
          >

            Block User

          </button>

        </div>

      </div>

    </div>

  </div>

</template>

<style scoped>

/* =========================
   PAGE
========================= */

.profile-details {

  min-height: 100vh;

  padding:
    140px 40px 80px;

  background:
    radial-gradient(
      circle at top left,
      rgba(139,92,246,0.18),
      transparent 25%
    ),

    radial-gradient(
      circle at bottom right,
      rgba(236,72,153,0.14),
      transparent 25%
    ),

    #050816;

  max-width: 1600px;

  margin: 0 auto;
}

/* =========================
   LOADING / ERROR
========================= */

.loading-container,
.error-container {

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  padding: 80px;

  border-radius: 34px;

  background:
    linear-gradient(
      135deg,
      rgba(12,18,32,0.76),
      rgba(18,24,42,0.62)
    );

  backdrop-filter: blur(24px);

  border:
    1px solid rgba(255,255,255,0.08);

  color: white;

  text-align: center;
}

/* =========================
   SPINNER
========================= */

.spinner {

  width: 44px;
  height: 44px;

  border-radius: 50%;

  border:
    4px solid rgba(255,255,255,0.12);

  border-top:
    4px solid #8b5cf6;

  animation: spin 1s linear infinite;

  margin-bottom: 20px;
}

@keyframes spin {

  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* =========================
   PROFILE CONTAINER
========================= */

.profile-container {

  border-radius: 38px;

  overflow: hidden;

  background:
    linear-gradient(
      135deg,
      rgba(12,18,32,0.76),
      rgba(18,24,42,0.62)
    );

  backdrop-filter: blur(28px);

  border:
    1px solid rgba(255,255,255,0.08);

  box-shadow:
    0 25px 50px rgba(0,0,0,0.42);
}

/* =========================
   HEADER
========================= */

.profile-header {

  display: flex;

  justify-content: space-between;

  align-items: center;

  flex-wrap: wrap;

  gap: 20px;

  padding: 34px 40px;

  border-bottom:
    1px solid rgba(255,255,255,0.06);
}

.header-left {

  display: flex;

  flex-direction: column;

  gap: 10px;
}

.profile-header h1 {

  margin: 0;

  color: white;

  font-size: 2.5rem;

  font-weight: 800;

  letter-spacing: -0.04em;
}

/* =========================
   MUTUAL BADGE
========================= */

.mutual-badge {

  display: inline-flex;

  align-items: center;

  justify-content: center;

  width: fit-content;

  padding: 10px 18px;

  border-radius: 999px;

  background:
    rgba(34,197,94,0.18);

  border:
    1px solid rgba(34,197,94,0.24);

  color: white;

  font-size: 0.85rem;

  font-weight: 700;

  backdrop-filter: blur(16px);
}

/* =========================
   ACTIONS
========================= */

.actions {

  display: flex;

  flex-wrap: wrap;

  gap: 14px;

  align-items: center;
}

.action-btn {

  display: flex;

  align-items: center;

  gap: 8px;

  padding: 14px 22px;

  border-radius: 18px;

  border: none;

  cursor: pointer;

  font-weight: 700;

  text-decoration: none;

  transition: all 0.3s ease;

  backdrop-filter: blur(16px);
}

.action-btn:hover {

  transform:
    translateY(-2px);
}

/* PASS */

.pass-btn {

  background:
    rgba(255,255,255,0.08);

  color: white;

  border:
    1px solid rgba(255,255,255,0.08);
}

.pass-btn:hover {

  background:
    rgba(239,68,68,0.18);
}

/* MESSAGE */

.msg-btn {

  background:
    linear-gradient(
      135deg,
      #22c55e,
      #16a34a
    );

  color: white;

  box-shadow:
    0 10px 24px rgba(34,197,94,0.28);
}

/* MATCH */

.match-btn {

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #6d28d9
    );

  color: white;

  box-shadow:
    0 10px 24px rgba(139,92,246,0.3);
}

/* BLOCK */

.block-btn {

  background:
    rgba(239,68,68,0.16);

  border:
    1px solid rgba(239,68,68,0.18);

  color: #fca5a5;
}

.block-btn:hover {

  background:
    rgba(239,68,68,0.28);

  box-shadow:
    0 12px 24px rgba(239,68,68,0.18);
}

/* =========================
   BODY
========================= */

.profile-body {

  display: grid;

  grid-template-columns:
    420px 1fr;

  gap: 40px;

  padding: 40px;
}

/* =========================
   IMAGE
========================= */

.profile-image {

  position: relative;

  overflow: hidden;

  border-radius: 34px;

  height: 620px;

  background:
    rgba(255,255,255,0.05);

  border:
    1px solid rgba(255,255,255,0.08);
}

.profile-image img {

  width: 100%;

  height: 100%;

  object-fit: cover;

  transition: transform 0.5s ease;
}

.profile-image:hover img {

  transform: scale(1.05);
}

/* =========================
   INFO
========================= */

.profile-info {

  display: flex;

  flex-direction: column;

  gap: 28px;
}

/* =========================
   SECTIONS
========================= */

.info-section {

  padding: 28px;

  border-radius: 28px;

  background:
    rgba(255,255,255,0.05);

  border:
    1px solid rgba(255,255,255,0.06);

  backdrop-filter: blur(20px);
}

.info-section h2 {

  margin-top: 0;

  margin-bottom: 22px;

  color: white;

  font-size: 1.4rem;

  font-weight: 700;

  letter-spacing: -0.02em;
}

/* =========================
   GRID
========================= */

.info-grid {

  display: grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap: 20px;
}

.info-item {

  display: flex;

  flex-direction: column;

  gap: 6px;
}

.info-label {

  color:
    rgba(255,255,255,0.5);

  font-size: 0.85rem;

  font-weight: 600;

  text-transform: uppercase;

  letter-spacing: 0.04em;
}

.info-value {

  color: white;

  font-size: 1rem;

  font-weight: 600;
}

/* =========================
   BIO
========================= */

.biography {

  line-height: 1.9;

  color:
    rgba(255,255,255,0.78);

  font-size: 1rem;
}

/* =========================
   MATCHES
========================= */

.matches-container {

  margin-top: 40px;

  padding: 40px;

  border-radius: 34px;

  background:
    linear-gradient(
      135deg,
      rgba(12,18,32,0.72),
      rgba(18,24,42,0.58)
    );

  border:
    1px solid rgba(255,255,255,0.08);

  backdrop-filter: blur(24px);
}

.matches-container h2 {

  color: white;

  font-size: 2rem;

  font-weight: 800;

  margin-bottom: 30px;
}

/* =========================
   MATCH GRID
========================= */

.matches-list {

  display: grid;

  grid-template-columns:
    repeat(auto-fill, minmax(320px, 1fr));

  gap: 28px;
}

/* =========================
   MATCH CARD
========================= */

.match-card {

  overflow: hidden;

  border-radius: 30px;

  background:
    rgba(255,255,255,0.05);

  border:
    1px solid rgba(255,255,255,0.08);

  transition: all 0.35s ease;
}

.match-card:hover {

  transform:
    translateY(-8px);

  box-shadow:
    0 22px 40px rgba(0,0,0,0.38);
}

.match-image {

  position: relative;

  height: 220px;
}

.match-image img {

  width: 100%;

  height: 100%;

  object-fit: cover;
}

/* =========================
   COMPATIBILITY
========================= */

.compatibility-badge {

  position: absolute;

  top: 16px;
  right: 16px;

  padding: 10px 14px;

  border-radius: 999px;

  background:
    linear-gradient(
      135deg,
      #22c55e,
      #16a34a
    );

  color: white;

  font-weight: 700;

  font-size: 0.82rem;

  box-shadow:
    0 10px 22px rgba(34,197,94,0.3);
}

/* =========================
   MATCH INFO
========================= */

.match-info {

  padding: 24px;
}

.match-info h3 {

  color: white;

  font-size: 1.3rem;

  margin-bottom: 10px;
}

.match-info p {

  color:
    rgba(255,255,255,0.65);

  margin: 5px 0;
}

/* =========================
   ATTRIBUTE LIST
========================= */

.attribute-list {

  display: flex;

  flex-wrap: wrap;

  gap: 8px;

  list-style: none;

  padding: 0;

  margin-top: 12px;
}

.attribute-list li {

  padding: 8px 14px;

  border-radius: 999px;

  background:
    rgba(255,255,255,0.08);

  border:
    1px solid rgba(255,255,255,0.06);

  color: white;

  font-size: 0.75rem;

  backdrop-filter: blur(12px);
}

/* =========================
   VIEW BUTTON
========================= */

.view-btn {

  display: inline-flex;

  margin-top: 18px;

  padding: 12px 18px;

  border-radius: 16px;

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #6d28d9
    );

  color: white;

  text-decoration: none;

  font-weight: 700;

  transition: all 0.3s ease;
}

.view-btn:hover {

  transform:
    translateY(-2px);

  box-shadow:
    0 12px 26px rgba(139,92,246,0.32);
}

/* =========================
   MOBILE
========================= */

@media (max-width: 900px) {

  .profile-details {

    padding:
      120px 18px 60px;
  }

  .profile-body {

    grid-template-columns: 1fr;
  }

  .profile-image {

    height: 500px;
  }

  .info-grid {

    grid-template-columns: 1fr;
  }

  .profile-header {

    flex-direction: column;

    align-items: flex-start;
  }

  .actions {

    width: 100%;
  }

  .action-btn {

    flex: 1;

    justify-content: center;
  }
}
</style>