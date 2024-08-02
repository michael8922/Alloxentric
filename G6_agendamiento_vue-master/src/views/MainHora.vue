<template>
  <!-- Begin Page Content -->
  <div class="container-fluid cont-all bg-all">
    <!-- Page Heading -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">Guardar Hora</h1>
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
                      'inactive': isPastDate(day),
                      'active': isSelectedDate(day),
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
        <div class="card shadow mb-4">
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">Horario</h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-log-12 mt-4">
                <div v-if="MensajeExitoso" class="alert alert-success alert-dismissible fade show">
                  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                  {{ MensajeExitoso }}
                </div>
                <div v-if="MensajeError" class="alert alert-danger">
                  {{ MensajeError }}
                </div>
                <div class="button-container" id="buttonContainer">
                  <button
                    class="btn btn-hora"
                    v-for="button in times"
                    :value="button.value"
                    :key="button.value"
                    @click="toggleHourSelection(button.value)"
                    :class="{ selected: selectedHours.includes(button.value) }"
                    style="background-color: #06b7b"
                  >
                    {{ button.text }}
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-lg-12">
                <form class="user">
                  <div class="form-group">
                    <select
                      class="custom-select form-control form-control-user"
                      id="ElementArrayCentroMedico"
                      v-model="selectCentroMedico"
                      @change="saveSelectedValue"
                      required
                    >
                      <option
                        class="alert-success font-weight-bold p-1"
                        value=""
                        disabled
                        selected
                      >
                        Seleccione un centro medico
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
                  </div>
                </form>
              </div>
            </div>
            <button
              type="button"
              class="btn btn-primary btn-lg btn-block mt-4"
              @click="sendSelectedDateTime()"
            >
              Guardar
            </button>
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
  name: "MainHora",
})
export default class MainHora extends Vue {

  selectCentroMedico = "";
  ElementArrayCentroMedico = [];
  times = [];
  selectedHours = [];
  selectedDateTime: { fecha: string; hora: string }[] = [];
  selectedDateObjects = [];
  RuteEpecialidad = "";
  MensajeError = "";
  MensajeExitoso = "";
  selectedDates = {}; // Hacer que selectedDates sea reactivo

  data() {
    return {
      currYear: new Date().getFullYear(),
      currMonth: new Date().getMonth(),
      // ... otras propiedades ...
      selectedDates: {}, // Inicializa selectedDates aquí
    };
  }



  mounted(): void {
    this.initializeData();
    this.renderCalendar();
  }

  private initializeData(): void {
    this.getEspecialidad();
    this.getDataCentroMedico();
    this.getDataHora();
    this.toggleHourSelection();
    this.setupPrevNextIconClick();
    this.setupConfirmationButtonClick();
    this.sendSelectedDateTime();
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
    const daysInMonth = new Date(this.currYear, this.currMonth + 1, 0).getDate();
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
    let lastDateOfMonth = new Date(this.currYear, this.currMonth + 1, 0).getDate(); // Obtener el último día del mes

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
    this.currentDate.innerText = `${this.months[this.currMonth]} ${this.currYear}`;
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

  private toggleHourSelection(hourValue) {
    // Verificar si la hora ya está seleccionada y actualizar selectedHours
    const index = this.selectedHours.indexOf(hourValue);
    if (hourValue && index === -1) {
      this.selectedHours.push(hourValue);
    } else if (hourValue && index !== -1) {
      this.selectedHours.splice(index, 1);
    }

    // Luego de actualizar las horas seleccionadas, actualiza el array de objetos seleccionados
    this.updateSelectedDateObjects();
  }

  private updateSelectedDateObjects() {
    // Limpia el array para reconstruirlo
    this.selectedDateObjects = [];

    // Combina las fechas y horas seleccionadas para crear el array
    Object.keys(this.selectedDates).forEach((key) => {
      this.selectedDates[key].forEach((date) => {
        const formattedDate = this.formatDate(date, key);

        // Verifica si hay horas y un centro médico seleccionados
        if (this.selectedHours.length === 0 || this.selectCentroMedico === "") {
          this.MensajeError = "Por favor seleccione una o mas horas y un centro medico.";
        } else {
          // Si ambos están seleccionados, limpia el mensaje de error
          this.MensajeError = "";
          this.selectedHours.forEach((hour) => {
            this.selectedDateObjects.push({
              fecha: formattedDate,
              hora: hour,
            });
          });
        }
      });
    });

    console.log("Fechas y horas seleccionadas:", this.selectedDateObjects);
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

  private getEspecialidad() {
    console.log("getEspecialidad está siendo llamado");
    this.isLoading = true;
    let config = {
      method: "get",
      url: `${process.env.VUE_APP_API_4}/conf_medicos/conf_medico/${this.$store.state.tokenParsed.preferred_username}`,
      headers: { Authorization: `Bearer ${this.$store.state.token}` },
    };

    axios(config)
      .then((response) => {
        const especialidadData = response.data;
        if (especialidadData && especialidadData.especialidad) {
          this.RuteEpecialidad = especialidadData.especialidad; // Asignar directamente la especialidad a la variable
          console.log("RUT:", this.$store.state.tokenParsed.preferred_username); // Imprimir el RUT
          console.log("Especialidad:", this.RuteEpecialidad); // Imprimir la especialidad
        } else {
          console.error("Especialidad no encontrada en los datos.");
          this.especialidad = ""; // Asegurar que especialidad es una variable y no un array
        }
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        this.isLoading = false;
      });
  }

  private sendSelectedDateTime(): void {
    console.log("Mensaje: ", this.selectedDateObjects);
    this.selectedDateObjects.forEach((selectedDateTime) => {
      // Aquí puedes incluir los campos adicionales junto con fecha y hora
      const dataToSend = {
        correo: "",
        telefono: "",
        rut: "",
        prevision: "",
        centro_medico: this.selectCentroMedico,
        especialidad: this.RuteEpecialidad,
        nombre_medico: this.$store.state.tokenParsed.name,
        nombre_paciente: "",
        fecha: selectedDateTime.fecha,
        hora: selectedDateTime.hora,
        rut_medico: this.$store.state.tokenParsed.preferred_username,
        //...this.selectedDateTime,
      };

      let dt = JSON.stringify(dataToSend);

      let config = {
        method: "post",
        url: process.env.VUE_APP_API_4 + "/conf_medicos/crear_hora", // Reemplaza 'URL_DEL_ENDPOINT' con la URL correcta del servidor
        data: dt,
        headers: {
          Authorization: `Bearer ${this.$store.state.token}`,
          "Content-Type": "application/json",
        },
      };

      axios(config)
        .then((response) => {
          console.log("Datos enviados con éxito.");
          this.selectedDateTime = "";
          this.MensajeExitoso = "Los datos se guardaron exitosamente en el sistema.";

          // Limpia el calendario, las horas y el centro médico seleccionado
          this.selectedHours = []; // Limpia las horas seleccionadas
          this.selectCentroMedico = ""; // Limpia el centro médico seleccionado
          this.selectedDates = {}; // Limpia las fechas seleccionadas en el calendario
          this.selectedDateObjects = []; // Limpia los objetos de fecha y hora seleccionados

          this.selectionMessage = "";

        })
        .catch((error) => {
          console.error("Error al enviar los datos:", error);
          this.MensajeExitoso = "Ocurrió un error al guardar los datos."; // Mensaje para un error
        });
    });
  }

  //GetData Centro Medico
  private getDataCentroMedico() {
    this.isLoading = true;
    let config = {
      method: "get",
      url: `${process.env.VUE_APP_API_3}/centros/centro_medico`,
      headers: { Authorization: `Bearer ${this.$store.state.token}` },
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
          this.ElementArrayCentroMedico.push({
            text: item.name_centro_medico,
            value: item.name_centro_medico,
          });
        });
        this.selectCentroMedico = "";
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
    //this.getDataComuna(); // Llamar a la función para cargar las comunas al seleccionar una región

    this.updateSelectedDateObjects();
  }

  //GetData Hora
  private getDataHora() {
    this.isLoading = true;
    let config = {
      method: "get",
      url: `${process.env.VUE_APP_API_3}/horas/hora`,
      headers: { Authorization: `Bearer ${this.$store.state.token}` },
    };

    axios(config)
      .then((response) => {
        this.data = response.data as Array<ILabels>;
        this.selectHora = this.data[0].hora; // o cualquier lógica que elijas para mantener el valor seleccionado
        this.times = [];
        this.data.forEach((item) => {
          // Modificar para incluir el campo value con el _id
          this.times.push({ text: item.hora, value: item.hora });
        }, console.log(this.times));
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        this.isLoading = false;
      });
  }

}
</script>
