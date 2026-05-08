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

/* =========================
   PAGE
========================= */

.edit-profile {

  min-height: 100vh;

  padding:
    140px 24px 80px;

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

  position: relative;

  overflow: hidden;
}

/* =========================
   CONTAINER
========================= */

.form-container {

  max-width: 920px;

  margin: 0 auto;

  padding: 42px;

  border-radius: 38px;

  background:
    linear-gradient(
      135deg,
      rgba(12,18,32,0.78),
      rgba(18,24,42,0.62)
    );

  backdrop-filter: blur(28px);

  border:
    1px solid rgba(255,255,255,0.08);

  box-shadow:
    0 25px 50px rgba(0,0,0,0.42);
}

/* =========================
   TITLE
========================= */

h1 {

  font-size: 3rem;

  font-weight: 800;

  letter-spacing: -0.04em;

  color: white;

  margin-bottom: 38px;

  text-align: center;
}

/* =========================
   LOADING
========================= */

.loading-state {

  text-align: center;

  padding: 40px;

  color:
    rgba(255,255,255,0.62);

  font-size: 1rem;
}

/* =========================
   ALERTS
========================= */

.alert {

  padding: 18px 20px;

  border-radius: 20px;

  margin-bottom: 24px;

  font-weight: 600;

  backdrop-filter: blur(16px);
}

.alert.success {

  background:
    rgba(34,197,94,0.16);

  border:
    1px solid rgba(34,197,94,0.22);

  color: #bbf7d0;
}

.alert.error {

  background:
    rgba(239,68,68,0.16);

  border:
    1px solid rgba(239,68,68,0.22);

  color: #fecaca;
}

/* =========================
   FORM
========================= */

form {

  display: flex;

  flex-direction: column;

  gap: 30px;
}

/* =========================
   GRID
========================= */

.grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(240px, 1fr));

  gap: 22px;
}

/* =========================
   FORM GROUP
========================= */

.form-group {

  display: flex;

  flex-direction: column;

  gap: 10px;
}

.form-group.full {

  grid-column: 1 / -1;
}

/* =========================
   LABELS
========================= */

label {

  color:
    rgba(255,255,255,0.82);

  font-size: 0.92rem;

  font-weight: 700;

  letter-spacing: 0.01em;
}

/* =========================
   INPUTS
========================= */

.input {

  width: 100%;

  min-height: 58px;

  padding: 0 18px;

  border-radius: 20px;

  border:
    1px solid rgba(255,255,255,0.08);

  background:
    rgba(255,255,255,0.06);

  color: white;

  font-size: 0.96rem;

  outline: none;

  transition: all 0.3s ease;

  backdrop-filter: blur(18px);

  box-sizing: border-box;
}

.input::placeholder {

  color:
    rgba(255,255,255,0.42);
}

/* FOCUS */

.input:focus {

  border-color:
    rgba(139,92,246,0.5);

  box-shadow:
    0 0 24px rgba(139,92,246,0.22);
}

/* =========================
   TEXTAREA
========================= */

textarea.input {

  min-height: 160px;

  padding-top: 18px;

  resize: vertical;
}

/* =========================
   SELECT
========================= */

select.input {

  appearance: none;
}

/* =========================
   CHARACTER COUNT
========================= */

.char-count {

  text-align: right;

  font-size: 0.78rem;

  color:
    rgba(255,255,255,0.42);
}

/* =========================
   INTERESTS
========================= */

.interests-input-row {

  display: flex;

  gap: 12px;
}

.interests-input-row .input {

  flex: 1;
}

/* =========================
   ADD BUTTON
========================= */

.btn-add {

  min-width: 120px;

  border: none;

  border-radius: 20px;

  background:
    linear-gradient(
      135deg,
      #22c55e,
      #16a34a
    );

  color: white;

  font-weight: 700;

  cursor: pointer;

  transition: all 0.3s ease;

  box-shadow:
    0 10px 24px rgba(34,197,94,0.28);
}

.btn-add:hover {

  transform:
    translateY(-2px);

  box-shadow:
    0 14px 28px rgba(34,197,94,0.36);
}

/* =========================
   TAGS
========================= */

.interests-tags {

  display: flex;

  flex-wrap: wrap;

  gap: 12px;

  margin-top: 16px;
}

.tag {

  display: flex;

  align-items: center;

  gap: 8px;

  padding: 10px 16px;

  border-radius: 999px;

  background:
    rgba(255,255,255,0.08);

  border:
    1px solid rgba(255,255,255,0.08);

  backdrop-filter: blur(12px);

  color: white;

  font-size: 0.82rem;

  font-weight: 600;
}

/* REMOVE */

.tag-remove {

  background: none;

  border: none;

  color:
    rgba(255,255,255,0.58);

  cursor: pointer;

  font-size: 1rem;

  transition: all 0.2s ease;
}

.tag-remove:hover {

  color: #f87171;
}

/* =========================
   CHECKBOXES
========================= */

.checkboxes {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(220px, 1fr));

  gap: 16px;
}

.checkbox-label {

  display: flex;

  align-items: center;

  gap: 12px;

  padding: 18px;

  border-radius: 22px;

  background:
    rgba(255,255,255,0.05);

  border:
    1px solid rgba(255,255,255,0.06);

  backdrop-filter: blur(16px);

  color:
    rgba(255,255,255,0.78);

  cursor: pointer;

  transition: all 0.3s ease;
}

.checkbox-label:hover {

  background:
    rgba(255,255,255,0.08);
}

.checkbox-label input {

  width: 18px;
  height: 18px;
}

/* =========================
   ACTIONS
========================= */

.form-actions {

  display: flex;

  justify-content: flex-end;

  gap: 16px;

  margin-top: 10px;

  flex-wrap: wrap;
}

/* =========================
   PRIMARY BUTTON
========================= */

.btn-primary {

  border: none;

  padding: 16px 28px;

  border-radius: 22px;

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

  box-shadow:
    0 12px 28px rgba(139,92,246,0.3);
}

.btn-primary:hover:not(:disabled) {

  transform:
    translateY(-2px);

  box-shadow:
    0 16px 34px rgba(139,92,246,0.4);
}

/* =========================
   SECONDARY BUTTON
========================= */

.btn-secondary {

  border: none;

  padding: 16px 28px;

  border-radius: 22px;

  background:
    rgba(255,255,255,0.08);

  border:
    1px solid rgba(255,255,255,0.08);

  color: white;

  font-weight: 700;

  cursor: pointer;

  transition: all 0.3s ease;

  backdrop-filter: blur(16px);
}

.btn-secondary:hover {

  background:
    rgba(255,255,255,0.12);

  transform:
    translateY(-2px);
}

/* =========================
   DISABLED
========================= */

button:disabled {

  opacity: 0.5;

  cursor: not-allowed;
}

/* =========================
   MOBILE
========================= */

@media (max-width: 768px) {

  .edit-profile {

    padding:
      120px 16px 60px;
  }

  .form-container {

    padding: 30px 22px;
  }

  h1 {

    font-size: 2.2rem;
  }

  .grid {

    grid-template-columns: 1fr;
  }

  .interests-input-row {

    flex-direction: column;
  }

  .btn-add {

    width: 100%;

    min-height: 56px;
  }

  .form-actions {

    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {

    width: 100%;
  }
}
</style>
