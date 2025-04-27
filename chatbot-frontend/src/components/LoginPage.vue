<template>
  <div>
    <h1>Login Page</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Nom d'utilisateur</label>
        <input type="text" id="username" v-model="username" placeholder="Entrez votre nom d'utilisateur" required />
      </div>
      <div>
        <label for="password">Mot de passe</label>
        <input type="password" id="password" v-model="password" placeholder="Entrez votre mot de passe" required />
      </div>
      <button type="submit">Se connecter</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    handleLogin() {
      if (this.username && this.password) {
        console.log("Login attempt:", this.username);
        // Appel à l'API pour la connexion, par exemple
        // Exemple d'appel pour récupérer le token :
        // this.$axios.post('/login', { username: this.username, password: this.password })
        //   .then(response => { 
        //     // Manipuler la réponse de l'API ici
        //   })
        //   .catch(error => {
        //     console.error("Erreur de connexion", error);
        //   });
      } else {
        alert("Veuillez entrer un nom d'utilisateur et un mot de passe");
      }
    }
  }
};
</script>

<style scoped>
/* Style spécifique pour LoginPage */
form {
  max-width: 300px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

label {
  margin: 8px 0;
  font-size: 14px;
}

input {
  margin-bottom: 16px;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
