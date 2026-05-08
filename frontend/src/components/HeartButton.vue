<script>
export default {
  name: 'HeartButton',
  props: {
    value: {
      type: Boolean,
      required: true
    },
    profileId: {
      type: [String, Number],
      required: true
    },
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    label: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    heartClasses() {
      return {
        'heart-button': true,
        'is-active': this.value,
        [`size-${this.size}`]: true
      }
    },
    ariaLabel() {
      return this.value ? 'Remove from favorites' : 'Add to favorites'
    }
  },
  methods: {
    handleClick() {
      this.$emit('toggle', this.profileId)
    }
  }
}
</script>

<template>
  <button 
    type="button"
    :class="heartClasses"
    @click="handleClick"
    :aria-label="ariaLabel"
    :title="ariaLabel"
  >
    <div class="heart-icon">
      <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
      </svg>
    </div>
    <span v-if="label" class="heart-label">
      {{ value ? 'Favorited' : 'Add to favorites' }}
    </span>
  </button>
</template>

<style scoped>
.heart-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  transition: transform 0.2s ease;
  color: #ccc;
}

.heart-button:hover {
  transform: scale(1.1);
}

.heart-button.is-active {
  color: #ff4757;
}

.heart-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.size-small .heart-icon svg {
  width: 18px;
  height: 18px;
}

.size-medium .heart-icon svg {
  width: 24px;
  height: 24px; 
}

.size-large .heart-icon svg {
  width: 32px;
  height: 32px;
}

.heart-label {
  font-size: 14px;
  font-weight: 500;
  color: inherit;
}

.heart-button.is-active .heart-icon svg {
  fill: currentColor;
}

.heart-button:focus {
  outline: none;
}

.heart-button:focus-visible {
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.5);
  border-radius: 4px;
}

/* Animation for when favorited */
@keyframes heart-pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.heart-button.is-active .heart-icon {
  animation: heart-pulse 0.4s ease-out;
}
</style>