<template>
  <div>
    <h1>Chat Component</h1>
    <p>{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: "ChatComponent",
  data() {
    return {
      message: "Bonjour, comment puis-je vous aider ?"
    };
  }
};
</script>

<style scoped>
/* Style spécifique pour ChatComponent */
div {
  color: blue;
  font-size: 18px;
}
h1 {
  font-size: 24px;
  font-weight: bold;
}
</style>
