<template>
  <div class="login-container">
    <h1>{{ isLogin ? 'Se connecter' : 'Créer un compte' }}</h1>
    
    <form @submit.prevent="isLogin ? handleLogin() : handleRegister()">
      <input v-model="username" placeholder="Nom d'utilisateur" required />
      <input v-model="password" type="password" placeholder="Mot de passe" required />
      
      <button type="submit">
        {{ isLogin ? 'Connexion' : 'Inscription' }}
      </button>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>

    <p class="toggle">
      <span v-if="isLogin">Pas encore de compte ?</span>
      <span v-else>Déjà un compte ?</span>
      <button @click="toggleMode">
        {{ isLogin ? 'Créer un compte' : 'Se connecter' }}
      </button>
    </p>
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
const isLogin = ref(true) // mode actuel : true = login, false = register

const toggleMode = () => {
  isLogin.value = !isLogin.value
  errorMessage.value = '' // reset les erreurs quand on change de mode
}

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
  }
}

const handleRegister = async () => {
  try {
    await api.post('/register', {
      username: username.value,
      password: password.value
    })
    errorMessage.value = "Inscription réussie, connectez-vous."
    isLogin.value = true // après inscription, retour à login automatique
  } catch (error) {
    errorMessage.value = "Erreur lors de l'inscription."
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
form {
  display: flex;
  flex-direction: column;
  align-items: center;
}
input {
  margin: 5px;
  padding: 10px;
  width: 200px;
}
button {
  padding: 10px 20px;
  margin-top: 10px;
  cursor: pointer;
}
.toggle {
  margin-top: 20px;
}
.toggle button {
  background: none;
  border: none;
  color: blue;
  cursor: pointer;
  text-decoration: underline;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
