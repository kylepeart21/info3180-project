<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '@/http.js'
import { useAuthStore } from '@/store/authentication.js'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const isLoading = ref(false)
const loadingProfile = ref(true)
const error = ref(null)
const success = ref(false)
const profileId = ref(null)
const interestInput = ref('')

const parishes = [
  'Kingston', 'St. Andrew', 'St. Catherine', 'Clarendon', 'Manchester',
  'St. Elizabeth', 'Westmoreland', 'Hanover', 'St. James', 'Trelawny',
  'St. Ann', 'St. Mary', 'Portland', 'St. Thomas'
]

const formData = reactive({
  description: '',
  parish: '',
  biography: '',
  sex: '',
  race: '',
  birth_year: null,
  height: null,
  fav_cuisine: '',
  fav_colour: '',
  fav_school_subject: '',
  political: false,
  religious: false,
  family_oriented: false,
  is_public: true,
  interests: []
})

const token = () => localStorage.getItem('jwt')
const headers = () => ({ Authorization: `Bearer ${token()}` })

onMounted(async () => {
  try {
    const res = await apiClient.get(`/api/users/${authStore.user_id}/profile`, { headers: headers() })
    const p = res.data.profile
    profileId.value = p.id
    Object.assign(formData, {
      description: p.description || '',
      parish: p.parish || '',
      biography: p.biography || '',
      sex: p.sex || '',
      race: p.race || '',
      birth_year: p.birth_year,
      height: p.height,
      fav_cuisine: p.fav_cuisine || '',
      fav_colour: p.fav_colour || '',
      fav_school_subject: p.fav_school_subject || '',
      political: p.political || false,
      religious: p.religious || false,
      family_oriented: p.family_oriented || false,
      is_public: p.is_public !== false,
      interests: p.interests || []
    })
  } catch (e) {
    error.value = 'Could not load your profile. Please try again.'
  } finally {
    loadingProfile.value = false
  }
})

function addInterest() {
  const val = interestInput.value.trim()
  if (val && !formData.interests.includes(val)) {
    formData.interests.push(val)
  }
  interestInput.value = ''
}

function removeInterest(interest) {
  formData.interests = formData.interests.filter(i => i !== interest)
}

async function handleSubmit() {
  if (!profileId.value) return
  try {
    isLoading.value = true
    error.value = null
    await apiClient.put(`/api/profiles/${profileId.value}`, formData, { headers: headers() })
    success.value = true
    setTimeout(() => router.push(`/users/${authStore.user_id}`), 1500)
  } catch (e) {
    error.value = e.response?.data?.error || e.message || 'Something went wrong'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="edit-profile">
    <div class="form-container">
      <h1>Edit Your Profile</h1>

      <div v-if="loadingProfile" class="loading-state">Loading your profile...</div>

      <template v-else>
        <div v-if="success" class="alert success">Profile updated! Redirecting...</div>
        <div v-if="error" class="alert error">{{ error }}</div>

        <form @submit.prevent="handleSubmit">
          <div class="grid">
            <div class="form-group">
              <label>Parish</label>
              <select v-model="formData.parish" class="input">
                <option value="">Select Parish</option>
                <option v-for="p in parishes" :key="p" :value="p">{{ p }}</option>
              </select>
            </div>

            <div class="form-group">
              <label>Sex</label>
              <select v-model="formData.sex" class="input">
                <option value="">Select Sex</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div class="form-group">
              <label>Race</label>
              <input type="text" v-model="formData.race" class="input" placeholder="Your race" />
            </div>

            <div class="form-group">
              <label>Birth Year</label>
              <input type="number" v-model="formData.birth_year" class="input" :max="new Date().getFullYear()" min="1900" />
            </div>

            <div class="form-group">
              <label>Height (cm)</label>
              <input type="number" v-model="formData.height" class="input" min="100" max="250" step="0.1" />
            </div>
          </div>

          <div class="form-group full">
            <label>Short Description</label>
            <input type="text" v-model="formData.description" class="input" maxlength="500" placeholder="A brief description about yourself" />
            <span class="char-count">{{ formData.description.length }}/500</span>
          </div>

          <div class="form-group full">
            <label>Biography</label>
            <textarea v-model="formData.biography" class="input" maxlength="1000" placeholder="Tell us more about yourself" rows="4"></textarea>
            <span class="char-count">{{ formData.biography.length }}/1000</span>
          </div>

          <div class="grid">
            <div class="form-group">
              <label>Favorite Cuisine</label>
              <input type="text" v-model="formData.fav_cuisine" class="input" placeholder="e.g., Italian" />
            </div>
            <div class="form-group">
              <label>Favorite Color</label>
              <input type="text" v-model="formData.fav_colour" class="input" placeholder="e.g., Blue" />
            </div>
            <div class="form-group">
              <label>Favorite School Subject</label>
              <input type="text" v-model="formData.fav_school_subject" class="input" placeholder="e.g., Mathematics" />
            </div>
          </div>

          <!-- Interests -->
          <div class="form-group full">
            <label>Interests / Hobbies</label>
            <div class="interests-input-row">
              <input
                type="text"
                v-model="interestInput"
                @keydown.enter.prevent="addInterest"
                class="input"
                placeholder="Type an interest and press Enter"
              />
              <button type="button" @click="addInterest" class="btn-add">Add</button>
            </div>
            <div class="interests-tags" v-if="formData.interests.length">
              <span v-for="interest in formData.interests" :key="interest" class="tag">
                {{ interest }}
                <button type="button" @click="removeInterest(interest)" class="tag-remove">&times;</button>
              </span>
            </div>
          </div>

          <!-- Checkboxes -->
          <div class="checkboxes">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.political" />
              Interested in Politics
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.religious" />
              Religious
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.family_oriented" />
              Family Oriented
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.is_public" />
              Public Profile
            </label>
          </div>

          <div class="form-actions">
            <button type="button" @click="router.back()" class="btn-secondary" :disabled="isLoading">Cancel</button>
            <button type="submit" class="btn-primary" :disabled="isLoading">
              {{ isLoading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </template>
    </div>
  </div>
</template>

<style scoped>
.edit-profile {
  min-height: 100vh;
  padding: 80px 1.5rem 3rem;
  background: #f8f9fa;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.form-container {
  max-width: 760px;
  margin: 0 auto;
  background: #fff;
  border-radius: 10px;
  padding: 2rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

h1 {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #333;
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}

.alert {
  padding: 12px 16px;
  border-radius: 6px;
  margin-bottom: 1rem;
  border-left: 4px solid;
}

.alert.success { background: #e6ffed; border-color: #28a745; color: #2b7a2b; }
.alert.error { background: #ffe6e6; border-color: #dc3545; color: #a71d2a; }

form { display: flex; flex-direction: column; gap: 1.5rem; }

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.form-group { display: flex; flex-direction: column; gap: 4px; }
.form-group.full { grid-column: 1 / -1; }

label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #444;
}

.input {
  padding: 10px 12px;
  font-size: 0.95rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #fefefe;
  transition: border 0.2s;
  width: 100%;
  box-sizing: border-box;
}

.input:focus { border-color: #007bff; outline: none; box-shadow: 0 0 0 3px rgba(0,123,255,0.15); }

textarea.input { min-height: 120px; resize: vertical; }

.char-count { font-size: 0.8rem; color: #888; text-align: right; }

.interests-input-row { display: flex; gap: 8px; }
.interests-input-row .input { flex: 1; }

.btn-add {
  padding: 10px 14px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.interests-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }

.tag {
  background: #e9ecef;
  border-radius: 16px;
  padding: 4px 10px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.tag-remove {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #888;
  line-height: 1;
  padding: 0;
}

.checkboxes { display: flex; flex-wrap: wrap; gap: 1rem; }

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 0.95rem;
}

.form-actions { display: flex; justify-content: flex-end; gap: 1rem; flex-wrap: wrap; }

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover:not(:disabled) { background: #0056b3; }

.btn-secondary {
  background: #e0e0e0;
  color: #333;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

button:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
