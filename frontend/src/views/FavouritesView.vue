<script>
import ProfileCard from '@/components/ProfileCard.vue'
import apiClient from '@/http.js';
import {onMounted} from "vue";
import { useAuthStore} from "@/store/authentication.js";
import {useRouter} from "vue-router";

export default {
  name: 'FavouritesView',
  components: {
    ProfileCard
  },
  data() {
    return {
      activeTab: 'myFavourites',
      myFavourites: [],
      topFavourites: [],
      loading: true,
      error: null,
      sortBy: 'name',
      sortOrder: 'asc'
    }
  },
  computed: {
    sortedMyFavourites() {
      return [...this.myFavourites].sort((a, b) => {
        let aValue, bValue;
        
        if (this.sortBy === 'name') {
          aValue = a.name.toLowerCase();
          bValue = b.name.toLowerCase();
        } else if (this.sortBy === 'parish') {
          aValue = (a.parish || '').toLowerCase();
          bValue = (b.parish || '').toLowerCase();
        } else if (this.sortBy === 'age') {
          aValue = this.calculateAge(a.birth_year);
          bValue = this.calculateAge(b.birth_year);
        }
        
        if (this.sortOrder === 'asc') {
          return aValue > bValue ? 1 : -1;
        } else {
          return aValue < bValue ? 1 : -1;
        }
      });
    },
    
    sortedTopFavourites() {
      return [...this.topFavourites].sort((a, b) => {
        if (this.sortBy === 'favourites') {
          return this.sortOrder === 'asc' 
            ? a.favourite_count - b.favourite_count 
            : b.favourite_count - a.favourite_count;
        } else {
          let aValue, bValue;
          
          if (this.sortBy === 'name') {
            aValue = a.name.toLowerCase();
            bValue = b.name.toLowerCase();
          } else if (this.sortBy === 'parish') {
            aValue = (a.parish || '').toLowerCase();
            bValue = (b.parish || '').toLowerCase();
          } else if (this.sortBy === 'age') {
            aValue = this.calculateAge(a.birth_year);
            bValue = this.calculateAge(b.birth_year);
          }
          
          if (this.sortOrder === 'asc') {
            return aValue > bValue ? 1 : -1;
          } else {
            return aValue < bValue ? 1 : -1;
          }
        }
      });
    }
  },
  created() {
    this.fetchFavourites()
  },
  methods: {
    async fetchFavourites() {
      try {
        this.loading = true;
        const authStore = useAuthStore();
        const token = localStorage.getItem('jwt');
        const headers = { 'Authorization': `Bearer ${token}` };

        const myFavResponse = await apiClient.get(`/api/users/${authStore.user_id}/favourites`, { headers });
        this.myFavourites = myFavResponse.data;

        const topFavResponse = await apiClient.get('/api/users/favourites/10', { headers });
        this.topFavourites = topFavResponse.data;

        this.loading = false;
      } catch (err) {
        this.error = err.message;
        this.loading = false;
      }
    },
    
    async removeFromFavourites(profileId) {
      try {
        const token = localStorage.getItem('jwt');
        await apiClient.delete(`/api/profiles/${profileId}/favourite`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        this.myFavourites = this.myFavourites.filter(profile => profile.id !== profileId);
        const topIndex = this.topFavourites.findIndex(p => p.id === profileId);
        if (topIndex !== -1) {
          this.topFavourites[topIndex].favourite_count -= 1;
          this.topFavourites[topIndex].is_favourited = false;
        }
      } catch (err) {
        console.error('Error removing from favourites:', err);
      }
    },
    
    async addToFavourites(profileId) {
      try {
        const token = localStorage.getItem('jwt');
        await apiClient.post(`/api/profiles/${profileId}/favourite`, {}, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const profileData = this.topFavourites.find(p => p.id === profileId);
        if (!this.myFavourites.some(p => p.id === profileId) && profileData) {
          this.myFavourites.push(profileData);
        }
        const topIndex = this.topFavourites.findIndex(p => p.id === profileId);
        if (topIndex !== -1) {
          this.topFavourites[topIndex].favourite_count += 1;
          this.topFavourites[topIndex].is_favourited = true;
        }
      } catch (err) {
        console.error('Error adding to favourites:', err);
      }
    },
    
    handleToggleFavourite(profileId) {
      // Check if profile is already in user's favourites
      const isFavourited = this.myFavourites.some(p => p.id === profileId)
      
      if (isFavourited) {
        this.removeFromFavourites(profileId)
      }
      else {
        this.addToFavourites(profileId)
      }
    },
    
    calculateAge(birthYear) {
      const currentYear = new Date().getFullYear()
      return currentYear - birthYear
    },
    
    changeSortOption(option) {
      if (this.sortBy === option) {
        // Toggle sort order if clicking the same option
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortBy = option
        // Reset to ascending order when changing sort option
        this.sortOrder = 'asc'
      }
    },
    
    getSortIcon(option) {
      if (this.sortBy !== option) return ''
      return this.sortOrder === 'asc' ? '↑' : '↓'
    }
  }
}
</script>

<template>
  <div class="favourites-view">
    <div class="container">
      <h1>Favourites</h1>
      
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>Loading favourites...</p>
      </div>
      
      <div v-else-if="error" class="error-container">
        <div class="error-icon">⚠️</div>
        <p>{{ error }}</p>
        <button @click="fetchFavourites" class="retry-btn">Try Again</button>
      </div>
      
      <div v-else class="favourites-content">
        <div class="tabs">
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'myFavourites' }"
            @click="activeTab = 'myFavourites'"
          >
            My Favourites
            <span class="count-badge">{{ myFavourites.length }}</span>
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'topFavourites' }"
            @click="activeTab = 'topFavourites'"
          >
            Popular Profiles
            <span class="count-badge">{{ topFavourites.length }}</span>
          </button>
        </div>
        
        <div class="sort-options">
          <span>Sort by:</span>
          <button 
            class="sort-btn" 
            :class="{ active: sortBy === 'name' }"
            @click="changeSortOption('name')"
          >
            Name {{ getSortIcon('name') }}
          </button>
          <button 
            class="sort-btn" 
            :class="{ active: sortBy === 'age' }"
            @click="changeSortOption('age')"
          >
            Age {{ getSortIcon('age') }}
          </button>
          <button 
            class="sort-btn" 
            :class="{ active: sortBy === 'parish' }"
            @click="changeSortOption('parish')"
          >
            Parish {{ getSortIcon('parish') }}
          </button>
          <button 
            v-if="activeTab === 'topFavourites'"
            class="sort-btn" 
            :class="{ active: sortBy === 'favourites' }"
            @click="changeSortOption('favourites')"
          >
            Favourites {{ getSortIcon('favourites') }}
          </button>
        </div>
        
        <div v-if="activeTab === 'myFavourites'">
          <div v-if="myFavourites.length === 0" class="empty-state">
            <div class="empty-icon">💔</div>
            <h3>No Favourites Yet</h3>
            <p>Start exploring profiles and add some to your favourites!</p>
            <router-link to="/profiles" class="explore-btn">Explore Profiles</router-link>
          </div>
          
          <div v-else class="profiles-grid">
            <profile-card
              v-for="profile in sortedMyFavourites"
              :key="profile.id"
              :profile="profile"
              :is-favourited="true"
              :expanded="false"
              details-button-text="View Profile"
              @toggle-favourite="handleToggleFavourite"
            />
          </div>
        </div>
        
        <div v-if="activeTab === 'topFavourites'">
          <div v-if="topFavourites.length === 0" class="empty-state">
            <div class="empty-icon">🔍</div>
            <h3>No Popular Profiles</h3>
            <p>Be the first to favourite some profiles!</p>
            <router-link to="/profiles" class="explore-btn">Explore Profiles</router-link>
          </div>
          
          <div v-else class="profiles-grid">
            <profile-card
              v-for="profile in sortedTopFavourites"
              :key="profile.id"
              :profile="profile"
              :is-favourited="profile.is_favourited"
              :expanded="false"
              :show-favorite-count="true"
              details-button-text="View Profile"
              @toggle-favourite="handleToggleFavourite"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

/* =========================
   PAGE
========================= */

.favourites-view {

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
}

/* =========================
   CONTAINER
========================= */

.container {

  max-width: 1600px;

  margin: 0 auto;
}

/* =========================
   TITLE
========================= */

h1 {

  margin-bottom: 40px;

  color: white;

  font-size: 3rem;

  font-weight: 800;

  letter-spacing: -0.04em;
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

  text-align: center;

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
   RETRY BUTTON
========================= */

.retry-btn {

  margin-top: 22px;

  padding: 14px 20px;

  border: none;

  border-radius: 18px;

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #6d28d9
    );

  color: white;

  font-weight: 700;

  cursor: pointer;

  transition: all 0.3s ease;
}

.retry-btn:hover {

  transform:
    translateY(-2px);

  box-shadow:
    0 12px 24px rgba(139,92,246,0.28);
}

/* =========================
   MAIN CONTENT
========================= */

.favourites-content {

  padding: 34px;

  border-radius: 36px;

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
   TABS
========================= */

.tabs {

  display: flex;

  gap: 16px;

  margin-bottom: 30px;

  flex-wrap: wrap;
}

.tab-btn {

  display: flex;

  align-items: center;

  gap: 10px;

  padding: 16px 24px;

  border: none;

  border-radius: 22px;

  background:
    rgba(255,255,255,0.06);

  border:
    1px solid rgba(255,255,255,0.08);

  color:
    rgba(255,255,255,0.72);

  font-size: 0.95rem;

  font-weight: 700;

  cursor: pointer;

  transition: all 0.3s ease;

  backdrop-filter: blur(18px);
}

.tab-btn:hover {

  transform:
    translateY(-2px);

  background:
    rgba(255,255,255,0.08);

  color: white;
}

.tab-btn.active {

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #6d28d9
    );

  color: white;

  box-shadow:
    0 12px 28px rgba(139,92,246,0.28);
}

/* =========================
   BADGE
========================= */

.count-badge {

  padding: 5px 10px;

  border-radius: 999px;

  background:
    rgba(255,255,255,0.14);

  font-size: 0.75rem;

  font-weight: 700;
}

/* =========================
   SORT OPTIONS
========================= */

.sort-options {

  display: flex;

  align-items: center;

  flex-wrap: wrap;

  gap: 14px;

  margin-bottom: 36px;
}

.sort-options span {

  color:
    rgba(255,255,255,0.55);

  font-weight: 600;
}

.sort-btn {

  padding: 12px 18px;

  border-radius: 18px;

  border:
    1px solid rgba(255,255,255,0.08);

  background:
    rgba(255,255,255,0.06);

  color:
    rgba(255,255,255,0.72);

  cursor: pointer;

  font-weight: 600;

  transition: all 0.3s ease;

  backdrop-filter: blur(14px);
}

.sort-btn:hover {

  transform:
    translateY(-2px);

  background:
    rgba(255,255,255,0.08);

  color: white;
}

.sort-btn.active {

  background:
    rgba(139,92,246,0.18);

  border:
    1px solid rgba(139,92,246,0.28);

  color: white;
}

/* =========================
   EMPTY STATE
========================= */

.empty-state {

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  text-align: center;

  padding: 90px 40px;

  border-radius: 34px;

  background:
    rgba(255,255,255,0.04);

  border:
    1px solid rgba(255,255,255,0.06);

  backdrop-filter: blur(20px);
}

.empty-icon {

  font-size: 5rem;

  margin-bottom: 24px;
}

.empty-state h3 {

  color: white;

  font-size: 2rem;

  margin-bottom: 12px;
}

.empty-state p {

  color:
    rgba(255,255,255,0.62);

  margin-bottom: 28px;

  max-width: 480px;

  line-height: 1.7;
}

/* =========================
   EXPLORE BUTTON
========================= */

.explore-btn {

  display: inline-flex;

  align-items: center;

  justify-content: center;

  padding: 16px 26px;

  border-radius: 20px;

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

  box-shadow:
    0 12px 28px rgba(139,92,246,0.28);
}

.explore-btn:hover {

  transform:
    translateY(-2px);

  box-shadow:
    0 16px 32px rgba(139,92,246,0.36);
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
   MOBILE
========================= */

@media (max-width: 768px) {

  .favourites-view {

    padding:
      120px 18px 60px;
  }

  h1 {

    font-size: 2.3rem;
  }

  .tabs {

    flex-direction: column;
  }

  .tab-btn {

    width: 100%;

    justify-content: center;
  }

  .sort-options {

    flex-direction: column;

    align-items: flex-start;
  }

  .profiles-grid {

    grid-template-columns: 1fr;
  }
}
</style>