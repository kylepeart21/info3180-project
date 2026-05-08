<template>
  <div class="container mt-4">
    <!-- SEARCH AND FILTER AREA -->
    <div class="search-filters mb-4">
      <input type="text" class="form-control mb-3" placeholder="Search profiles..." v-model="searchTerm" />
      <div class="filter-buttons">
        <button
          v-for="filter in filters"
          :key="filter"
          @click="selectedFilter = filter"
          :class="['filter-btn', { active: selectedFilter === filter }]"
        >
          {{ filter }}
        </button>
      </div>
    </div>

    <!-- MUTUAL MATCHES -->
    <div v-if="mutualMatches.length" class="section mb-5">
      <h2 class="section-title">Mutual Matches 💚</h2>
      <div class="profiles-grid">
        <div v-for="profile in mutualMatches" :key="'mutual-' + profile.id" class="profile-card-wrapper">
          <div class="profile-card">
            <img :src="profile.photo || '/default-profile.jpg'" alt="" class="bg-img" />
            <div class="overlay">
              <div class="text-block">
                <div class="mutual-indicator">Mutual Match</div>
                <p class="name">{{ profile.name }}</p>
                <p class="parish">{{ profile.parish }}</p>
                <div class="card-btns">
                  <router-link :to="`/profiles/${profile.id}`" class="btn btn-light btn-sm">View</router-link>
                  <router-link :to="`/messages?userId=${profile.user_id_fk}`" class="btn btn-success btn-sm">Message</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- LATEST PROFILES AREA -->
    <h2 class="section-title mt-4">Browse Profiles</h2>

    <div v-if="loading">Loading profiles...</div>
    <div v-else>
      <div v-if="filteredProfiles.length" class="profiles-grid">
        <div v-for="profile in filteredProfiles" :key="profile.id" class="profile-card-wrapper">
          <div class="profile-card">
            <img :src="profile.photo || '/default-profile.jpg'" alt="Profile Image" class="bg-img" />
            <div class="overlay">
              <div class="text-block">
                <p class="name">{{ profile.name }}</p>
                <p class="parish">{{ profile.parish }}</p>
                <div v-if="profile.interests && profile.interests.length" class="interests-preview">
                  <span v-for="interest in profile.interests.slice(0, 2)" :key="interest" class="interest-chip">{{ interest }}</span>
                </div>
                <div class="card-btns">
                  <router-link :to="`/profiles/${profile.id}`" class="btn btn-light btn-sm">View</router-link>
                  <button @click="likeProfile(profile.user_id_fk, profile.id)" class="btn btn-danger btn-sm">♥</button>
                  <button @click="passProfile(profile.user_id_fk, profile.id)" class="btn btn-secondary btn-sm">Pass</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="no-profiles">No profiles found matching your search.</div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import apiClient from '@/http.js'
import { useAuthStore } from '@/store/authentication.js'

const authStore = useAuthStore()
const profiles = ref([])
const mutualMatches = ref([])
const loading = ref(true)
const searchTerm = ref('')
const selectedFilter = ref(null)
const passedIds = ref(new Set())
const likedIds = ref(new Set())

const filters = ['Name', 'Birth', 'Sex', 'Race', 'Parish', 'Interests']

const token = () => localStorage.getItem('jwt')
const headers = () => ({ Authorization: `Bearer ${token()}` })

onMounted(async () => {
  try {
    const [profilesRes, mutualRes] = await Promise.all([
      apiClient.get('/api/profiles', { headers: headers() }),
      apiClient.get('/api/profiles/mutual-matches', { headers: headers() })
    ])
    profiles.value = profilesRes.data.profiles
    mutualMatches.value = mutualRes.data.profiles
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})

const filteredProfiles = computed(() => {
  const term = searchTerm.value.toLowerCase().trim()

  return profiles.value.filter(profile => {
    if (passedIds.value.has(profile.user_id_fk)) return false
    if (!term) return true

    switch (selectedFilter.value) {
      case 'Name':
        return profile.name?.toLowerCase().includes(term)
      case 'Sex':
        return profile.sex?.trim().toLowerCase() === term
      case 'Race':
        return profile.race?.toLowerCase().includes(term)
      case 'Birth':
        return profile.birth_year?.toString().includes(term)
      case 'Parish':
        return profile.parish?.toLowerCase().includes(term)
      case 'Interests':
        return profile.interests?.some(i => i.toLowerCase().includes(term))
      default:
        return (
          profile.name?.toLowerCase().includes(term) ||
          profile.parish?.toLowerCase().includes(term)
        )
    }
  })
})

async function likeProfile(userId, profileId) {
  try {
    await apiClient.post(`/api/profiles/${userId}/favourite`, {}, { headers: headers() })
    likedIds.value.add(userId)
    // Check if now a mutual match
    await refreshMutualMatches()
  } catch (e) {
    if (e.response?.status !== 400) console.error('Error liking profile:', e)
  }
}

async function passProfile(userId, profileId) {
  try {
    await apiClient.post(`/api/profiles/${userId}/pass`, {}, { headers: headers() })
    passedIds.value = new Set([...passedIds.value, userId])
  } catch (e) {
    console.error('Error passing profile:', e)
  }
}

async function refreshMutualMatches() {
  try {
    const res = await apiClient.get('/api/profiles/mutual-matches', { headers: headers() })
    mutualMatches.value = res.data.profiles
  } catch (e) {
    console.error(e)
  }
}
</script>

<style scoped>
/* =========================
   PAGE
========================= */

.container {

  min-height: 100vh;

  padding:
    140px 40px 80px;

  background:
    radial-gradient(
      circle at top left,
      rgba(139,92,246,0.22),
      transparent 25%
    ),

    radial-gradient(
      circle at bottom right,
      rgba(236,72,153,0.16),
      transparent 25%
    ),

    #050816;

  max-width: 1600px;
}

/* =========================
   SEARCH PANEL
========================= */

.search-filters {

  padding: 30px;

  border-radius: 32px;

  background:
    linear-gradient(
      135deg,
      rgba(12,18,32,0.74),
      rgba(18,24,42,0.6)
    );

  backdrop-filter: blur(26px);

  border:
    1px solid rgba(255,255,255,0.08);

  box-shadow:
    0 20px 40px rgba(0,0,0,0.35);

  margin-bottom: 60px;
}

/* =========================
   SEARCH INPUT
========================= */

.form-control {

  height: 64px;

  border-radius: 22px !important;

  border:
    1px solid rgba(255,255,255,0.08) !important;

  background:
    rgba(255,255,255,0.06) !important;

  color: white !important;

  font-size: 1rem;

  padding: 0 22px;

  backdrop-filter: blur(20px);

  transition: all 0.3s ease;
}

.form-control::placeholder {

  color:
    rgba(255,255,255,0.45);
}

.form-control:focus {

  box-shadow:
    0 0 24px rgba(139,92,246,0.25) !important;

  border-color:
    rgba(139,92,246,0.5) !important;
}

/* =========================
   FILTER BUTTONS
========================= */

.filter-buttons {

  display: flex;

  gap: 12px;

  flex-wrap: wrap;
}

.filter-btn {

  background:
    rgba(255,255,255,0.06);

  color:
    rgba(255,255,255,0.82);

  border:
    1px solid rgba(255,255,255,0.08);

  padding: 14px 22px;

  border-radius: 18px;

  font-weight: 600;

  cursor: pointer;

  transition: all 0.3s ease;

  backdrop-filter: blur(18px);
}

.filter-btn:hover {

  transform:
    translateY(-2px);

  background:
    rgba(139,92,246,0.18);

  color: white;
}

.filter-btn.active {

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #6d28d9
    );

  color: white;

  box-shadow:
    0 0 25px rgba(139,92,246,0.35);
}

/* =========================
   SECTION TITLES
========================= */

.section-title {

  font-size: 2rem;

  font-weight: 800;

  color: white;

  margin-bottom: 30px;

  letter-spacing: -0.03em;
}

/* =========================
   PROFILE GRID
========================= */

.profiles-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fill, minmax(340px, 1fr));

  gap: 34px;
}

/* =========================
   PROFILE CARD
========================= */

.profile-card {

  position: relative;

  width: 100%;

  height: 470px;

  border-radius: 34px;

  overflow: hidden;

  background:
    rgba(255,255,255,0.06);

  border:
    1px solid rgba(255,255,255,0.08);

  backdrop-filter: blur(18px);

  box-shadow:
    0 18px 40px rgba(0,0,0,0.38);

  transition: all 0.35s ease;
}

.profile-card:hover {

  transform:
    translateY(-10px);

  box-shadow:
    0 28px 50px rgba(0,0,0,0.45);
}

/* =========================
   PROFILE IMAGE
========================= */

.bg-img {

  width: 100%;

  height: 100%;

  object-fit: cover;

  transition: transform 0.5s ease;
}

.profile-card:hover .bg-img {

  transform: scale(1.05);
}

/* =========================
   OVERLAY
========================= */

.overlay {

  position: absolute;

  inset: 0;

  display: flex;

  align-items: flex-end;

  padding: 26px;

  background:
    linear-gradient(
      to top,
      rgba(0,0,0,0.82),
      rgba(0,0,0,0.15),
      transparent
    );
}

/* =========================
   TEXT
========================= */

.text-block {

  width: 100%;

  text-align: center;

  color: white;
}

.name {

  font-size: 2rem;

  font-weight: 800;

  margin-bottom: 4px;

  letter-spacing: -0.03em;
}

.parish {

  color:
    rgba(255,255,255,0.72);

  margin-bottom: 12px;

  font-size: 1rem;
}

/* =========================
   MUTUAL BADGE
========================= */

.mutual-indicator {

  display: inline-flex;

  align-items: center;

  justify-content: center;

  padding: 8px 16px;

  border-radius: 999px;

  background:
    rgba(34,197,94,0.2);

  border:
    1px solid rgba(34,197,94,0.28);

  backdrop-filter: blur(16px);

  color: white;

  font-size: 0.78rem;

  font-weight: 700;

  margin-bottom: 12px;
}

/* =========================
   INTERESTS
========================= */

.interests-preview {

  display: flex;

  justify-content: center;

  flex-wrap: wrap;

  gap: 8px;

  margin-bottom: 14px;
}

.interest-chip {

  padding: 8px 14px;

  border-radius: 999px;

  background:
    rgba(255,255,255,0.1);

  border:
    1px solid rgba(255,255,255,0.08);

  backdrop-filter: blur(12px);

  font-size: 0.75rem;

  color: white;
}

/* =========================
   BUTTONS
========================= */

.card-btns {

  display: flex;

  justify-content: center;

  gap: 10px;

  margin-top: 10px;

  flex-wrap: wrap;
}

.btn-sm {

  border: none;

  padding: 12px 18px;

  border-radius: 16px;

  font-size: 0.82rem;

  font-weight: 700;

  transition: all 0.28s ease;

  text-decoration: none;
}

.btn-sm:hover {

  transform:
    translateY(-2px);
}

.btn-light {

  background:
    rgba(255,255,255,0.92);

  color: #111827;
}

.btn-danger {

  background:
    linear-gradient(
      135deg,
      #ef4444,
      #dc2626
    );

  color: white;
}

.btn-secondary {

  background:
    rgba(255,255,255,0.12);

  color: white;
}

.btn-success {

  background:
    linear-gradient(
      135deg,
      #22c55e,
      #16a34a
    );

  color: white;
}

/* =========================
   NO PROFILES
========================= */

.no-profiles {

  padding: 70px;

  border-radius: 30px;

  text-align: center;

  color:
    rgba(255,255,255,0.65);

  background:
    rgba(255,255,255,0.04);

  border:
    1px solid rgba(255,255,255,0.06);

  backdrop-filter: blur(18px);
}

/* =========================
   MOBILE
========================= */

@media (max-width: 768px) {

  .container {

    padding:
      120px 18px 60px;
  }

  .profiles-grid {

    grid-template-columns: 1fr;
  }

  .profile-card {

    height: 440px;
  }

  .name {

    font-size: 1.7rem;
  }
}
</style>
