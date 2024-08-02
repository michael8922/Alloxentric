<template>
  <v-app-bar color="" app>
  
    <v-list-item-avatar
      ><v-icon @click.stop="showMenu()" large
        >mdi-menu</v-icon
      ></v-list-item-avatar
    >

    <div>
      <v-avatar :size="35">
        <img src="@/assets/img/global.png" />
      </v-avatar>
      <select
        class="mx-2"
        v-model="$i18n.locale"
        @change="updateLanguage($event.target.value)"
        variant="info"
      >
        mdi-chevron-down
        <option
          hide-details
          v-for="(o, i) in locales_array"
          :key="i"
          :value="o.value"
          :selected="o.value === locale_default"
        >
          {{ o.caption }}
        </option>
      </select>
    </div>

    <!-- Sidebar Toggle (Topbar) -->
    <button
      id="sidebarToggleTop"
      class="btn btn-link d-md-none rounded-circle mr-3"
    >
      <i class="fa fa-bars"></i>
    </button>

    <!-- Topbar Navbar -->
    <ul class="navbar-nav ml-auto">
      <!-- Nav Item - Search Dropdown (Visible Only XS) -->
      <li class="nav-item dropdown no-arrow d-sm-none">
        <a
          class="nav-link dropdown-toggle"
          href="#"
          id="searchDropdown"
          role="button"
          data-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
        >
          <i class="fas fa-search fa-fw"></i>
        </a>
      </li>

      <div class="topbar-divider d-none d-sm-block"></div>

      <!-- Nav Item - User Information -->
      <li class="nav-item dropdown no-arrow">
        <a
          class="nav-link dropdown-toggle pr-4"
          href="#"
          id="userDropdown"
          role="button"
          data-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
        >
          <span class="mr-2 d-none d-lg-inline text-gray-600 small"
            >{{ this.$store.state.tokenParsed.name }}</span
          >
          <img
            class="img-profile rounded-circle"
            src="@/assets/img/undraw_profile.svg"
          />
        </a>
      </li>
    </ul>
	<v-list>
		<v-list-item @click="listenLogout">
		<v-list-item-title>
			Cerrar Sesión
		</v-list-item-title>
		</v-list-item>
	</v-list>

    <!-- End of Topbar -->
    <div class="text-center"></div>

  </v-app-bar>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import { LOCALES, Locales } from "@/locales/i18n";
import MixinLogin from "@/mixing/MixinLogin.vue";
import defaultLocale from "@/i18n";
import store from "@/store"
import Util from '@/utils/Util';
import { Icon } from '@/model/util/Icon';

@Component({
  name: "AppBar",
})
export default class AppBar extends MixinLogin {
  public locales_array = LOCALES;
  public locale_default = defaultLocale;
  @Prop() readonly keycloak!: string;

  public mounted() {
	console.log("Aceeso", this.$store.state.tokenParsed);
  }

public listenLogout() {
  if (!this.$keycloak) {
    console.error('Keycloak instance is not available');
    Util.showMessage('No se pudo cerrar la sesión', Icon.ERROR);
    return;
  }

  // Aquí indicas la ruta específica de tu aplicación a la que quieres redirigir después del logout
  const postLogoutRedirectUri = `${window.location.origin}/MainLogin`;

  this.$keycloak.logout({ redirectUri: postLogoutRedirectUri })
    .then(() => {
      console.log('Logout successful');
      // Limpia el estado de la sesión aquí si es necesario
      this.$router.push({ name: 'MainLogin' }); // Redirige con Vue Router en lugar de Keycloak
    })
    .catch(error => {
      console.error('Logout failed', error);
      Util.showMessage('Error al cerrar sesión', Icon.ERROR);
    });
}

  public updateLanguage(lang: Locales) {
    console.log("cambiando idioma a ", lang);
    this.$emit("changeEvent", lang);
  }

  public showMenu() {
    this.$root.$refs.compmenu_component.showMenu2();
  }
}
</script>
