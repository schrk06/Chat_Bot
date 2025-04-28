<template>
    <div class="login-container">
      <h1>Se connecter ou s'inscrire</h1>
      <form @submit.prevent="handleLogin">
        <input v-model="username" placeholder="Nom d'utilisateur" required />
        <input v-model="password" type="password" placeholder="Mot de passe" required />
        <div class="button-group">
          <button type="submit">Connexion</button>
          <button type="button" @click="handleRegister">Créer un compte</button>
        </div>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import api from '../services/api'
  
  const router = useRouter()
  const username = ref('')
  const password = ref('')
  const errorMessage = ref('')
  const successMessage = ref('')
  
  const handleLogin = async () => {
    try {
      const response = await api.post('/login', {
        username: username.value,
        password: password.value
      })
      localStorage.setItem('token', response.data.access_token)
      router.push('/chat')
    } catch (error) {
      errorMessage.value = "Identifiants incorrects."
      successMessage.value = ''
    }
  }
  
  const handleRegister = async () => {
    try {
      await api.post('/register', {
        username: username.value,
        password: password.value
      })
      successMessage.value = "Inscription réussie ! Connecte-toi maintenant."
      errorMessage.value = ''
    } catch (error) {
      errorMessage.value = "Erreur lors de l'inscription (compte existant ?)"
      successMessage.value = ''
    }
  }
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 100px;
  }
  input {
    margin: 5px;
    padding: 10px;
    width: 200px;
  }
  .button-group {
    display: flex;
    gap: 10px;
    margin-top: 10px;
  }
  button {
    padding: 10px 20px;
    cursor: pointer;
  }
  .error {
    color: red;
    margin-top: 10px;
  }
  .success {
    color: green;
    margin-top: 10px;
  }
  </style>
  