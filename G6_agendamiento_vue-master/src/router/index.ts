import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import MainBase from '../views/MainBase.vue'
import MainInicio from '../views/MainInicio.vue'
import CRUDView from '../views/CRUDView.vue'
import MainAgenda from '../views/MainAgenda.vue'
import MainEspera from '../views/MainEspera.vue'
import MainConfiguracion from '../views/MainConfiguracion.vue'
import MainLogin from '../views/MainLogin.vue'
import RegistroDoctor from '../views/RegistroDoctor.vue'
import GuardarHora from '../views/MainHora.vue'
import MainUsuario from '../views/MainUsuario.vue'


Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'base',
    component: MainBase,
    redirect: { name: 'MainLogin' }, // Redirige utilizando el nombre de la ruta
    children: [
      {
        path: 'MainLogin',
        name: 'MainLogin',
        component: MainLogin,
        meta: { showNavBar: false }
      },
      {
        path: 'inicio', // Se elimina /home ya que está implícito en la ruta del padre
        name: 'MainInicio',
        component: MainInicio,
        meta: { showNavBar: true }
      },
      {
        path: 'agenda',
        name: 'MainAgenda',
        component: MainAgenda,
        meta: { showNavBar: true }
      },
      {
        path: 'espera',
        name: 'MainEspera',
        component: MainEspera,
        meta: { showNavBar: true }
      },
      {
        path: 'guardarhora',
        name: 'GuardarHora',
        component: GuardarHora,
        meta: { showNavBar: true }
      },
      {
        path: 'configuracion',
        name: 'MainConfiguracion',
        component: MainConfiguracion,
        meta: { showNavBar: true }
      },
      {
        path: 'RegistroDoctor',
        name: 'RegistroDoctor',
        component: RegistroDoctor,
        meta: { showNavBar: true }
      },
      {
        path: 'MainUsuario',
        name: 'MainUsuario',
        component: MainUsuario,
        meta: { showNavBar: true }
      }
    ] 
  }
]

const router = new VueRouter({
  mode: 'history', // Agrega el modo history para evitar el hash en la URL
  routes
})

export default router

