import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/LoginPage.vue';
import Chat from '../components/ChatComponent.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
