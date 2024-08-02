import Vue from "vue";
import "./plugins/axios";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import i18n from "./i18n";
import "./style.css";
import "./sb-admin-2.css";
import "./sb-admin-2.min.css";

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: (h) => h(App),
}).$mount("#app");

import Keycloak, { KeycloakOnLoad } from "keycloak-js";

/* import { messages, defaultLocale } from "@/i18n";

Vue.use(VueI18n)

export const i18n = new VueI18n({
  messages,
  locale: process.env.VUE_APP_I18N_LOCALE || defaultLocale,
  fallbackLocale: process.env.VUE_APP_I18N_FALLBACK_LOCALE || defaultLocale
}); */

Vue.config.productionTip = false;

const initOptions = {
  url: process.env.VUE_APP_KEYCLOAK_URL,
  realm: process.env.VUE_APP_KEYCLOAK_REALM,
  clientId: process.env.VUE_APP_KEYCLOAK_CLIENT,
  onLoad: "login-required" as KeycloakOnLoad,
};


const keycloak = new Keycloak(initOptions);
keycloak.init({ onLoad: 'check-sso' }).then((auth) => {
  if (auth) {
    console.log('Authenticated', keycloak);
    // Si el usuario está autenticado, configurar Keycloak en Vue.prototype y continuar
    Vue.prototype.$keycloak = keycloak;
    store.dispatch('guardarToken', keycloak);
  } else {
    console.log('Not authenticated');
    // Si el usuario no está autenticado, redirigir a la vista MainLogin de la aplicación Vue
    router.push({ name: 'MainLogin' });
  }

  new Vue({
    router,
    store,
    vuetify,
    i18n,
    render: (h) => h(App),
  }).$mount('#app');
  
  // Agregar aquí la lógica de actualización del token si es necesario
})
.catch((error) => {
  console.error('Authenticated Failed', error);
  // Manejar error de autenticación
});
  
