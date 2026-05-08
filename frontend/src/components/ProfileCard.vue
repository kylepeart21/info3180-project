<template>
    <div class="profile-card" :class="{ 'expanded': expanded }">
      <div class="profile-img">
        <img :src="profile.image_url || '/default-profile.jpg'" :alt="profile.name">
        <div v-if="showFavoriteCount" class="favourite-count">❤ {{ profile.favourite_count }}</div>
      </div>
      <div class="profile-info">
        <h3>{{ profile.name }}</h3>
        <p>Age: {{ calculateAge(profile.birth_year) }}</p>
        <p>{{ profile.sex }}, {{ profile.race }}</p>
        <p v-if="expanded && profile.parish">Parish: {{ profile.parish }}</p>
        
        <div v-if="expanded && profile.fav_cuisine" class="additional-info">
          <p><span>Favorite Cuisine:</span> {{ profile.fav_cuisine }}</p>
          <p><span>Favorite Color:</span> {{ profile.fav_colour }}</p>
          <p><span>Favorite School Subject:</span> {{ profile.fav_school_subject }}</p>
        </div>
        
        <div v-if="expanded && profile.compatibility" class="match-info">
          <p class="compatibility">Compatibility: <span>{{ profile.compatibility }}%</span></p>
        </div>
        
        <div class="card-actions">
          <router-link :to="`/profiles/${profile.id}`" class="details-btn">
            {{ detailsButtonText }}
          </router-link>
          
          <heart-button 
            :value="isFavourited" 
            :profile-id="profile.id"
            @toggle="$emit('toggle-favourite', profile.id)"
          />
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
    props: {
      profile: {
        type: Object,
        required: true
      },
      isFavourited: {
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
      detailsButtonText: {
        type: String,
        default: 'View more details'
      }
    },
    methods: {
      calculateAge(birthYear) {
        const currentYear = new Date().getFullYear()
        return currentYear - birthYear
      }
    }
  }
  </script>
  
  <style scoped>
  .profile-card {
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: all 0.3s ease;
  }
  
  .profile-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
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
    background-color: rgba(0, 0, 0, 0.6);
    color: white;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  
  .profile-info {
    padding: 20px;
  }
  
  .profile-info h3 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 18px;
    font-weight: 600;
    color: #333;
  }
  
  .profile-info p {
    margin: 5px 0;
    color: #6c757d;
  }
  
  .additional-info {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid #eee;
  }
  
  .additional-info p span {
    font-weight: 500;
    color: #555;
  }
  
  .match-info {
    margin-top: 15px;
  }
  
  .compatibility {
    font-weight: 500;
  }
  
  .compatibility span {
    color: #28a745;
    font-weight: 600;
  }
  
  .card-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;
  }
  
  .details-btn {
    background-color: #3498db;
    color: white;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 5px;
    font-size: 14px;
    font-weight: 500;
    transition: background-color 0.3s;
  }
  
  .details-btn:hover {
    background-color: #2980b9;
  }
  
  .expanded .additional-info {
    display: block;
  }
  </style>