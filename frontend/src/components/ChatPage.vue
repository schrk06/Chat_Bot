<template>
    <div class="chat-container">
      <div class="header">
        <h1>Chatbot 🤖</h1>
        <button @click="logout" class="logout-button">Déconnexion</button>
      </div>
  
      <div class="messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" class="message">
          <strong>{{ message.sender }} :</strong> {{ message.text }}
        </div>
        <div v-if="loading" class="message">
          <em>Le bot est en train d'écrire...</em>
        </div>
      </div>
  
      <form @submit.prevent="sendMessage" class="input-form">
        <input v-model="prompt" placeholder="Écris ton message..." required />
        <button type="submit">Envoyer</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, nextTick } from 'vue'
  import api from '../services/api'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  const prompt = ref('')
  const messages = ref([])
  const loading = ref(false)
  const messagesContainer = ref(null)
  
  const sendMessage = async () => {
    if (!prompt.value.trim()) return
    messages.value.push({ sender: "Moi", text: prompt.value })
  
    const userPrompt = prompt.value
    prompt.value = ''
    loading.value = true
  
    try {
      const response = await api.post('/chat', { 
        prompt: userPrompt,
        provider: "huggingface" 
      })
  
      messages.value.push({ sender: "Bot", text: response.data.response })
    } catch (error) {
      if (error.response && error.response.status === 401) {
        router.push('/')
      } else {
        messages.value.push({ sender: "Bot", text: "Erreur de communication avec le serveur." })
      }
    } finally {
      loading.value = false
      await nextTick()
      scrollToBottom()
    }
  }
  
  const scrollToBottom = () => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  }
  
  const logout = () => {
    localStorage.removeItem('token')
    router.push('/')
  }
  </script>
  
  <style scoped>
  .chat-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 50px;
  }
  .header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    padding: 0 30px;
    align-items: center;
  }
  .logout-button {
    padding: 5px 10px;
    cursor: pointer;
  }
  .messages {
    width: 80%;
    max-width: 500px;
    min-height: 300px;
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
    overflow-y: auto;
  }
  .message {
    margin-bottom: 5px;
  }
  .input-form {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  input {
    width: 300px;
    padding: 10px;
  }
  button {
    padding: 10px 20px;
    margin-left: 10px;
    cursor: pointer;
  }
  </style>
  