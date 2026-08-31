import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AlumnosView from '../views/AlumnosView.vue'
import TutoresView from '../views/TutoresView.vue'
import ClasesView from '../views/ClasesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/alumnos',
      name: 'alumnos',
      component: AlumnosView
    },
    {
      path: '/tutores',
      name: 'tutores',
      component: TutoresView
    },
    {
      path: '/clases',
      name: 'clases',
      component: ClasesView
    }
  ]
})

export default router