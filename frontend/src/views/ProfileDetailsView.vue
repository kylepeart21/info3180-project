<script>
import HeartButton from '@/components/HeartButton.vue'
import { useAuthStore } from '@/store/authentication.js'
import apiClient from '@/http.js';
import {onMounted} from "vue";
import {useRouter} from "vue-router";


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
      showMatches: false,
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
    async fetchProfileDetails() {
      try {
        const profileId = this.$route.params.profile_id;
        const token = localStorage.getItem('jwt');

        const response = await apiClient.get(`/api/profiles/${profileId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        this.profile = response.data.profile;
        this.loading = false;
      } catch (err) {
        this.error = err.message;
        this.loading = false;
      }
    },
    
    async checkIfFavorited() {
      try {
        const authStore = useAuthStore();
        const token = localStorage.getItem('jwt');

        const response = await apiClient.get(`/api/users/${authStore.user_id}/favourites`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        const favouriteUserIds = response.data.map(u => u.id);
        this.isFavorited = favouriteUserIds.includes(this.profile.user_id_fk);
      } catch (err) {
        console.error('Error checking favorite status:', err);
      }
    },
    
    async checkMutualMatch() {
      try {
        const token = localStorage.getItem('jwt')
        const res = await apiClient.get('/api/profiles/mutual-matches', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        const mutualIds = res.data.profiles.map(p => p.user_id_fk)
        this.isMutualMatch = mutualIds.includes(this.profile.user_id_fk)
      } catch (e) {
        console.error('Error checking mutual match:', e)
      }
    },

    async passProfile() {
      try {
        const token = localStorage.getItem('jwt')
        await apiClient.post(`/api/profiles/${this.profile.user_id_fk}/pass`, {}, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        this.isPassed = true
        this.$toast?.success('Profile passed')
      } catch (e) {
        console.error('Error passing profile:', e)
      }
    },

    async toggleFavorite() {
      try {
        const token = localStorage.getItem('jwt');
        const headers = { 'Authorization': `Bearer ${token}` };

        if (this.isFavorited) {
          await apiClient.delete(`/api/profiles/${this.profile.user_id_fk}/favourite`, { headers });
        } else {
          await apiClient.post(`/api/profiles/${this.profile.user_id_fk}/favourite`, {}, { headers });
        }

        this.isFavorited = !this.isFavorited;
        this.$toast.success(`Profile ${this.isFavorited ? 'added to' : 'removed from'} favorites`);
      } catch (err) {
        console.error('Error toggling favorite:', err);
        this.$toast.error(err.message);
      }
    },
    
    async matchMe() {
      this.showMatches = true;
      this.loadingMatches = true;

      try {
        const profileId = this.$route.params.profile_id;
        const token = localStorage.getItem('jwt');

        const response = await apiClient.get(`/api/profiles/matches/${profileId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        this.matches = response.data.profiles;
        this.loadingMatches = false;
      } catch (err) {
        console.error('Error finding matches:', err);
        this.loadingMatches = false;
        this.$toast.error('Failed to load matches. Please try again.');
      }
    },
    
    calculateAge(birthYear) {
      const currentYear = new Date().getFullYear()
      return currentYear - birthYear
    },
    
    formatHeight(heightInInches) {
      if (!heightInInches) return 'Not specified'
      
      const feet = Math.floor(heightInInches / 12)
      const inches = heightInInches % 12
      return `${feet}'${inches}"`
    },
    
    sendEmail() {
      // This function is a placeholder for the "Email Profile" functionality
      this.$toast.info('Email functionality coming soon!')
    }
  }
}
</script>

<template>
  <div class="profile-details">
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading profile...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <p>{{ error }}</p>
      <button @click="fetchProfileDetails" class="retry-btn">Try Again</button>
    </div>
    
    <div v-else class="profile-container">
      <div class="profile-header">
        <div class="header-left">
          <h1>{{ profile.name }}'s Profile</h1>
          <div v-if="isMutualMatch" class="mutual-badge">Mutual Match 💚</div>
        </div>
        <div class="actions">
          <heart-button
            :value="isFavorited"
            :profile-id="profile.id"
            @toggle="toggleFavorite"
          />
          <button class="action-btn pass-btn" @click="passProfile" :disabled="isPassed">
            {{ isPassed ? 'Passed' : 'Pass' }}
          </button>
          <router-link to="/messages" class="action-btn msg-btn">
            <span class="btn-icon">💬</span>
            Message
          </router-link>
          <button class="action-btn match-btn" @click="matchMe">
            <span class="btn-icon">🔄</span>
            Match Me
          </button>
        </div>
      </div>

      <div class="profile-body">
        <div class="profile-image">
          <img :src="profile.photo || '/default-profile.jpg'" :alt="profile.name">
        </div>
        
        <div class="profile-info">
          <div class="info-section">
            <h2>Personal Information</h2>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">Name:</span>
                <span class="info-value">{{ profile.name }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Age:</span>
                <span class="info-value">{{ calculateAge(profile.birth_year) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Sex:</span>
                <span class="info-value">{{ profile.sex }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Race:</span>
                <span class="info-value">{{ profile.race }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Height:</span>
                <span class="info-value">{{ formatHeight(profile.height) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Parish:</span>
                <span class="info-value">{{ profile.parish || 'Not specified' }}</span>
              </div>
            </div>
          </div>
          
          <div class="info-section">
            <h2>Preferences</h2>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">Favorite Cuisine:</span>
                <span class="info-value">{{ profile.fav_cuisine }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Favorite Color:</span>
                <span class="info-value">{{ profile.fav_colour }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Favorite School Subject:</span>
                <span class="info-value">{{ profile.fav_school_subject }}</span>
              </div>
            </div>
          </div>
          
          <div class="info-section">
            <h2>Values</h2>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">Political:</span>
                <span class="info-value">{{ profile.political ? 'Yes' : 'No' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Religious:</span>
                <span class="info-value">{{ profile.religious ? 'Yes' : 'No' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Family Oriented:</span>
                <span class="info-value">{{ profile.family_oriented ? 'Yes' : 'No' }}</span>
              </div>
            </div>
          </div>
          
          <div v-if="profile.biography" class="info-section">
            <h2>Biography</h2>
            <p class="biography">{{ profile.biography }}</p>
          </div>
        </div>
      </div>
      
      <div v-if="showMatches" class="matches-container">
        <h2>Your Matches</h2>
        <div v-if="loadingMatches" class="loading-matches">
          <div class="spinner"></div>
          <p>Finding matches...</p>
        </div>
        <div v-else-if="matches.length === 0" class="no-matches">
          <p>No matches found. Your perfect match might not be on JamDate yet!</p>
        </div>
        <div v-else class="matches-list">
          <div v-for="match in matches" :key="match.id" class="match-card">
            <div class="match-image">
              <img :src="match.image_url || '/default-profile.jpg'" :alt="match.name">
              <div class="compatibility-badge">{{ match.compatibility }}%</div>
            </div>
            <div class="match-info">
              <h3>{{ match.name }}</h3>
              <p>Age: {{ calculateAge(match.birth_year) }}</p>
              <p>{{ match.sex }}, {{ match.parish }}</p>
              <div class="matching-attributes">
                <p>Matching on:</p>
                <ul class="attribute-list">
                  <li v-if="match.fav_cuisine === profile.fav_cuisine">Cuisine</li>
                  <li v-if="match.fav_colour === profile.fav_colour">Color</li>
                  <li v-if="match.fav_school_subject === profile.fav_school_subject">School Subject</li>
                  <li v-if="match.political === profile.political">Political Views</li>
                  <li v-if="match.religious === profile.religious">Religious Views</li>
                  <li v-if="match.family_oriented === profile.family_oriented">Family Values</li>
                </ul>
              </div>
              <router-link :to="`/profiles/${match.id}`" class="view-btn">View Profile</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-details {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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

.profile-container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.profile-header {
  padding: 20px 30px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.header-left { display: flex; flex-direction: column; gap: 6px; }

.profile-header h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.mutual-badge {
  background: #28a745;
  color: white;
  border-radius: 16px;
  padding: 3px 12px;
  font-size: 13px;
  font-weight: 600;
  display: inline-block;
}

.actions {
  display: flex;
  gap: 15px;
  align-items: center;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 10px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  border: none;
}

.match-btn {
  background-color: #3498db;
  color: white;
  text-decoration: none;
}

.match-btn:hover { background-color: #2980b9; }

.pass-btn {
  background-color: #e9ecef;
  color: #555;
}

.pass-btn:hover:not(:disabled) { background-color: #f8d7da; color: #dc3545; }
.pass-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.msg-btn {
  background-color: #2ecc71;
  color: white;
  text-decoration: none;
}

.msg-btn:hover { background-color: #27ae60; }

.btn-icon {
  font-size: 16px;
}

.profile-body {
  display: flex;
  padding: 30px;
}

.profile-image {
  flex: 0 0 250px;
  margin-right: 30px;
}

.profile-image img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.profile-info {
  flex: 1;
}

.info-section {
  margin-bottom: 25px;
}

.info-section h2 {
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 10px;
  margin-bottom: 15px;
  font-size: 18px;
  color: #333;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-label {
  font-weight: 500;
  color: #6c757d;
  margin-bottom: 3px;
  font-size: 14px;
}

.info-value {
  font-size: 16px;
  color: #333;
}

.biography {
  line-height: 1.6;
  color: #333;
}



.matches-container h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 20px;
  color: #333;
}

.loading-matches {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
}

.no-matches {
  text-align: center;
  padding: 40px;
  background-color: #f8f9fa;
  border-radius: 8px;
  color: #6c757d;
}

.matches-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.match-card {
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.match-card:hover {
  transform: translateY(-5px);
}

.match-image {
  position: relative;
  height: 180px;
}

.match-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.compatibility-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #27ae60;
  color: white;
  padding: 5px 10px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 14px;
}

.match-info {
  padding: 15px;
}

.match-info h3 {
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 18px;
}

.match-info p {
  margin: 5px 0;
  color: #6c757d;
}

.matching-attributes {
  margin-top: 10px;
}

.matching-attributes p {
  font-weight: 500;
  margin-bottom: 5px;
}

.attribute-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.attribute-list li {
  background-color: #e9ecef;
  padding: 3px 8px;
  border-radius: 15px;
  font-size: 12px;
  color: #495057;
}

.view-btn {
  display: inline-block;
  margin-top: 15px;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.view-btn:hover {
  background-color: #2980b9;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .profile-body {
    flex-direction: column;
  }
  
  .profile-image {
    margin-right: 0;
    margin-bottom: 20px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .matches-list {
    grid-template-columns: 1fr;
  }
}
</style>