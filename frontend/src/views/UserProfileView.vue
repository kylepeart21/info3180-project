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
.filter-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-right: 8px;
  margin-bottom: 8px;
}

.filter-btn:hover { background-color: #0056b3; }
.filter-btn.active { background-color: #333; }

.section-title {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #333;
}

.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.profile-card {
  position: relative;
  width: 100%;
  height: 300px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.12);
}

.bg-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(transparent, rgba(0,0,0,0.8));
  padding: 16px 12px 12px;
  color: white;
}

.text-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 4px;
}

.name { font-weight: 700; font-size: 1rem; margin: 0; }
.parish { font-size: 0.82rem; margin: 0; color: #ccc; }

.mutual-indicator {
  background: #28a745;
  color: white;
  border-radius: 12px;
  padding: 2px 10px;
  font-size: 11px;
  font-weight: 600;
  margin-bottom: 4px;
}

.interests-preview {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  justify-content: center;
}

.interest-chip {
  background: rgba(255,255,255,0.2);
  border-radius: 12px;
  padding: 2px 8px;
  font-size: 11px;
}

.card-btns {
  display: flex;
  gap: 6px;
  margin-top: 6px;
  flex-wrap: wrap;
  justify-content: center;
}

.btn-sm {
  padding: 4px 10px;
  font-size: 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}

.btn-light { background: rgba(255,255,255,0.9); color: #333; }
.btn-danger { background: #e74c3c; color: white; }
.btn-secondary { background: rgba(0,0,0,0.5); color: white; }
.btn-success { background: #28a745; color: white; }

.no-profiles {
  text-align: center;
  padding: 40px;
  color: #6c757d;
}
</style>
