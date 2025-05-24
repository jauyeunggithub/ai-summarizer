import { createRouter, createWebHistory } from 'vue-router'

import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import SignUp from '@/views/SignUp.vue'
import Profile from '@/views/Profile.vue'
import Summaries from '@/views/Summaries.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUp,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/summaries',
    name: 'Summaries',
    component: Summaries,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
