import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../components/LoginPage.vue'
import ChatPage from '../components/ChatPage.vue'

const routes = [
  { path: '/', component: LoginPage },
  { path: '/chat', component: ChatPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
