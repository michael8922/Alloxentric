<template>

    <div class="bg-gradient-primary">
        <!-- Begin Page Content -->
        <div class="container">

            <!-- Outer Row -->
            <div class="row justify-content-center">

                <div class="col-xl-10 col-lg-12 col-md-9">

                    <div class="card o-hidden border-0 shadow-lg my-5">
                        <div class="card-body p-0">
                            <!-- Nested Row within Card Body -->
                            <div class="row">
                                <div class="col-lg-6 d-none d-lg-block bg-login-image"></div>
                                <div class="col-lg-6">
                                    <div class="p-5">
                                        <div class="text-center pb-4">
                                            <img src="img/alloxentric_isotipo.png" alt="">
                                        </div>
                                        <div class="text-center">
                                            <h1 class="h4 text-gray-900 mb-4">Bienvenido(a)!</h1>
                                        </div>
                                        <form class="user">
                                             <!-- Campo Rut -->
                                            <div class="form-group">
                                                <input 
                                                type="text" class="form-control form-control-user" 
                                                    id="rut" 
                                                    placeholder="Rut" 
                                                    v-model="rutElement"
                                                    required>
                                            </div>

                                            <!-- Campo Nombre y Appelido -->
                                            <div class="form-row">
                                                <div class="form-group col-md-6">
                                                    <input type="text" class="form-control form-control-user"
                                                    id="nombre" 
                                                    placeholder="Nombre"
                                                    v-model="nombreElement"
                                                    required>
                                                </div>

                                                <div class="form-group col-md-6">
                                                    <input type="text" class="form-control form-control-user"
                                                    id="apellido" 
                                                    placeholder="Apellido"
                                                    v-model="apellidoElement"
                                                    required>
                                                </div>
                                            </div>

                                            <!-- Campo Telefono -->
                                            <div class="form-group">
                                            <input type="tel" class="form-control form-control-user" 
                                                id="telefono" 
                                                placeholder="Teléfono" 
                                                v-model="telefonoElement"
                                                required>
                                            </div>

                                            <!-- Campo Correo -->
                                            <div class="form-group">
                                                <input type="email" class="form-control form-control-user"
                                                    id="email"
                                                    placeholder="Correo electronico"
                                                    v-model="correoElement"
                                                    required>
                                            </div>

                                            <!-- Contraseña -->
                                            <div class="form-group">
                                                <input type="password" class="form-control form-control-user"
                                                    id="password" 
                                                    placeholder="Contraseña"
                                                    v-model="passwordElement"
                                                    required>
                                            </div>
                                            <!-- 
                                            <a class="btn btn-primary btn-user">
                                                Registrarse
                                            </a>
                                            -->

                                            <v-btn
                                            class="btn btn-primary btn-user btn-block"
                                            @click="aggregateItem()"
                                            >
                                            Registrarse
                                            </v-btn>

                                            <hr>
                                            <a href="index.html" class="btn btn-google btn-user btn-block">
                                                <i class="fab fa-google fa-fw"></i> Login con Google
                                            </a>
                                            <a href="index.html" class="btn btn-facebook btn-user btn-block">
                                                <i class="fab fa-facebook-f fa-fw"></i> Login con Facebook
                                            </a>
                                            <a href="index.html" class="btn btn-facebook btn-user btn-block">
                                                <i class="fab fa-facebook-f fa-fw"></i> Login con Linkedin
                                            </a>
                                        </form>
                                        <hr>
                                        <div class="text-center">
                                            <a class="small" href="forgot-password.html">¿Ha olvidado su contraseña?</a>
                                        </div>
                                        <div class="text-center">
                                            <a class="small" href="register.html">¿Ya tienes una cuenta?</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

            </div>

        </div>
    </div>
    <!-- /.container-fluid -->

</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
    import { internet } from '@/utils/Internet';
	import { AxiosResponse } from 'axios';
	import Util from '@/utils/Util';
	import DataTable from '@/components/util/DataTable.vue';
    import axios from "axios";
	@Component({
		name: 'LoginUser',
	})

	export default class Login extends Vue {
        public isLoading = false;
		public message = this.$t("Main.message");
        public rut = this.$t("LoginUser.rut");
        public nombre = this.$t("LoginUser.nombre");
        public apellido = this.$t("LoginUser.apellido");
        public correo = this.$t("LoginUser.correo");
        public telefono = this.$t("LoginUser.telefono");
        public password = this.$t("LoginUser.password");
        public btnSave = this.$t("LoginUser.btnSave");

        public rutElement = "";
        public nombreElement = "";
        public apellidoElement = "";
        public correoElement = "";
        public telefonoElement = "";
        public passwordElement = "";
        public current_item = {
            'Rut': '', 
            'Nombre': '', 
            'Apellido': '',
            'Correo': '',
            'Telefono': '',
            'Password': '', 
        }; 

        mounted(): void {
		this.getData();
	}

	private getData(): void {
		this.isLoading = true;
		const request_PruebaConexion = internet
			.newRequest()
			.get(`pacientes/paciente`);
		Util.waitForPromises([request_PruebaConexion])
			.then((responses) => {
				const response_1 = responses[0] as AxiosResponse;
				let message = this.message3 as string
				this.message3 = message+response_1.data
			})
			.catch(console.log)
			.finally(() => {
				this.isLoading = false;
			});
	}

    public aggregateItem(){
        let rut = this.rutElement;
        let nombre = this.nombreElement;
        let apellido = this.apellidoElement;
        let correo = this.correoElement;
        let telefono = this.telefonoElement;
        let password = this.passwordElement;
        let dt = JSON.stringify({
            'rut': rut, 
            'nombre': nombre,
            'apellido': apellido,
            'correo': correo,
            'telefono': telefono,
            'password': password,
        });
        let config = {
            //aqui llamamos al endpoint desde el back que necesitamos utilizar para agregar registros
            method: 'post',
            url: process.env.VUE_APP_API_2 + "/pacientes/paciente",
            data: dt,
            headers: { 
                Authorization: `Bearer ${this.$store.state.token}`,
                'Content-Type': 'application/json'
            }
        };
        axios(config)
			.then(response => {
                //this.dialog = false;
                this.rutElement = "";
                this.nombreElement = "";
                this.apellidoElement = "";
                this.correoElement = "";
                this.telefonoElement = "";
                this.passwordElement = "";
                //this.getData();
			})
    }
}

</script>