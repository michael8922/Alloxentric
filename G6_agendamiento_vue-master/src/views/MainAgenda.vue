<template>
  <!-- Begin Page Content -->
  <div class="container-fluid cont-all bg-all">
    <!-- Page Heading -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">Agenda</h1>
    </div>

    <!-- Content Row -->
    <div class="row">
      <!-- Content Column -->
      <div class="col-lg-6 mb-4">
        <!-- Project Card Example -->
        <div class="card shadow mb-4">
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">Calendario</h6>
          </div>
          <div class="card-body">
            <div class="wrapper">
              <div class="calendar">
                <header>
                  <p class="current-date">
                    {{ currentMonthName }} {{ currYear }}
                  </p>
                  <div class="icons">
                    <span
                      id="prev"
                      class="material-symbols-rounded"
                      @click="changeMonth(-1)"
                      >chevron_left</span
                    >
                    <span
                      id="next"
                      class="material-symbols-rounded"
                      @click="changeMonth(1)"
                      >chevron_right</span
                    >
                  </div>
                </header>
                <ul class="weeks">
                  <li>Lun</li>
                  <li>Mar</li>
                  <li>Mie</li>
                  <li>Jue</li>
                  <li>Vie</li>
                  <li>Sab</li>
                  <li>Dom</li>
                </ul>
                <ul class="days">
                  <li
                    v-for="day in getDaysArray"
                    :key="day"
                    @click="!isPastDate(day) && toggleDate(day)"
                    :class="{
                      inactive: isPastDate(day),
                      active: isSelectedDate(day),
                      'current-day': isToday(day),
                    }"
                  >
                    {{ day }}
                    <span v-if="isToday(day)" class="dot"></span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-6 mb-4">
        <!-- Illustrations -->
        <div class="card shadow mb-4">
          <div
            class="card-header py-3 d-flex justify-content-between align-items-center"
          >
            <h6 class="m-0 font-weight-bold text-primary">Listado de citas</h6>
            <a
              type="button"
              class="btn btn-danger"
              data-toggle="modal"
              data-target="#VerDatoModal"
              @click="showModal = true"
            >
              Cancelar citas
            </a>
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
                    <th>Fecha de la cita</th>
                    <th>Hora de la cita</th>
                    <th>Paciente</th>
                    <th>Contacto</th>
                    <th>
                      <input
                        type="checkbox"
                        v-model="selectAll"
                        @change="toggleAllChecks"
                      />
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(paciente, index) in datosPaciente"
                    :key="index"
                    class="table-link"
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
                    <td>{{ paciente.fecha }}</td>
                    <td>{{ paciente.hora }}</td>
                    <td>{{ paciente.nombre_paciente }}</td>
                    <td>{{ paciente.telefono }}</td>
                    <td>
                      <input
                        type="checkbox"
                        v-model="paciente.isSelected"
                        :disabled="paciente.status === 'cancelada'"
                        @change="updateSelectedOrders(paciente)"
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
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
      v-if="showModal"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">
              <strong>{{ this.$store.state.tokenParsed.name }}</strong>
            </h5>
          </div>
          <div class="modal-body">
            <div class="box-nro">
              ¿Estás seguro de querer cancelar las citas seleccionadas?
            </div>
          </div>
          <div class="modal-footer">
            <button
              class="btn btn-secondary"
              type="button"
              data-dismiss="modal"
            >
              Cancel
            </button>
            <a class="btn btn-primary" data-dismiss="modal"  @click="actualizarEstado()">Confirmar</a>
          </div>
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
  name: "MainAgenda",
})
export default class MainAgenda extends Vue {
  public message = this.$t("Main.message");

  public selectedDateObjects = [];
  public MensajeError = "";
  public selectedDates = {};
  public datosPaciente = [];
  public selectAll = false;
  public selectedOrders = [];

  data() {
    return {
      currYear: new Date().getFullYear(),
      currMonth: new Date().getMonth(),
      // ... otras propiedades ...
      selectedDates: {}, // Inicializa selectedDates aquí
      showModal: false,
    };
  }

  mounted(): void {
    this.initializeData();
    this.renderCalendar();
  }

  private initializeData(): void {
    this.setupPrevNextIconClick();
    this.obtenerCalendarioPorRut();
  }

  @Watch("selectedDateObjects")
  onFechaInicioChanged(newVal: string, oldVal: string) {
    if (newVal !== oldVal) {
      this.obtenerCalendarioPorRut();
      this.actualizarEstado();
    }
  }

  // Propiedad computada para mostrar el nombre del mes actual
  get currentMonthName() {
    const months = [
      "Enero",
      "Febrero",
      "Marzo",
      "Abril",
      "Mayo",
      "Junio",
      "Julio",
      "Augosto",
      "Septiembre",
      "Octubre",
      "Noviembre",
      "Diciembre",
    ];
    return months[this.currMonth];
  }

  // Método para cambiar de mes
  changeMonth(step) {
    this.currMonth += step;

    if (this.currMonth < 0) {
      this.currMonth = 11;
      this.currYear--;
    } else if (this.currMonth > 11) {
      this.currMonth = 0;
      this.currYear++;
    }

    // Forzar una actualización del componente para asegurarse de que Vue detecte el cambio
    this.$forceUpdate();

    // Si renderCalendar() es el método que actualiza el calendario, asegúrate de llamarlo aquí
    this.renderCalendar();
  }

  // Método para obtener un array de días para el calendario
  get getDaysArray() {
    const daysInMonth = new Date(
      this.currYear,
      this.currMonth + 1,
      0
    ).getDate();
    console.log(`Días en el mes: ${daysInMonth}`); // Debug: imprimir los días en el mes
    console.log("Mes: ", this.currMonth);

    return Array.from({ length: daysInMonth }, (_, i) => i + 1);
  }

  // Método para verificar si un día está seleccionado
  isSelectedDate(day) {
    const key = `${this.currYear}-${this.currMonth + 1}`;
    return this.selectedDates[key] && this.selectedDates[key].includes(day);
  }

  // Método para verificar si el día es hoy y así ponerle un punto
  isToday(day) {
    const today = new Date();
    const dateToCheck = new Date(this.currYear, this.currMonth, day);
    return (
      dateToCheck.getDate() === today.getDate() &&
      dateToCheck.getMonth() === today.getMonth() &&
      dateToCheck.getFullYear() === today.getFullYear()
    );
  }

  // Método para verificar si un día es anterior al día actual
  private isPastDate(date) {
    const today = new Date();
    const dateToCheck = new Date(this.currYear, this.currMonth, date);
    return dateToCheck < today;
  }

  private renderCalendar(): void {
    let today = new Date(); // Obtener la fecha actual
    let firstDayOfMonth = new Date(this.currYear, this.currMonth, 1).getDay(); // Obtener el primer día del mes
    let lastDateOfMonth = new Date(
      this.currYear,
      this.currMonth + 1,
      0
    ).getDate(); // Obtener el último día del mes

    let liTag = "";

    // Ajustar el inicio del calendario basado en el primer día del mes
    for (let i = 0; i < firstDayOfMonth; i++) {
      liTag += `<li class="inactive"></li>`; // Espacios vacíos para los días que no pertenecen al mes actual
    }

    for (let i = 1; i <= lastDateOfMonth; i++) {
      let isPast = this.isPastDate(i);
      let isToday =
        i === today.getDate() &&
        this.currMonth === today.getMonth() &&
        this.currYear === today.getFullYear();
      let isSelected = this.isSelectedDate(i);

      liTag += `<li class="${isSelected ? "active" : ""} ${
        isPast ? "past" : ""
      } ${isToday ? "today" : ""}"
                    :data-date="${i}"
                    :class="{ 'active': isSelectedDate(i), 'past': isPastDate(i), 'today': isToday }"
                    @click="isPast ? null : toggleDate(i)">
                ${i}
                ${isToday ? '<span class="dot"></span>' : ""}
              </li>`;
    }

    this.daysTag.innerHTML = liTag;

    // Asegúrate de que 'this.months' esté correctamente definido y tenga todos los meses
    this.currentDate.innerText = `${this.months[this.currMonth]} ${
      this.currYear
    }`;
  }

  private toggleDate(date) {
    if (!this.isPastDate(date)) {
      const key = `${this.currYear}-${this.currMonth + 1}`;
      if (!this.selectedDates[key]) {
        this.$set(this.selectedDates, key, []);
      }

      const dateIndex = this.selectedDates[key].indexOf(date);
      if (dateIndex >= 0) {
        this.selectedDates[key].splice(dateIndex, 1);
      } else {
        this.selectedDates[key].push(date);
      }

      this.updateSelectedDateObjects();
    }
  }

  private updateSelectedDateObjects() {
    // Limpia el array para reconstruirlo
    this.selectedDateObjects = [];

    // Combina las fechas y horas seleccionadas para crear el array
    Object.keys(this.selectedDates).forEach((key) => {
      this.selectedDates[key].forEach((date) => {
        const formattedDate = this.formatDate(date, key);

        // Si ambos están seleccionados, limpia el mensaje de error
        this.selectedDateObjects.push({
          fecha: formattedDate,
        });
      });
    });
  }

  private formatDate(date, key) {
    const [year, month] = key.split("-");
    const formattedMonth = month.padStart(2, "0");
    const formattedDay = date.toString().padStart(2, "0");
    return `${year}-${formattedMonth}-${formattedDay}`;
  }

  private setupPrevNextIconClick() {
    const prevNextIcon = document.querySelectorAll(".icons span");
    prevNextIcon.forEach((icon) => {
      icon.addEventListener("click", () => {
        const step = icon.id === "prev" ? -0 : 0;
        this.changeMonth(step);
      });
    });
  }

  async obtenerCalendarioPorRut() {
    this.isLoading = true;

    let fechasFormateadas = [];

    if (
      !Array.isArray(this.selectedDateObjects) ||
      this.selectedDateObjects.length === 0
    ) {
      // Si no hay fechas seleccionadas, establecer la fecha actual como la fecha por defecto
      const today = new Date();
      const formattedToday = `${today.getFullYear()}-${(today.getMonth() + 1)
        .toString()
        .padStart(2, "0")}-${today.getDate().toString().padStart(2, "0")}`;

      fechasFormateadas.push(formattedToday);
    } else {
      fechasFormateadas = this.selectedDateObjects.map(
        (fechaObj) => fechaObj.fecha
      );
    }

    console.log("Fechas formateadas: ", fechasFormateadas);

    const queryParams = new URLSearchParams();
    queryParams.append(
      "rut_medico",
      this.$store.state.tokenParsed.preferred_username
    );

    fechasFormateadas.forEach((fecha) => {
      queryParams.append("fecha", fecha);
    });

    console.log("QueryParams: ", queryParams);

    const url = `${
      process.env.VUE_APP_API_4
    }/conf_medicos/calendarioAgenda?${queryParams.toString()}`;

    const config = {
      method: "get",
      url: url,
      headers: { Authorization: `Bearer ${this.$store.state.token}` },
    };

    console.log("Fechas:", fechasFormateadas);

    try {
      const response = await axios(config);
      console.log("Datos recibidos de la API:", response.data);

      if (Array.isArray(response.data)) {
        console.log("Número de citas recibidas:", response.data.length);
        this.datosPaciente = response.data.map((item) => ({
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
          isSelected: false,
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

  private colorEstado(estado) {
    if (estado === "confirmada") {
      return "#28a745";
    } else if (estado === "reservada") {
      return "#ffc107";
    } else if (estado === "cancelada") {
      return "#dc3545";
    } else if (estado === "disponible") {
      return "#36b9cc";
    }
    return "#000"; // Color por defecto para otros estados
  }

  private toggleAllChecks() {
    if (this.selectAll) {
      // Seleccionar todos los checkboxes y guardar todos los números de orden
      this.selectedOrders = this.datosPaciente.map(
        (paciente) => paciente.nro_orden
      );
    } else {
      // Deseleccionar todos los checkboxes y vaciar los números de orden
      this.selectedOrders = [];
    }

    console.log("Selected orders after toggling all:", this.selectedOrders);

    this.datosPaciente.forEach((paciente) => {
      paciente.isSelected = this.selectAll;
    });
  }

  private updateSelectedOrders(paciente) {
    if (paciente.isSelected) {
      // Agregar el número de orden si la cita está seleccionada
      this.selectedOrders.push(paciente.nro_orden);
    } else {
      // Remover el número de orden si la cita no está seleccionada
      const index = this.selectedOrders.indexOf(paciente.nro_orden);
      if (index !== -1) {
        this.selectedOrders.splice(index, 1);
      }
    }

    console.log("Selected orders:", this.selectedOrders);
    // Actualizar el estado del checkbox 'seleccionar todos' en base a si todos los checkboxes individuales están marcados
    this.selectAll = this.datosPaciente.every(
      (paciente) => paciente.isSelected
    );
  }

  public actualizarEstado() {
    let orderNumbers = this.selectedOrders;
    console.log("Numero de orden: ", orderNumbers);

    let config = {
      method: "put",
      headers: {
        Authorization: `Bearer ${this.$store.state.token}`,
        "Content-Type": "application/json",
      },
    };

    let promises = orderNumbers.map((orderNumber) => {
      return axios.put(
        `${process.env.VUE_APP_API_4}/conf_medicos/update_cancelado/${orderNumber}`,
        {},
        config
      );
    });

    Promise.all(promises)
      .then((responses) => {

        // Actualiza la tabla de citas aquí
        // Si necesitas llamar a la API para actualizar la lista de citas, hazlo aquí
        // Si no, actualiza directamente el estado local de las citas
        this.datosPaciente = this.datosPaciente.map((paciente) => {
          if (orderNumbers.includes(paciente.nro_orden)) {
            return { ...paciente, status: "cancelada" };
          }
          return paciente;
        });

        // Limpia los órdenes seleccionados y resetea 'selectAll'
        this.showModal = false; // Esto cerrará el modal
        this.selectedOrders = [];
        this.selectAll = false;


        // Refresca los datos de la tabla si es necesario
        this.obtenerCalendarioPorRut();
      })
      .catch((error) => {
        console.error("Error al actualizar estados:", error);
      });
  }
}
</script>
