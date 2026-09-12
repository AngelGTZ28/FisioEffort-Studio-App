import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../supabase'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import AlumnosView from '../views/AlumnosView.vue'
import TutoresView from '../views/TutoresView.vue'
import ClasesView from '../views/ClasesView.vue'
import PagosView from '../views/PagosView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
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
    },
    {
      path: '/pagos',
      name: 'pagos',
      component: PagosView
    }
  ]
})

// CADENERO DE SUPABASE
router.beforeEach(async (to, _from) => {
  // Le preguntamos directamente a Supabase si hay una sesión activa
  const { data } = await supabase.auth.getSession()
  const tieneSesion = data.session !== null

  // Si intenta ir a cualquier página que NO sea el login, y no tiene sesión...
  if (to.name !== 'login' && !tieneSesion) {
    return { name: 'login' } // Lo pateamos de regreso al logins
  }
  
  // Si ya tiene sesión y quiere ir al login, lo mandamos al inicio (ya está logueado)
  if (to.name === 'login' && tieneSesion) {
    return { name: 'home' } // Asegúrate de que tu ruta principal se llame 'home'
  }
})

export default router