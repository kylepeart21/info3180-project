<template>
  <div class="profile-card" :class="{ expanded }">
    <div class="profile-img">
      <img :src="profile.photo || '/default-profile.jpg'" :alt="profile.name">
      <div v-if="showFavoriteCount" class="favourite-count">❤ {{ profile.favourite_count }}</div>
      <div v-if="isMutualMatch" class="mutual-badge">Mutual Match</div>
    </div>
    <div class="profile-info">
      <h3>{{ profile.name }}</h3>
      <p>Age: {{ calculateAge(profile.birth_year) }}</p>
      <p>{{ profile.sex }}, {{ profile.race }}</p>
      <p v-if="profile.parish">{{ profile.parish }}</p>

      <div v-if="expanded && profile.fav_cuisine" class="additional-info">
        <p><span>Favorite Cuisine:</span> {{ profile.fav_cuisine }}</p>
        <p><span>Favorite Color:</span> {{ profile.fav_colour }}</p>
        <p><span>Favorite School Subject:</span> {{ profile.fav_school_subject }}</p>
      </div>

      <div v-if="profile.interests && profile.interests.length" class="interests-list">
        <span v-for="interest in profile.interests.slice(0, 3)" :key="interest" class="interest-tag">{{ interest }}</span>
      </div>

      <div v-if="expanded && profile.compatibility" class="match-info">
        <p class="compatibility">Compatibility: <span>{{ profile.compatibility }}%</span></p>
      </div>

      <div class="card-actions">
        <router-link :to="`/profiles/${profile.id}`" class="details-btn">
          {{ detailsButtonText }}
        </router-link>

        <div class="action-buttons">
          <button v-if="showPassButton" @click="$emit('pass-profile', profile.user_id_fk)" class="pass-btn" title="Pass">✕</button>
          <heart-button
            :value="isFavourited"
            :profile-id="profile.id"
            @toggle="$emit('toggle-favourite', profile.user_id_fk)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HeartButton from './HeartButton.vue'

export default {
  name: 'ProfileCard',
  components: { HeartButton },
  emits: ['toggle-favourite', 'pass-profile'],
  props: {
    profile: { type: Object, required: true },
    isFavourited: { type: Boolean, default: false },
    isMutualMatch: { type: Boolean, default: false },
    expanded: { type: Boolean, default: false },
    showFavoriteCount: { type: Boolean, default: false },
    showPassButton: { type: Boolean, default: false },
    detailsButtonText: { type: String, default: 'View more details' }
  },
  methods: {
    calculateAge(birthYear) {
      return new Date().getFullYear() - birthYear
    }
  }
}
</script>

<style scoped>
.profile-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.profile-img {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.profile-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.favourite-count {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0,0,0,0.6);
  color: white;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 13px;
}

.mutual-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: #28a745;
  color: white;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.profile-info { padding: 16px; }

.profile-info h3 {
  margin: 0 0 8px;
  font-size: 17px;
  font-weight: 600;
  color: #333;
}

.profile-info p { margin: 3px 0; color: #6c757d; font-size: 14px; }

.additional-info {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.additional-info p span { font-weight: 500; color: #555; }

.interests-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}

.interest-tag {
  background: #e9ecef;
  border-radius: 12px;
  padding: 2px 10px;
  font-size: 12px;
  color: #495057;
}

.match-info { margin-top: 12px; }
.compatibility { font-weight: 500; }
.compatibility span { color: #28a745; font-weight: 600; }

.card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 14px;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.details-btn {
  background: #3498db;
  color: white;
  text-decoration: none;
  padding: 7px 14px;
  border-radius: 5px;
  font-size: 13px;
  font-weight: 500;
  transition: background 0.2s;
}

.details-btn:hover { background: #2980b9; }

.pass-btn {
  background: #e9ecef;
  color: #555;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.pass-btn:hover { background: #f8d7da; color: #dc3545; }
</style>
