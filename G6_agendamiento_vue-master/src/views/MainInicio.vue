<template>
  <!-- Begin Page Content -->
  <div class="container-fluid cont-all bg-all">
    <!-- Content Row -->
    <div class="row">
      <!-- Resumen de Citas -->
      <div class="col-lg-6">
        <!-- Page Heading -->
        <div
          class="d-sm-flex align-items-center justify-content-between mb-4 mt-4"
        >
          <h1 class="h3 mb-0 text-gray-800">Resumen Citas</h1>
        </div>
        <div class="row">
          <div class="col-xl-12 col-md-6 mb-12">
            <div class="row">
              <div class="col-md-4 mb-6">
                <label for="fechaInicio" class="col-12 col-form-label"
                  >Fecha inicial</label
                >
                <div class="col-12">
                  <div class="input-group date" id="datepickerInicio">
                    <input
                      type="date"
                      class="form-control"
                      id="fechaInicio"
                      v-model="fechaInicio"
                    />
                  </div>
                </div>
              </div>

              <div class="col-md-4 mb-6">
                <label for="fechaFin" class="col-12 col-form-label"
                  >Fecha final</label
                >
                <div class="col-12">
                  <div class="input-group date" id="datepickerFin">
                    <input
                      type="date"
                      class="form-control"
                      id="fechaFin"
                      v-model="fechaFin"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- ... Otros elementos ... -->

          <!-- Card Total de Citas Agendadas -->
          <div class="col-xl-4 col-md-6 mb-12">
            <div class="card border-left-warning shadow h-100 py-2">
              <div class="card-body">
                <div class="row no-gutters align-items-center">
                  <div class="col mr-2">
                    <div
                      class="text-xs font-weight-bold text-warning text-uppercase mb-1"
                    >
                      Total citas agendadas
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-gray-800">
                      {{ totalCitasReservadas }}
                    </div>
                  </div>
                  <div class="col-auto">
                    <i class="fas fa-calendar fa-2x text-gray-300"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Card Total de Citas Confirmadas -->
          <div class="col-xl-4 col-md-6 mb-12">
            <div class="card border-left-success shadow h-100 py-2">
              <div class="card-body">
                <div class="row no-gutters align-items-center">
                  <div class="col mr-2">
                    <div
                      class="text-xs font-weight-bold text-success text-uppercase mb-1"
                    >
                      Total citas confirmadas
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-gray-800">
                      {{ totalCitasConfirmadas }}
                    </div>
                  </div>
                  <div class="col-auto">
                    <i class="fa-solid fa-user fa-2x text-gray-300"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Card Total de Citas Canceladas -->
          <div class="col-xl-4 col-md-6 mb-12">
            <div class="card border-left-danger shadow h-100 py-2">
              <div class="card-body">
                <div class="row no-gutters align-items-center">
                  <div class="col mr-2">
                    <div
                      class="text-xs font-weight-bold text-danger text-uppercase mb-1"
                    >
                      Total citas canceladas
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-gray-800">
                      {{ totalCitasCanceladas }}
                    </div>
                  </div>
                  <div class="col-auto">
                    <i class="fas fa-times-circle fa-2x text-gray-300"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Card Total de Citas Confirmadas -->
          <div class="col-xl-4 col-md-6 mb-12">
            <div class="card border-left-info shadow h-100 py-2">
              <div class="card-body">
                <div class="row no-gutters align-items-center">
                  <div class="col mr-2">
                    <div
                      class="text-xs font-weight-bold text-info text-uppercase mb-1"
                    >
                      Total citas disponibles
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-gray-800">
                      {{ totalCitasDisponibles }}
                    </div>
                  </div>
                  <div class="col-auto">
                    <i class="fas fa-check-circle fa-2x text-gray-300"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Resumen de pagos -->
          <div class="col-xl-12">
            <!-- Page Heading -->
            <div
              class="d-sm-flex align-items-center justify-content-between mb-4 mt-4"
            >
              <h1 class="h3 mb-0 text-gray-800">Resumen de Pagos</h1>
            </div>

            <div class="row">
              <!-- Earnings (Monthly) Card Example -->
              <div class="col-xl-6 col-md-6 mb-12">
                <div class="card border-left-primary shadow h-100 py-2">
                  <div class="card-body">
                    <div class="row no-gutters align-items-center">
                      <div class="col mr-2">
                        <div
                          class="text-xs font-weight-bold text-primary text-uppercase mb-1"
                        >
                          Total citas pagadas
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">
                          70
                        </div>
                      </div>
                      <div class="col-auto">
                        <i class="fas fa-calendar fa-2x text-gray-300"></i>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Earnings (Monthly) Card Example -->
              <div class="col-xl-6 col-md-6 mb-12">
                <div class="card border-left-success shadow h-100 py-2">
                  <div class="card-body">
                    <div class="row no-gutters align-items-center">
                      <div class="col mr-2">
                        <div
                          class="text-xs font-weight-bold text-success text-uppercase mb-1"
                        >
                          Total monto pagado
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">
                          $23.000.000
                        </div>
                      </div>
                      <div class="col-auto">
                        <i class="fas fa-dollar-sign fa-2x text-gray-300"></i>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Dashboard -->
      <div class="col-lg-6">
        <div class="row">
          <div class="col-lg-12 mb-12">
            <!-- Project Card Example -->
            <div class="card shadow mb-4">
              <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">
                  Lista de pacientes
                </h6>
              </div>
              <div class="card-body">
                <div class="table-responsive">
                  <table
                    class="table table-bordered"
                    id="dataTable"
                    width="100%"
                    cellspacing="0"
                  >
                    <thead>
                      <tr>
                        <th>Estado</th>
                        <th>Nombre paciente</th>
                        <th>Fecha de atención</th>
                        <th>Hora de atención</th>
                        <th>Previsión</th>
                        <th>Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="(paciente, index) in datosPaciente"
                        :key="index"
                      >
                        <td>
                          <span
                            class="status-dot"
                            :style="{
                              backgroundColor: colorEstado(paciente.status),
                            }"
                          ></span>
                          {{ paciente.status }}
                        </td>
                        <td>{{ paciente.nombre_paciente }}</td>
                        <td>{{ paciente.fecha }}</td>
                        <td>{{ paciente.hora }}</td>
                        <td>{{ paciente.prevision }}</td>
                        <td>
                          <button
                            type="submit"
                            class="btn btn-primary btn-block"
                            data-toggle="modal"
                            data-target="#VerDatoModal"
                            @click="seleccionPaciente(paciente)"
                          >
                            Ver datos
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Ver Dato Modal-->
    <div
      class="modal fade"
      id="VerDatoModal"
      tabindex="-1"
      role="dialog"
      aria-labelledby="VerDatoModal"
      aria-hidden="true"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">
              Datos de <strong>{{ pacienteActual.nombre_paciente }}</strong>
            </h5>
            <button
              class="close"
              type="button"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">×</span>
            </button>
          </div>
          <div class="modal-body">
            <p><strong>Rut: </strong> {{ pacienteActual.rut }}</p>
            <p><strong>Correo: </strong> {{ pacienteActual.correo }}</p>
            <p><strong>Telefono: </strong> {{ pacienteActual.telefono }}</p>
            <p><strong>Previsión: </strong> {{ pacienteActual.prevision }}</p>
            <p>
              <strong>Fecha de atención: </strong> {{ pacienteActual.fecha }}
            </p>
            <p><strong>Hora de atención: </strong> {{ pacienteActual.hora }}</p>
            <p>
              <strong>estado: </strong> {{ pacienteActual.status }}
            </p>
            <p>
              <strong>Centro Medico: </strong>
              {{ pacienteActual.centro_medico }}
            </p>
            <div class="PacienteModal">
              <strong> N° de Orden: {{ pacienteActual.nro_orden }} </strong>
            </div>
          </div>
          <!-- 
                <div class="modal-footer">
                    <button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>
                    <a class="btn btn-primary" href="login.html">Salir</a>
                </div>
                -->
        </div>
      </div>
    </div>
  </div>
  <!-- /.container-fluid -->
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { ILabels } from "@/model/main/Ilabels";
import axios from "axios";

@Component({
  name: "MainInicio",
})
export default class MainInicio extends Vue {
  public isLoading = false;
  public totalCitasReservadas = 0;
  public totalCitasConfirmadas = 0;
  public totalCitasCanceladas = 0;
  public totalCitasDisponibles = 0;
  public fechaInicio = "";
  public fechaFin = "";
  public hora = [];
  public nombre = [];
  public especialidad = [];
  public prevision = [];
  public datosPaciente = [];
  public pacienteActual = [];

  mounted() {
    if (!this.fechaInicio) {
      const hoy = new Date();
      let fechaActual = `${hoy.getFullYear()}-${(hoy.getMonth() + 1)
        .toString()
        .padStart(2, "0")}-${hoy.getDate().toString().padStart(2, "0")}`;
      this.fechaInicio = fechaActual;
    }

    // Calcula la fecha final del mes actual
    const hoy = new Date();
    const primerDiaDelSiguienteMes = new Date(
      hoy.getFullYear(),
      hoy.getMonth() + 1,
      1
    );
    const ultimoDiaDelMes = new Date(primerDiaDelSiguienteMes - 1);

    let fechaFinalDelMes = `${ultimoDiaDelMes.getFullYear()}-${(
      ultimoDiaDelMes.getMonth() + 1
    )
      .toString()
      .padStart(2, "0")}-${ultimoDiaDelMes
      .getDate()
      .toString()
      .padStart(2, "0")}`;

    this.fechaFin = fechaFinalDelMes;

    this.fechaInicio = this.fechaInicio || this.fechaInicio;
    this.fechaFin = this.fechaFin || this.fechaFinalDelMes;
    this.getDataTotalCitas();
    this.obtenerCalendarioPorRut();
  }

  @Watch("fechaInicio")
  onFechaInicioChanged(newVal: string, oldVal: string) {
    if (newVal !== oldVal) {
      this.getDataTotalCitas();
      this.obtenerCalendarioPorRut();
    }
  }

  @Watch("fechaFin")
  onFechaFinChanged(newVal: string, oldVal: string) {
    if (newVal !== oldVal) {
      this.getDataTotalCitas();
      this.obtenerCalendarioPorRut();
    }
  }

  private getDataTotalCitas() {
    // Si alguna de las fechas es vacía, no hacer la llamada
    if (!this.fechaInicio || !this.fechaFin) return;

    const fechaInicioFormatoAPI = this.fechaInicio; // Asumiendo que ya está en formato 'YYYY-MM-DD'
    const fechaFinFormatoAPI = this.fechaFin;

    let config = {
      method: "get",
      url: `${process.env.VUE_APP_API_4}/conf_medicos/countStatus/${this.$store.state.tokenParsed.preferred_username}/${fechaInicioFormatoAPI}/${fechaFinFormatoAPI}`,
      headers: { Authorization: `Bearer ${this.$store.state.token}` },
    };

    axios(config)
      .then((response) => {
        const data = response.data;
        this.totalCitasReservadas = data.reservada;
        this.totalCitasConfirmadas = data.confirmada;
        this.totalCitasCanceladas = data.cancelada;
        this.totalCitasDisponibles = data.disponible;
      })
      .catch((error) => {
        console.error(error);
      });
  }

  private convertirFormatoFecha(fecha: string): string {
    if (!fecha) return "";
    // No es necesario cambiar el formato si ya está en "YYYY-MM-DD"
    return fecha;
  }

  async obtenerCalendarioPorRut() {
    this.isLoading = true;

    if (!this.fechaInicio || !this.fechaFin) {
      console.log("Fechas de inicio o fin no definidas.");
      this.isLoading = false;
      return;
    }

    const config = {
      method: "get",
      url: `${process.env.VUE_APP_API_4}/conf_medicos/calendarioFiltroRut/${this.$store.state.tokenParsed.preferred_username}/${this.fechaInicio}/${this.fechaFin}?fecha_inicial=${this.fechaInicio}&fecha_termino=${this.fechaFin}`,
      headers: { Authorization: `Bearer ${this.$store.state.token}` },
    };

    console.log("Fecha final Metodo2:", this.fechaFin);
    console.log("Fecha inicio Metodo2:", this.fechaInicio);

    try {
      const response = await axios(config);
      console.log("Datos recibidos de la API:", response.data);

      // Depuración: Verifica si la respuesta es un array y tiene más de un objeto
      if (Array.isArray(response.data)) {
        console.log("Número de citas recibidas:", response.data.length);
        this.datosPaciente = response.data.map((item) => ({
          // Mapeo de la respuesta a la estructura que necesita tu tabla
          correo: item.correo,
          telefono: item.telefono,
          rut: item.rut,
          prevision: item.prevision,
          centro_medico: item.centro_medico,
          especialidad: item.especialidad,
          nombre_paciente: item.nombre_paciente,
          fecha: item.fecha,
          hora: item.hora,
          status: item.status,
          nro_orden: item.nro_orden,
        }));
      } else {
        console.error("La respuesta no es un array:", response.data);
      }
    } catch (error) {
      console.error("Error al hacer la llamada a la API:", error);
    } finally {
      this.isLoading = false;
    }
  }

  private seleccionPaciente(paciente) {
    this.pacienteActual = paciente;
  }

  private colorEstado(estado) {
    if (estado === "confirmada") {
      return "#28a745"; // Verde de Bootstrap text-success
    } else if (estado === "reservada") {
      return "#ffc107"; // Amarillo de Bootstrap text-warning
    } else if (estado === "cancelada") {
      return "#dc3545"; // Rojo de Bootstrap text-danger
    }
    return "#000"; // Color por defecto para otros estados
  }
}
</script>
