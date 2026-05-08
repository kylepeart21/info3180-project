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
.create-profile {
  background-color: #fff;
  min-height: 100vh;
  padding: 3rem 1.5rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #444;
}

.input,
textarea,
select {
  padding: 10px 14px;
  font-size: 0.95rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: #fefefe;
  transition: border 0.2s ease, box-shadow 0.2s ease;
}

.input:focus,
textarea:focus,
select:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2);
}

textarea {
  min-height: 150px;
  resize: vertical;
}

.checkbox {
  width: 16px;
  height: 16px;
  accent-color: #007bff;
}

.text-sm {
  font-size: 0.85rem;
  color: #666;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #e0e0e0;
  color: #333;
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-secondary:hover {
  background-color: #c2c2c2;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.interests-row {
  display: flex;
  gap: 8px;
}

.interests-row .input { flex: 1; }

.btn-add {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 14px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.interests-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

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

.success,
.error {
  border-left: 5px solid;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.success {
  background-color: #e6ffed;
  border-color: #28a745;
  color: #2b7a2b;
}

.error {
  background-color: #ffe6e6;
  border-color: #dc3545;
  color: #a71d2a;
}

.flex {
  display: flex;
}

.items-center {
  align-items: center;
}

.space-y-4 {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.space-x-4 {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.grid {
  display: grid;
  gap: 1.5rem;
}

.grid-cols-1 {
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .grid-cols-2 {
    grid-template-columns: repeat(2, 1fr);
  }

  .max-w-3xl {
    max-width: 768px;
    margin: 0 auto;
  }
}
</style>