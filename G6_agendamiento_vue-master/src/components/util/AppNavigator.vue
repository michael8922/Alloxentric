<template>
	<v-navigation-drawer
		class="navbar-nav bg-gradient-primary"
		app
		width="290"
		v-model="drawer"
		dark
		temporary
	>
		<v-list-item>
			<v-list-item-content>
				<v-list-item-title>
					<img src="@/assets/img/Alloxentric-logo-white.png" width="190" height="45" />
				</v-list-item-title>
			</v-list-item-content>
		</v-list-item>
		<v-list>
			<v-list-item-title class="text-center">
				Menú
			</v-list-item-title>
			<v-divider></v-divider>
			<v-list-group
				class="justify-content-between sidebar-brand d-flex align-items-center justify-content-center"
				v-for="(item, i) in filteredItems"
				:key="i"
				:v-model="selected"
				active-class="active"
				color="#FFFFFF"
				@click="changeRoute(item)"
			>
				<template v-slot:activator>
					<v-list-item-icon class="mr-0"></v-list-item-icon>
					<v-list-item-content>
						<v-list-item-title v-text="item.title"></v-list-item-title>
					</v-list-item-content>
				</template>
			</v-list-group>
		</v-list>
	</v-navigation-drawer>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import { INavigator } from '@/model/util/INavigator';

@Component({
	name: 'AppNavigator',
	data() {
		return {
			drawer: false,
		};
	},
	methods: {
		showMenu2() {
			this.drawer = true;
		},
		determineHomePage(role) {
			// Devuelve el nombre de la ruta de inicio basada en el rol
			switch(role) {
			case 'doctor':
				return 'MainInicio'; // Nombre de la ruta para doctores
			case 'paciente':
				return 'MainUsuario'; // Nombre de la ruta para pacientes
			default:
				return 'SomeOtherRoute'; // Nombre de la ruta por defecto o para otros roles
			}
		},
	},
	computed: {
		filteredItems(): INavigator[] {
			const role = this.$store.state.tokenParsed.realm_access.roles[0];
			if (role === 'doctor') {
				// Mostrar opciones para el rol de doctor
				return this.items.filter(
					(item) => item.title !== 'Agendamiento Medico'
				);
			} else if (role === 'paciente') {
				// Mostrar solo Agendamiento Medico para el rol de paciente
				return this.items.filter((item) => item.title === 'Agendamiento Medico');
			} else {
				// Otros roles pueden personalizarse según sea necesario
				return this.items;
			}
		},
	},
	created() {

		this.$root.$refs.compmenu_component = this;
	},
	watch: {
	// Observa los cambios en los roles del usuario
	'$store.state.tokenParsed.realm_access.roles': {
		handler(newRoles) {
		// Llama a determineHomePage cada vez que cambien los roles
		const homePage = this.determineHomePage(newRoles[0]);
		// Redirige al usuario a la página de inicio correspondiente
		this.$router.push({ name: homePage });
		},
		deep: true, // Esto asegura que la vigilancia sea profunda y reactiva a cambios en objetos/arrays
		immediate: true // Esto asegura que el watcher se ejecute inmediatamente con el valor actual al inicializarse
	}
	},
})
export default class AppNavigator {
	public selected = 0;
	private currentRoute = '';
	public items: Array<INavigator> = [
		{
			title: 'Inicio' as string,
			urlName: 'MainInicio',
			parent: 'dashboardInicio',
			subMenus: [],
		},
		{
			title: 'Agenda' as string,
			urlName: 'MainAgenda',
			parent: 'dashboardInicio',
			subMenus: [],
		},
		{
			title: 'Lista Espera' as string,
			urlName: 'MainEspera',
			parent: 'dashboardInicio',
			subMenus: [],
		},
		{
			title: 'Guardar Hora' as string,
			urlName: 'GuardarHora',
			parent: 'dashboardInicio',
			subMenus: [],
		},
		{
			title: 'Configuración' as string,
			urlName: 'MainConfiguracion',
			parent: 'dashboardInicio',
			subMenus: [],
		},
		{
			title: 'Agendamiento Medico' as string,
			urlName: 'MainUsuario',
			parent: 'dashboardInicio',
			subMenus: [],
		},
	];
	public changeRoute(to: INavigator) {
		if (to.title === 'Salir') {
			//this.logout();
			//Util.showMessage('Hasta pronto', Icon.INFO);
			this.$router.push({
				name: 'home',
			});
			//this.keycloak.logout();
			return;
		}
		if (to.urlName !== this.currentRoute && to.urlName !== undefined) {
			this.currentRoute = to.parent;
			this.$router.push({
				name: to.urlName,
			});
		}
	}
}
</script>

<style scoped>
.active {
	background-color: transparent;
}
</style>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;400;600;800;900&display=swap');

.v-application {
	font-family: 'nunito', sans-serif !important;
}
</style>
