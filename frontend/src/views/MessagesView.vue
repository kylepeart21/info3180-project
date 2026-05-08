<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
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

onMounted(async () => {
  await fetchConversations()

  // If navigated from a profile page with ?userId=X, open that chat
  const targetUserId = route.query.userId ? parseInt(route.query.userId) : null
  if (targetUserId) {
    // Try to find user in existing conversations first
    const existing = conversations.value.find(c => c.user.id === targetUserId)
    if (existing) {
      await selectConversation(existing.user)
    } else {
      // No prior conversation — fetch the user and open a fresh chat panel
      try {
        const res = await apiClient.get(`/api/users/${targetUserId}`, { headers: headers() })
        const user = res.data.user
        // Manually set selectedUser so the chat panel opens immediately
        selectedUser.value = user
        messages.value = []
        loadingMessages.value = false
      } catch (e) {
        console.error('Could not load user for chat:', e)
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
  <div class="messages-view">
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
.messages-view {
  display: flex;
  height: calc(100vh - 70px);
  margin-top: 56px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  overflow: hidden;
}

/* Left panel */
.conversations-panel {
  width: 320px;
  min-width: 260px;
  border-right: 1px solid #e9ecef;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background: #fff;
}

.panel-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e9ecef;
  background: #f8f9fa;
}

.panel-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.panel-loading, .panel-empty {
  padding: 20px;
  color: #6c757d;
  text-align: center;
  font-size: 14px;
}

.conv-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.15s;
  gap: 12px;
}

.conv-item:hover { background: #f8f9fa; }
.conv-item.active { background: #e8f4fd; }

.conv-avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.conv-info {
  flex: 1;
  min-width: 0;
}

.conv-name {
  font-weight: 600;
  font-size: 14px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conv-preview {
  font-size: 13px;
  color: #6c757d;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conv-time {
  font-size: 11px;
  color: #aaa;
  flex-shrink: 0;
}

/* Right panel */
.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #fff;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  border-bottom: 1px solid #e9ecef;
  background: #f8f9fa;
}

.chat-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.chat-name {
  font-weight: 600;
  font-size: 16px;
}

.messages-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #f5f5f5;
}

.msg-loading, .msg-empty {
  text-align: center;
  color: #6c757d;
  margin: auto;
  font-size: 14px;
}

.message-bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.4;
  position: relative;
}

.message-bubble p {
  margin: 0 0 4px 0;
  word-wrap: break-word;
}

.message-bubble.sent {
  background: #3498db;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.message-bubble.received {
  background: #fff;
  color: #333;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.msg-time {
  font-size: 11px;
  opacity: 0.7;
  display: block;
  text-align: right;
}

.message-input-area {
  display: flex;
  gap: 10px;
  padding: 14px 20px;
  border-top: 1px solid #e9ecef;
  background: #fff;
}

.msg-input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 24px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.msg-input:focus { border-color: #3498db; }

.send-btn {
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 24px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.send-btn:hover:not(:disabled) { background: #2980b9; }
.send-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* No selection state */
.no-chat {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
}

.no-chat-content {
  text-align: center;
  color: #6c757d;
}

.no-chat-icon { font-size: 48px; margin-bottom: 16px; }
.no-chat-content h3 { font-size: 20px; margin-bottom: 8px; color: #495057; }
.no-chat-content p { font-size: 14px; }

@media (max-width: 600px) {
  .conversations-panel { width: 100%; }
  .chat-panel { display: none; }
  .messages-view.chat-open .conversations-panel { display: none; }
  .messages-view.chat-open .chat-panel { display: flex; width: 100%; }
}
</style>
