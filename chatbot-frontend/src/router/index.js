import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/LoginPage.vue'
import Chat from '../components/ChatComponent.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/chat', component: Chat },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
