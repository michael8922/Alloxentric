<template>
  <!-- Begin Page Content -->
  <div class="container-fluid cont-all bg-all">
    <!-- Page Heading -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">Configuración</h1>
    </div>

    <!-- Content Row -->
    <div class="row">
      <!-- Content Column -->
      <div class="col-lg-8 mb-4">
        <!-- Project Card Example -->
        <div class="card shadow mb-4">
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">Datos Personales</h6>
          </div>
          <div class="card-body">
            <div class="d-grid gap-2 col-12 mx-auto">
              <form class="user">
                <!-- telefono y correo -->
                <div class="form-row">
                  <div class="form-group col-md-4">
                    <input
                      type="number"
                      class="form-control form-control-user"
                      id="telefono"
                      placeholder="Telefono"
                      v-model="ElementTelefono"
                      required
                      @blur="agregarPrefijoChile"
                    />
                  </div>

                  <div class="form-group col-md-4">
                    <input
                      type="email"
                      class="form-control form-control-user"
                      id="correo"
                      placeholder="Correo"
                      v-model="CorreoElement"
                      required
                    />
                  </div>

                  <div class="form-group col-md-4">
                    <!-- Select Centro Medico -->
                    <select
                      class="custom-select form-control form-control-user"
                      id="ElementArrayCentroMedico"
                      v-model="selectCentroMedico"
                      @change="saveSelectedValue"
                      required
                    >
                      <option class="alert-success font-weight-bold" value="" disabled selected>
                        Seleccione uno o mas centros medicos
                      </option>
                      <option
                        v-for="option in ElementArrayCentroMedico"
                        :value="option.value"
                        :key="option.value"
                      >
                        {{ option.text }}
                      </option>
                      <!-- Agrega opciones de comuna aquí -->
                    </select>
                    <!-- End Select Centro Medico-->
                  </div>
                </div>

                <!-- Especialidad y Centro Medico -->
                <div class="form-row">
                  <div class="form-group col-md-4">
                    <!-- Select Especialidad -->
                    <select
                      class="custom-select form-control form-control-user"
                      id="ElementArrayCentroMedico"
                      v-model="selectEspecialidad"
                      @change="saveSelectedValueEspecialidad"
                      required
                    >
                      <option class="alert-success font-weight-bold p-1" value="" disabled selected>
                        Seleccione una especialidad
                      </option>
                      <option
                        v-for="option in ElementArrayEspecialidad"
                        :value="option.value"
                        :key="option.value"
                      >
                        {{ option.text }}
                      </option>
                      <!-- Agrega opciones de comuna aquí -->
                    </select>
                    <!-- End Select Especialidad -->
                  </div>

                  <div class="form-group col-md-4">
                    <input
                      type="text"
                      class="form-control form-control-user"
                      id="NContraseña"
                      placeholder="Nueva Contraseña"
                      v-model="NuevaContraseñaElement"
                      required
                    />
                  </div>

                  <div class="form-group col-md-4">
                    <input
                      type="text"
                      class="form-control form-control-user"
                      id="CNContraseña"
                      placeholder="Confirma Nueva Contraseña"
                      v-model="CNuevaContraseñaElement"
                      required
                    />
                  </div>
                </div>

                <div class="row">
                <div class="col-md-6 pr-0 pt-0 mt-4">
                  <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">
                      Contactabilidad confirmación
                    </h6>
                  </div>
                  <div class="card-body">
                    <div class="d-grid gap-2 col-12 mx-auto">
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="isChecked1"
                          id="flexCheckDefault"
                          @change="checkboxChanged('isChecked1')"
                        />
                        <label class="form-check-label" for="flexCheckDefault">
                          Teléfono
                        </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="isChecked2"
                          id="flexCheckChecked"
                          @change="checkboxChanged('isChecked2')"
                        />
                        <label class="form-check-label" for="flexCheckChecked">
                          Whatsapp
                        </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="isChecked3"
                          id="flexCheckChecked"
                          @change="checkboxChanged('isChecked3')"
                        />
                        <label class="form-check-label" for="flexCheckChecked">
                          Correo
                        </label>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="col-md-6 pl-0 pt-0 mt-4">
                  <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">
                      Contactabilidad lista de espera
                    </h6>
                  </div>
                  <div class="card-body">
                    <div class="d-grid gap-2 col-12 mx-auto">
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="isChecked4"
                          id="flexCheckDefault"
                          @change="checkboxChanged('isChecked4')"
                        />
                        <label class="form-check-label" for="flexCheckDefault">
                          Teléfono
                        </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="isChecked5"
                          id="flexCheckChecked"
                          @change="checkboxChanged('isChecked5')"
                        />
                        <label class="form-check-label" for="flexCheckChecked">
                          Whatsapp
                        </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="isChecked6"
                          id="flexCheckChecked"
                          @change="checkboxChanged('isChecked6')"
                        />
                        <label class="form-check-label" for="flexCheckChecked">
                          Correo
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

                <v-btn
                class="btn btn-primary btn-user"
                @click="aggregateItem()"
                >
                Guardar Cambios
                </v-btn>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Column -->
      <div class="col-lg-4 mb-4">
        <div class="row">
          <div class="col-lg-12">
            <!-- Project Card Example -->
            <div class="card shadow mb-4">
              <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">
                  Conectar cuenta Google
                </h6>
              </div>
              <div class="card-body">
                <div class="d-grid gap-2 col-12 mx-auto">
                  <button class="btn btn-google" type="button">
                    <i class="fab fa-fw fa-google"></i> Conectarse a Google
                  </button>
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
import { Component, Vue } from "vue-property-decorator";
import { ILabels } from "@/model/main/Ilabels";
import axios from "axios";

@Component({
  name: "MainConfiguracion",
})
export default class MainConfiguracion extends Vue {
  // ...

  //Centro Medico
  public selectCentroMedico = '';
  public ElementArrayCentroMedico = [];

  //Especialidad
  public selectEspecialidad = '';
  public ElementArrayEspecialidad = [];

  public ElementTelefono = ''; // Campo de teléfono

  public CorreoElement = "";
  public NuevaContraseñaElement = "";
  public CNuevaContraseñaElement = "";
  public isChecked1 = false;
  public isChecked2 = false;
  public isChecked3 = false;
  public isChecked4 = false;
  public isChecked5 = false;
  public isChecked6 = false;

    mounted(): void {
		this.getDataCentroMedico();
    this.getDataEspecialidad();
	}

  //GetData Centro Medico
  private getDataCentroMedico() {
    this.isLoading = true;
    let config = {
      method: 'get',
      url: `${process.env.VUE_APP_API_3}/centros/centro_medico`,
      headers: { Authorization: `Bearer ${this.$store.state.token}` }
    };

    axios(config)
      .then((response) => {
        this.data = response.data as Array<ILabels>;
        if (!this.selectCentroMedico) {
          this.selectCentroMedico = this.data[0].name_centro_medico; // o cualquier lógica que elijas para mantener el valor seleccionado
        }
        this.ElementArrayCentroMedico = [];
        this.data.forEach((item) => {
          // Modificar para incluir el campo value con el _id
          this.ElementArrayCentroMedico.push({ text: item.name_centro_medico, value: item.name_centro_medico });
        });
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        this.isLoading = false;
      });
  }

  // En el método saveSelectedValue
  public saveSelectedValue(event) {
    this.selectedValue = this.selectCentroMedico; // Asignar el valor de selectRegion a selectedValue
    console.log(this.selectCentroMedico); // Verificar el valor de selectRegion
  }


  //GetData Especialidad
  private getDataEspecialidad() {
    this.isLoading = true;
    let config = {
      method: 'get',
      url: `${process.env.VUE_APP_API_3}/especialidades/especialidad`,
      headers: { Authorization: `Bearer ${this.$store.state.token}` }
    };

    axios(config)
      .then((response) => {
        this.data = response.data as Array<ILabels>;
        if (!this.selectEspecialidad) {
          this.selectEspecialidad = this.data[0].especialidad; // o cualquier lógica que elijas para mantener el valor seleccionado
        }
        this.ElementArrayEspecialidad = [];
        this.data.forEach((item) => {
          // Modificar para incluir el campo value con el _id
          this.ElementArrayEspecialidad.push({ text: item.especialidad, value: item.especialidad });
        });
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        this.isLoading = false;
      });
  }

  // En el método saveSelectedValue
  public saveSelectedValueEspecialidad(event) {
    this.saveSelectedValueEspecialidad = this.selectEspecialidad; // Asignar el valor de selectRegion a selectedValue
    console.log(this.selectEspecialidad); // Verificar el valor de selectRegion
    this.getDataComuna(); // Llamar a la función para cargar las comunas al seleccionar una región
  }

  // Método para agregar prefijo de Chile al teléfono
  private agregarPrefijoChile() {
    // Verificar si el teléfono no comienza con el prefijo de Chile
    if (!this.ElemenTelefono.startsWith('+56')) {
      // Agregar el prefijo de Chile al teléfono
      this.ElementTelefono = '+56' + this.ElementTelefono;
    }
  }

  // Método para manejar el cambio en los checkboxes
  checkboxChanged(checkboxName: string) {
    console.log(`Estado de ${checkboxName}: ${this[checkboxName]}`);
    // Aquí puedes agregar cualquier lógica adicional que desees realizar al cambiar el estado del checkbox
  }



  public aggregateItem(){
      let telefono = this.ElementTelefono;
      let correo = this.CorreoElement;
      let centrosmedicos: string[] = this.selectCentroMedico;
      let especialidad = this.selectEspecialidad;
      let contraseña = this.NuevaContraseñaElement;
      let confirm_fono = this.isChecked1;
      let confirm_wsp = this.isChecked2;
      let confirm_mail = this.isChecked3;
      let list_fono = this.isChecked4;
      let list_wsp = this.isChecked5;
      let list_mail = this.isChecked6;
      let dt = JSON.stringify({
        "rut": "22282878-3",
        "nombre": "asds",
        "apellido": "sdf",
        "correo": correo,
        "telefono": telefono,
        "direccion": "dfdsfs",
        "secret": contraseña,
        "especialidad": especialidad,
        "centro_medico": [
          centrosmedicos
        ],
        "confirm_wsp": confirm_wsp,
        "confirm_mail": confirm_mail,
        "confirm_fono": confirm_fono,
        "list_wsp": list_wsp,
        "list_mail": list_mail,
        "list_fono": list_fono
      });
      let config = {
          //aqui llamamos al endpoint desde el back que necesitamos utilizar para agregar registros
          method: 'post',
          url: process.env.VUE_APP_API_4 + "/conf_medicos/conf_medico",
          data: dt,
          headers: { 
              Authorization: `Bearer ${this.$store.state.token}`,
              'Content-Type': 'application/json'
          }
      };
      axios(config)
    .then(response => {
              //this.dialog = false;
              this.ElementTelefono = "";
              this.CorreoElement = "";
              this.selectCentroMedico = "";
              this.selectEspecialidad = "";
              this.NuevaContraseñaElement = "";
              this.isChecked1 = "";
              this.isChecked2 = "";
              this.isChecked3 = "";
              this.isChecked4 = "";
              this.isChecked5 = "";
              this.isChecked6 = "";
              this.getDataCentroMedico();
    })
    .catch(error => {
      console.error(error);
    });
  }
}
</script>
