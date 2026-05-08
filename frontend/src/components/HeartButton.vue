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

/* =========================
   HEART BUTTON
========================= */

.heart-button {

  position: relative;

  display: inline-flex;

  align-items: center;

  justify-content: center;

  gap: 10px;

  width: 56px;
  height: 56px;

  border-radius: 50%;

  border:
    1px solid rgba(255,255,255,0.10);

  background:
    linear-gradient(
      135deg,
      rgba(255,255,255,0.10),
      rgba(255,255,255,0.04)
    );

  backdrop-filter: blur(18px);

  -webkit-backdrop-filter: blur(18px);

  cursor: pointer;

  color:
    rgba(255,255,255,0.72);

  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease,
    background 0.3s ease,
    color 0.3s ease;

  overflow: hidden;
}

/* =========================
   GLASS SHINE
========================= */

.heart-button::before {

  content: "";

  position: absolute;

  top: -40%;

  left: -60%;

  width: 100%;

  height: 200%;

  background:
    linear-gradient(
      115deg,
      transparent 20%,
      rgba(255,255,255,0.16) 50%,
      transparent 80%
    );

  transform:
    rotate(18deg);

  opacity: 0.6;

  transition:
    transform 0.6s ease;
}

.heart-button:hover::before {

  transform:
    rotate(18deg)
    translateX(35px);
}

/* =========================
   HOVER
========================= */

.heart-button:hover {

  transform:
    translateY(-2px)
    scale(1.06);

  color: white;

  background:
    linear-gradient(
      135deg,
      rgba(255,255,255,0.14),
      rgba(255,255,255,0.06)
    );

  box-shadow:
    0 10px 24px rgba(0,0,0,0.28);
}

/* =========================
   ACTIVE
========================= */

.heart-button.is-active {

  background:
    linear-gradient(
      135deg,
      rgba(255,71,87,0.28),
      rgba(255,71,87,0.16)
    );

  border:
    1px solid rgba(255,71,87,0.24);

  color: #ff6b81;

  box-shadow:
    0 12px 28px rgba(255,71,87,0.28),
    0 0 24px rgba(255,71,87,0.18);
}

/* =========================
   ICON
========================= */

.heart-icon {

  position: relative;

  display: flex;

  align-items: center;

  justify-content: center;

  z-index: 2;
}

.heart-icon svg {

  transition:
    transform 0.3s ease,
    fill 0.3s ease;
}

/* ACTIVE FILL */

.heart-button.is-active .heart-icon svg {

  fill: currentColor;
}

/* =========================
   SIZES
========================= */

.size-small {

  width: 42px;
  height: 42px;
}

.size-small .heart-icon svg {

  width: 18px;
  height: 18px;
}

.size-medium {

  width: 56px;
  height: 56px;
}

.size-medium .heart-icon svg {

  width: 24px;
  height: 24px;
}

.size-large {

  width: 70px;
  height: 70px;
}

.size-large .heart-icon svg {

  width: 32px;
  height: 32px;
}

/* =========================
   LABEL
========================= */

.heart-label {

  font-size: 0.9rem;

  font-weight: 600;

  color: inherit;

  white-space: nowrap;
}

/* =========================
   FOCUS
========================= */

.heart-button:focus {

  outline: none;
}

.heart-button:focus-visible {

  box-shadow:
    0 0 0 3px rgba(139,92,246,0.28),
    0 12px 28px rgba(0,0,0,0.28);
}

/* =========================
   HEART PULSE
========================= */

@keyframes heart-pulse {

  0% {

    transform: scale(1);
  }

  25% {

    transform: scale(1.18);
  }

  50% {

    transform: scale(0.96);
  }

  75% {

    transform: scale(1.08);
  }

  100% {

    transform: scale(1);
  }
}

.heart-button.is-active .heart-icon {

  animation:
    heart-pulse 0.45s ease-out;
}

/* =========================
   MOBILE
========================= */

@media (max-width: 768px) {

  .size-medium {

    width: 52px;
    height: 52px;
  }

  .size-medium .heart-icon svg {

    width: 22px;
    height: 22px;
  }
}
</style>