<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '@/http.js'
import { useAuthStore } from '@/store/authentication.js'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const currentUserId = computed(() => parseInt(authStore.user_id))

const conversations = ref([])
const selectedUser = ref(null)
const messages = ref([])
const newMessage = ref('')
const loadingConversations = ref(true)
const loadingMessages = ref(false)
const sending = ref(false)
const messagesList = ref(null)
let pollInterval = null

const headers = () => ({ Authorization: `Bearer ${localStorage.getItem('jwt')}` })

async function fetchConversations() {
  try {
    const res = await apiClient.get('/api/messages/conversations', { headers: headers() })
    conversations.value = res.data.conversations
  } catch (e) {
    console.error('Error loading conversations:', e)
  } finally {
    loadingConversations.value = false
  }
}

async function selectConversation(user) {
  selectedUser.value = user
  loadingMessages.value = true
  await loadMessages()
  loadingMessages.value = false
}

async function loadMessages() {
  if (!selectedUser.value) return
  try {
    const res = await apiClient.get(`/api/messages/${selectedUser.value.id}`, { headers: headers() })
    messages.value = res.data.messages
    await nextTick()
    scrollToBottom()
  } catch (e) {
    console.error('Error loading messages:', e)
  }
}

async function sendMessage() {
  const content = newMessage.value.trim()
  if (!content || sending.value) return

  sending.value = true
  try {
    const res = await apiClient.post('/api/messages', {
      receiver_id: selectedUser.value.id,
      content
    }, { headers: headers() })

    messages.value.push(res.data.data)
    newMessage.value = ''
    await nextTick()
    scrollToBottom()

    // Update conversation preview
    const conv = conversations.value.find(c => c.user.id === selectedUser.value.id)
    if (conv) conv.last_message = res.data.data
    else await fetchConversations()
  } catch (e) {
    console.error('Error sending message:', e)
  } finally {
    sending.value = false
  }
}

function scrollToBottom() {
  if (messagesList.value) {
    messagesList.value.scrollTop = messagesList.value.scrollHeight
  }
}

function formatTime(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  const now = new Date()
  const isToday = d.toDateString() === now.toDateString()
  if (isToday) return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  return d.toLocaleDateString([], { month: 'short', day: 'numeric' })
}

function formatMessageTime(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function truncate(text, len) {
  if (!text) return 'Start a conversation'
  return text.length > len ? text.slice(0, len) + '...' : text
}

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

// Watch ?userId query param — fires immediately on mount AND on URL changes
watch(
  () => route.query.userId,
  async (userId) => {
    if (!userId) return
    const targetId = parseInt(userId)
    if (isNaN(targetId)) return

    // If already in conversation list, select it
    const existing = conversations.value.find(c => c.user.id === targetId)
    if (existing) {
      await selectConversation(existing.user)
      return
    }

    // No prior conversation — fetch user and open a blank chat
    try {
      const res = await apiClient.get(`/api/users/${targetId}`, { headers: headers() })
      selectedUser.value = res.data.user
      messages.value = []
      loadingMessages.value = false
    } catch (e) {
      console.error('Could not open chat:', e)
    }
  },
  { immediate: true }
)

onMounted(async () => {
  await fetchConversations()

  // After conversations load, re-check userId in case it was missed before
  if (route.query.userId && !selectedUser.value) {
    const targetId = parseInt(route.query.userId)
    const existing = conversations.value.find(c => c.user.id === targetId)
    if (existing) {
      await selectConversation(existing.user)
    } else {
      try {
        const res = await apiClient.get(`/api/users/${targetId}`, { headers: headers() })
        selectedUser.value = res.data.user
        messages.value = []
        loadingMessages.value = false
      } catch (e) {
        console.error('Could not open chat:', e)
      }
    }
  }

  pollInterval = setInterval(async () => {
    await fetchConversations()
    if (selectedUser.value) await loadMessages()
  }, 5000)
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<template>
  <div class="messages-view" :class="{ 'chat-open': selectedUser }">
    <!-- Conversation list -->
    <div class="conversations-panel">
      <div class="panel-header">
        <h3>Messages</h3>
      </div>

      <div v-if="loadingConversations" class="panel-loading">Loading...</div>

      <div v-else-if="conversations.length === 0" class="panel-empty">
        <p>No conversations yet.</p>
        <p>Match with someone and start chatting!</p>
      </div>

      <div
        v-for="conv in conversations"
        :key="conv.user.id"
        class="conv-item"
        :class="{ active: selectedUser?.id === conv.user.id }"
        @click="selectConversation(conv.user)"
      >
        <img :src="conv.user.photo || '/default-profile.jpg'" :alt="conv.user.name" class="conv-avatar" />
        <div class="conv-info">
          <div class="conv-name">{{ conv.user.name }}</div>
          <div class="conv-preview">{{ truncate(conv.last_message?.content, 38) }}</div>
        </div>
        <div class="conv-time">{{ formatTime(conv.last_message?.timestamp) }}</div>
      </div>
    </div>

    <!-- Chat window -->
    <div class="chat-panel" v-if="selectedUser">
      <div class="chat-header">
        <img :src="selectedUser.photo || '/default-profile.jpg'" :alt="selectedUser.name" class="chat-avatar" />
        <span class="chat-name">{{ selectedUser.name }}</span>
      </div>

      <div class="messages-list" ref="messagesList">
        <div v-if="loadingMessages" class="msg-loading">Loading...</div>
        <template v-else>
          <div v-if="messages.length === 0" class="msg-empty">No messages yet. Say hello!</div>
          <div
            v-for="msg in messages"
            :key="msg.id"
            class="message-bubble"
            :class="msg.sender_id === currentUserId ? 'sent' : 'received'"
          >
            <p>{{ msg.content }}</p>
            <span class="msg-time">{{ formatMessageTime(msg.timestamp) }}</span>
          </div>
        </template>
      </div>

      <div class="message-input-area">
        <input
          v-model="newMessage"
          @keydown="handleKeydown"
          placeholder="Type a message... (Enter to send)"
          :disabled="sending"
          class="msg-input"
        />
        <button @click="sendMessage" :disabled="!newMessage.trim() || sending" class="send-btn">
          Send
        </button>
      </div>
    </div>

    <div class="no-chat" v-else>
      <div class="no-chat-content">
        <div class="no-chat-icon">💬</div>
        <h3>Select a conversation</h3>
        <p>Choose someone from the left to start chatting</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* =========================
   MAIN LAYOUT
========================= */

.messages-view {

  display: flex;

  height: calc(100vh - 100px);

  margin-top: 110px;

  padding: 0 28px 28px;

  gap: 24px;

  overflow: hidden;

  background:
    radial-gradient(
      circle at top left,
      rgba(139,92,246,0.16),
      transparent 25%
    ),

    radial-gradient(
      circle at bottom right,
      rgba(236,72,153,0.14),
      transparent 25%
    ),

    #050816;
}

/* =========================
   SIDEBAR
========================= */

.conversations-panel {

  width: 360px;

  min-width: 320px;

  display: flex;

  flex-direction: column;

  overflow-y: auto;

  border-radius: 34px;

  background:
    linear-gradient(
      135deg,
      rgba(12,18,32,0.78),
      rgba(18,24,42,0.62)
    );

  backdrop-filter: blur(26px);

  border:
    1px solid rgba(255,255,255,0.08);

  box-shadow:
    0 20px 40px rgba(0,0,0,0.38);
}

/* =========================
   HEADER
========================= */

.panel-header {

  padding: 28px;

  border-bottom:
    1px solid rgba(255,255,255,0.06);
}

.panel-header h3 {

  margin: 0;

  color: white;

  font-size: 1.6rem;

  font-weight: 800;

  letter-spacing: -0.03em;
}

/* =========================
   EMPTY STATES
========================= */

.panel-loading,
.panel-empty {

  padding: 40px 24px;

  color:
    rgba(255,255,255,0.58);

  text-align: center;

  font-size: 0.95rem;
}

/* =========================
   CONVERSATION ITEM
========================= */

.conv-item {

  display: flex;

  align-items: center;

  gap: 14px;

  padding: 18px 20px;

  margin: 10px 14px;

  border-radius: 24px;

  cursor: pointer;

  transition: all 0.3s ease;

  border:
    1px solid transparent;
}

.conv-item:hover {

  background:
    rgba(255,255,255,0.06);

  transform:
    translateY(-2px);
}

.conv-item.active {

  background:
    linear-gradient(
      135deg,
      rgba(139,92,246,0.18),
      rgba(236,72,153,0.12)
    );

  border:
    1px solid rgba(255,255,255,0.08);

  box-shadow:
    0 0 24px rgba(139,92,246,0.18);
}

/* =========================
   AVATARS
========================= */

.conv-avatar,
.chat-avatar {

  border-radius: 50%;

  object-fit: cover;

  border:
    2px solid rgba(255,255,255,0.08);
}

.conv-avatar {

  width: 56px;
  height: 56px;
}

.chat-avatar {

  width: 52px;
  height: 52px;
}

/* =========================
   CONVERSATION TEXT
========================= */

.conv-info {

  flex: 1;

  min-width: 0;
}

.conv-name {

  font-size: 1rem;

  font-weight: 700;

  color: white;

  margin-bottom: 4px;

  white-space: nowrap;

  overflow: hidden;

  text-overflow: ellipsis;
}

.conv-preview {

  font-size: 0.85rem;

  color:
    rgba(255,255,255,0.58);

  white-space: nowrap;

  overflow: hidden;

  text-overflow: ellipsis;
}

.conv-time {

  font-size: 0.72rem;

  color:
    rgba(255,255,255,0.45);
}

/* =========================
   CHAT PANEL
========================= */

.chat-panel {

  flex: 1;

  display: flex;

  flex-direction: column;

  overflow: hidden;

  border-radius: 34px;

  background:
    linear-gradient(
      135deg,
      rgba(12,18,32,0.78),
      rgba(18,24,42,0.62)
    );

  backdrop-filter: blur(26px);

  border:
    1px solid rgba(255,255,255,0.08);

  box-shadow:
    0 20px 40px rgba(0,0,0,0.38);
}

/* =========================
   CHAT HEADER
========================= */

.chat-header {

  display: flex;

  align-items: center;

  gap: 14px;

  padding: 24px 30px;

  border-bottom:
    1px solid rgba(255,255,255,0.06);
}

.chat-name {

  color: white;

  font-size: 1.2rem;

  font-weight: 700;
}

/* =========================
   MESSAGE AREA
========================= */

.messages-list {

  flex: 1;

  overflow-y: auto;

  padding: 30px;

  display: flex;

  flex-direction: column;

  gap: 14px;

  background:
    linear-gradient(
      to bottom,
      rgba(255,255,255,0.02),
      rgba(255,255,255,0.01)
    );
}

/* =========================
   BUBBLES
========================= */

.message-bubble {

  max-width: 72%;

  padding: 14px 18px;

  border-radius: 24px;

  position: relative;

  backdrop-filter: blur(18px);

  transition: all 0.3s ease;
}

.message-bubble p {

  margin: 0 0 6px;

  line-height: 1.5;

  word-wrap: break-word;
}

/* SENT */

.message-bubble.sent {

  align-self: flex-end;

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #6d28d9
    );

  color: white;

  border-bottom-right-radius: 8px;

  box-shadow:
    0 10px 24px rgba(139,92,246,0.3);
}

/* RECEIVED */

.message-bubble.received {

  align-self: flex-start;

  background:
    rgba(255,255,255,0.08);

  border:
    1px solid rgba(255,255,255,0.08);

  color: white;

  border-bottom-left-radius: 8px;
}

/* =========================
   TIMESTAMP
========================= */

.msg-time {

  font-size: 0.72rem;

  opacity: 0.65;

  text-align: right;

  display: block;
}

/* =========================
   INPUT AREA
========================= */

.message-input-area {

  display: flex;

  gap: 14px;

  padding: 22px 28px;

  border-top:
    1px solid rgba(255,255,255,0.06);
}

/* INPUT */

.msg-input {

  flex: 1;

  height: 58px;

  border-radius: 22px;

  border:
    1px solid rgba(255,255,255,0.08);

  background:
    rgba(255,255,255,0.06);

  color: white;

  padding: 0 20px;

  outline: none;

  font-size: 0.95rem;

  backdrop-filter: blur(18px);

  transition: all 0.3s ease;
}

.msg-input::placeholder {

  color:
    rgba(255,255,255,0.45);
}

.msg-input:focus {

  border-color:
    rgba(139,92,246,0.45);

  box-shadow:
    0 0 24px rgba(139,92,246,0.22);
}

/* SEND BUTTON */

.send-btn {

  height: 58px;

  padding: 0 28px;

  border: none;

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
    0 10px 24px rgba(139,92,246,0.28);
}

.send-btn:hover:not(:disabled) {

  transform:
    translateY(-2px);

  box-shadow:
    0 14px 30px rgba(139,92,246,0.38);
}

.send-btn:disabled {

  opacity: 0.5;

  cursor: not-allowed;
}

/* =========================
   EMPTY CHAT
========================= */

.no-chat {

  flex: 1;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 34px;

  background:
    linear-gradient(
      135deg,
      rgba(12,18,32,0.72),
      rgba(18,24,42,0.58)
    );

  border:
    1px solid rgba(255,255,255,0.08);

  backdrop-filter: blur(24px);
}

.no-chat-content {

  text-align: center;

  color:
    rgba(255,255,255,0.62);
}

.no-chat-icon {

  font-size: 5rem;

  margin-bottom: 20px;
}

.no-chat-content h3 {

  font-size: 1.8rem;

  color: white;

  margin-bottom: 10px;
}

/* =========================
   MOBILE
========================= */

@media (max-width: 768px) {

  .messages-view {

    padding: 0 12px 18px;
  }

  .conversations-panel {

    width: 100%;
  }

  .chat-panel {

    display: none;
  }

  .messages-view.chat-open .conversations-panel {

    display: none;
  }

  .messages-view.chat-open .chat-panel {

    display: flex;

    width: 100%;
  }

  .message-bubble {

    max-width: 88%;
  }
}
</style>
