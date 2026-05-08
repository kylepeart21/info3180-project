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
.favourites-view {
  padding: 30px 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 30px;
  color: #333;
  font-size: 28px;
  font-weight: 600;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  text-align: center;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #3498db;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  font-size: 40px;
  margin-bottom: 20px;
}

.retry-btn {
  margin-top: 20px;
  padding: 8px 16px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #e9ecef;
}

.tab-btn {
  padding: 12px 20px;
  background-color: transparent;
  border: none;
  font-size: 16px;
  font-weight: 500;
  color: #6c757d;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.tab-btn.active {
  color: #3498db;
  border-bottom: 2px solid #3498db;
}

.count-badge {
  display: inline-block;
  margin-left: 8px;
  padding: 2px 8px;
  background-color: #e9ecef;
  border-radius: 20px;
  font-size: 12px;
  color: #495057;
}

.sort-options {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.sort-options span {
  color: #6c757d;
  margin-right: 10px;
}

.sort-btn {
  padding: 6px 12px;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 5px;
  font-size: 14px;
  color: #495057;
  cursor: pointer;
  transition: all 0.2s;
}

.sort-btn.active {
  background-color: #e9ecef;
  border-color: #ced4da;
  font-weight: 500;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  text-align: center;
  background-color: #f8f9fa;
  border-radius: 10px;
}

.empty-icon {
  font-size: 40px;
  margin-bottom: 20px;
}

.empty-state h3 {
  margin-bottom: 10px;
  font-size: 20px;
  color: #495057;
}

.empty-state p {
  margin-bottom: 20px;
  color: #6c757d;
}

.explore-btn {
  padding: 10px 16px;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.explore-btn:hover {
  background-color: #2980b9;
}

.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

@media (max-width: 768px) {
  .tabs {
    flex-direction: column;
    border-bottom: none;
  }
  
  .tab-btn {
    width: 100%;
    text-align: left;
    border-bottom: 1px solid #e9ecef;
  }
  
  .tab-btn.active {
    border-bottom: 1px solid #3498db;
  }
  
  .sort-options {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .sort-options span {
    margin-bottom: 10px;
  }
  
  .profiles-grid {
    grid-template-columns: 1fr;
  }
}
</style>