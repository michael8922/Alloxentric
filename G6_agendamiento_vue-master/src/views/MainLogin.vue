<template>

    <div class="bg-gradient-primary h-100 d-flex flex-column">
        <!-- Begin Page Content -->
        <div class="container">

                <div class="text-center mt-3 login-text">
                    <img src="../assets/img/Alloxentric-logo-white.png" alt="Alloxentric" class="my-4" width="500">
                    <p>Si usted es un <strong>doctor</strong>, y desea acceder a la información de sus pacientes, por favor <strong>seleccione la opción de "Ingresar como Doctor" ubicada a la izquierda*</strong> </p>
                    <hr class="mx-auto"  style="width: 30%; border: solid 1px #fff">
                    <p>Si usted es un <strong>paciente</strong>, y desea agendar una nueva cita médica, elija la opción "Agendar Cita" a la derecha. Aquí podrá seleccionar el horario que mejor le convenga y confirmar su próxima visita con nosotros.</p>
                </div>

                <div class="container my-auto">
                    <!-- Outer Row -->
                    <div class="row justify-content-center">

                        <div class="col-xl-6 ">

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
                                                    <h1 class="h4 text-gray-900 mb-4">Ingresar como <strong style="color: #01a79d; font-weight: 800;">Doctor</strong></h1>
                                                </div>
                                                <form class="user">
                                                    <a @click="iniciarSesion" class="btn btn-primary btn-user btn-block">
                                                        Entrar
                                                    </a>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>

                        <div class="col-xl-6 ">

                            <div class="card o-hidden border-0 shadow-lg my-5">
                                <div class="card-body p-0">
                                    <!-- Nested Row within Card Body -->
                                    <div class="row">
                                        <div class="col-lg-6 d-none d-lg-block bg-login-image-2"></div>
                                        <div class="col-lg-6">
                                            <div class="p-5">
                                                <div class="text-center pb-4">
                                                    <img src="img/alloxentric_isotipo.png" alt="">
                                                </div>
                                                <div class="text-center">
                                                    <h1 class="h4 text-gray-900 mb-4">Agendar <br> <strong style="color: #01a79d; font-weight: 800;">Cita</strong></h1>
                                                </div>
                                                <form class="user">
                                                    <a @click="entrarSinAutenticar" class="btn btn-primary btn-user btn-block">
                                                        Ingresar
                                                    </a>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>

                        <div class="col-xl-12">
                            <div class="alert alert-info fade show" role="alert">
                                <div class="d-flex justify-content-between align-items-center">
                                    <h1 class="alert-heading mb-0 h5">¿Necesitas modificar tu cita médica?</h1>
                                    <button type="button" class="btn btn-link" data-toggle="collapse" data-target="#collapseAlert" aria-expanded="false" aria-controls="collapseAlert">
                                        <i class="fas fa-chevron-down"></i>
                                    </button>
                                </div>
                                <div class="collapse" id="collapseAlert">
                                    <p>¡Hola! Queremos hacerte saber que si surge algún cambio en tu agenda y necesitas ajustar tu cita médica, ¡es fácil y rápido! Haz clic en el botón a continuación para modificar la fecha y hora de tu cita</p>
                                    <hr>
                                    <form class="user">
                                        <a @click="iniciarSesion" class="btn btn-primary btn-user">
                                            Modificar cita medica
                                        </a>
                                    </form>
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
import Keycloak from "keycloak-js";

@Component({
  name: 'Login',
})
export default class Login extends Vue {
  public message = this.$t("Main.message");

  entrarSinAutenticar() {
    // Redirige a la página que desees para acceso no autenticado
    this.$router.push({ name: "MainUsuario" });
  }

  iniciarSesion() {
    const initOptions: Keycloak.KeycloakConfig = {
      url: process.env.VUE_APP_KEYCLOAK_URL,
      realm: process.env.VUE_APP_KEYCLOAK_REALM,
      clientId: process.env.VUE_APP_KEYCLOAK_CLIENT,
      onLoad: "login-required",
    };

    const keycloak = Keycloak(initOptions);

    keycloak.init({ onLoad: initOptions.onLoad })
      .then((auth) => {
        if (auth) {
          // Autenticado correctamente con Keycloak
          // Redirige a la página principal autenticada
          this.$router.push({ name: "MainInicio" });
        } else {
          // No autenticado
          console.log("No autenticado");
        }
      })
      .catch((error: Keycloak.KeycloakError) => {
        // Manejar errores de inicialización de Keycloak
        console.error("Error de inicialización de Keycloak:", error);
      });
  }
}
</script>