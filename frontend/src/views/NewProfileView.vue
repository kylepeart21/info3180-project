<script setup>
import {ref, reactive, onMounted} from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/http.js';
import { useAuthStore} from '@/store/authentication.js';

const router = useRouter()
const isLoading = ref(false)
const error = ref(null)
const success = ref(false)
const authStore = useAuthStore();

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
  interests: []
})

const interestInput = ref('')

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

const validateForm = () => {
  const requiredFields = [
    'description', 'parish', 'biography', 'sex', 'race', 'birth_year',
    'height', 'fav_cuisine', 'fav_colour', 'fav_school_subject'
  ]

  return requiredFields.every(field => {
    const value = formData[field]
    return value !== null && value !== ''
  })
}

const handleSubmit = async () => {
  try {
    if (!validateForm()) {
      error.value = 'Please fill in all required fields'
      return
    }

    isLoading.value = true
    error.value = null

    const token = localStorage.getItem('jwt')
    if (!token) {
      throw new Error('Authentication required')
    }

    const response = await apiClient.post('/api/profiles', formData, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    // If request is successful
    success.value = true
    setTimeout(() => {
      router.push('/users/' + authStore.user_id);
    }, 2000)

  } catch (err) {
    error.value = err.response?.data?.error || err.message || 'Something went wrong'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="create-profile">
    <div class="max-w-3xl mx-auto p-6">
      <h1 class="text-3xl font-bold mb-8">Create Your Profile</h1>

      <div v-if="success" class="bg-green-50 border-l-4 border-green-500 p-4 mb-6">
        <p class="text-green-700">Profile created successfully! Redirecting...</p>
      </div>

      <div v-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Basic Information -->
          <div class="form-group">
            <label class="label">Parish*</label>
            <select v-model="formData.parish" class="input">
              <option value="">Select Parish</option>
              <option v-for="parish in parishes" :key="parish" :value="parish">
                {{ parish }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label class="label">Sex*</label>
            <select v-model="formData.sex" class="input">
              <option value="">Select Sex</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div class="form-group">
            <label class="label">Race*</label>
            <input type="text" v-model="formData.race" class="input" placeholder="Your race">
          </div>

          <div class="form-group">
            <label class="label">Birth Year*</label>
            <input
              type="number"
              v-model="formData.birth_year"
              class="input"
              :max="new Date().getFullYear()"
              min="1900"
            >
          </div>

          <div class="form-group">
            <label class="label">Height (cm)*</label>
            <input
              type="number"
              v-model="formData.height"
              class="input"
              min="100"
              max="250"
              step="0.1"
            >
          </div>
        </div>

        <!-- Description and Biography -->
        <div class="space-y-6">
          <div class="form-group">
            <label class="label">Short Description*</label>
            <input
              type="text"
              v-model="formData.description"
              class="input"
              maxlength="500"
              placeholder="A brief description about yourself"
            >
            <span class="text-sm text-gray-500">
              {{ formData.description.length }}/500 characters
            </span>
          </div>

          <div class="form-group">
            <label class="label">Biography*</label>
            <textarea
              v-model="formData.biography"
              class="input min-h-[150px]"
              maxlength="1000"
              placeholder="Tell us more about yourself"
            ></textarea>
            <span class="text-sm text-gray-500">
              {{ formData.biography.length }}/1000 characters
            </span>
          </div>
        </div>

        <!-- Favorites -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="form-group">
            <label class="label">Favorite Cuisine*</label>
            <input type="text" v-model="formData.fav_cuisine" class="input" placeholder="e.g., Italian">
          </div>

          <div class="form-group">
            <label class="label">Favorite Color*</label>
            <input type="text" v-model="formData.fav_colour" class="input" placeholder="e.g., Blue">
          </div>

          <div class="form-group">
            <label class="label">Favorite School Subject*</label>
            <input type="text" v-model="formData.fav_school_subject" class="input" placeholder="e.g., Mathematics">
          </div>
        </div>

        <!-- Interests -->
        <div class="form-group">
          <label class="label">Interests / Hobbies (min 3)</label>
          <div class="interests-row">
            <input
              type="text"
              v-model="interestInput"
              @keydown.enter.prevent="addInterest"
              class="input"
              placeholder="Type an interest and press Enter or click Add"
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
        <div class="space-y-4">
          <div class="flex items-center">
            <input type="checkbox" v-model="formData.political" class="checkbox">
            <label class="ml-2">Interested in Politics</label>
          </div>

          <div class="flex items-center">
            <input type="checkbox" v-model="formData.religious" class="checkbox">
            <label class="ml-2">Religious</label>
          </div>

          <div class="flex items-center">
            <input type="checkbox" v-model="formData.family_oriented" class="checkbox">
            <label class="ml-2">Family Oriented</label>
          </div>
        </div>

        <div class="flex justify-end space-x-4" style="margin-top: 1rem">
          <button
            type="button"
            @click="router.back()"
            class="btn-secondary"
            :disabled="isLoading"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn-primary"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Creating Profile...' : 'Create Profile' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>

/* =========================
   PAGE
========================= */

.create-profile {

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

  color: white;

  overflow: hidden;
}

/* =========================
   CONTAINER
========================= */

.max-w-3xl {

  max-width: 920px !important;

  margin: 0 auto;

  padding: 42px !important;

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

  text-align: center;

  margin-bottom: 42px;

  color: white;
}

/* =========================
   ALERTS
========================= */

.success,
.error {

  padding: 18px 20px;

  border-radius: 20px;

  margin-bottom: 24px;

  font-weight: 600;

  backdrop-filter: blur(16px);
}

.success {

  background:
    rgba(34,197,94,0.16);

  border:
    1px solid rgba(34,197,94,0.22);

  color: #bbf7d0;
}

.error {

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

  gap: 22px;
}

.grid-cols-1 {

  grid-template-columns: 1fr;
}

@media (min-width: 768px) {

  .grid-cols-2 {

    grid-template-columns:
      repeat(2, 1fr);
  }
}

/* =========================
   FORM GROUP
========================= */

.form-group {

  display: flex;

  flex-direction: column;

  gap: 10px;
}

/* =========================
   LABELS
========================= */

.label {

  color:
    rgba(255,255,255,0.82);

  font-size: 0.92rem;

  font-weight: 700;

  letter-spacing: 0.01em;
}

/* =========================
   INPUTS
========================= */

.input,
textarea,
select {

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

/* PLACEHOLDER */

.input::placeholder,
textarea::placeholder {

  color:
    rgba(255,255,255,0.42);
}

/* FOCUS */

.input:focus,
textarea:focus,
select:focus {

  border-color:
    rgba(139,92,246,0.5);

  box-shadow:
    0 0 24px rgba(139,92,246,0.22);
}

/* =========================
   TEXTAREA
========================= */

textarea {

  min-height: 170px;

  padding-top: 18px;

  resize: vertical;
}

/* =========================
   SMALL TEXT
========================= */

.text-sm {

  text-align: right;

  font-size: 0.78rem;

  color:
    rgba(255,255,255,0.42);
}

/* =========================
   INTERESTS
========================= */

.interests-row {

  display: flex;

  gap: 12px;
}

.interests-row .input {

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

.space-y-4 {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(220px, 1fr));

  gap: 16px;
}

.flex.items-center {

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

  transition: all 0.3s ease;
}

.flex.items-center:hover {

  background:
    rgba(255,255,255,0.08);
}

/* CHECKBOX */

.checkbox {

  width: 18px;
  height: 18px;

  accent-color: #8b5cf6;
}

/* =========================
   ACTIONS
========================= */

.space-x-4 {

  display: flex;

  justify-content: flex-end;

  gap: 16px;

  margin-top: 12px;

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

  .create-profile {

    padding:
      120px 16px 60px;
  }

  .max-w-3xl {

    padding: 30px 22px !important;
  }

  h1 {

    font-size: 2.2rem;
  }

  .interests-row {

    flex-direction: column;
  }

  .btn-add {

    width: 100%;

    min-height: 56px;
  }

  .space-x-4 {

    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {

    width: 100%;
  }
}
</style>