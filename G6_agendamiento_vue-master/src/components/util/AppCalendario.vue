<template>
  <!-- Begin Page Content -->
  <!-- Content Row -->
  <div class="row">
    <!-- Content Column -->
    <div class="col-lg-12 mt-4">
      <!-- Project Card Example -->
      <div class="card shadow">
        <div class="card-body">
          <div class="wrapper">
            <div class="calendar">
              <header>
                <!-- Aquí se muestra el mes y año actual -->
                <p class="current-date">{{ currentDate }}</p>
                <div class="icons">
                  <!-- Métodos actualizados para cambiar de mes -->
                  <span
                    @click="changeMonth(false)"
                    class="material-symbols-rounded"
                    >chevron_left</span
                  >
                  <span
                    @click="changeMonth(true)"
                    class="material-symbols-rounded"
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
                <li v-for="day in days" 
                    :key="day ? `day-${day}` : `empty-${Math.random()}`"
                    :class="{ 
                      'inactive': !day || !isDateAvailable(day) || isBeforeToday(day),
                      'active': day && isSelected(day) && isDateAvailable(day),
                      'today': day && isToday(day)
                    }" 
                    @click="day && isDateAvailable(day) && !isBeforeToday(day) && toggleDate(day)">
                  <span class="day-number">{{ day }}</span>
                  <span v-if="day && isToday(day)" class="dot"></span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- /.container-fluid -->
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
// Importa cualquier otro recurso o tipo que necesites.

@Component({
  name: "AppCalendario",
})
export default class AppCalendario extends Vue {
  @Prop({ required: true, type: Array }) readonly fechasDisponibles!: {
    text: string;
    value: string;
  }[];

  public days: (number | null)[] = []; // Modificado para aceptar números o null.
  public currentDate = ""; // Asegúrate de declarar todas las propiedades que usarás.
  private currYear = new Date().getFullYear();
  private currMonth = new Date().getMonth();
  public today = new Date().getDate(); // Almacenar el día actual también
  public userSelectedDate: string | null = null;

  private get currYear(): number {
    return new Date().getFullYear();
  }

  private get currMonth(): number {
    return new Date().getMonth();
  }

  private get months(): string[] {
    return [
      "Enero",
      "Febrero",
      "Marzo",
      "Abril",
      "Mayo",
      "Junio",
      "Julio",
      "Agosto",
      "Septiembre",
      "Octubre",
      "Noviembre",
      "Diciembre",
    ];
  }

  mounted(): void {
    this.renderCalendar();
  }

private toggleDate(day: number): void {
  const dateStr = `${this.currYear}-${String(this.currMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

  if (this.userSelectedDate === dateStr) {
    // Si la fecha ya estaba seleccionada, deseleccionar
    this.userSelectedDate = null;
  } else {
    // Si es una nueva selección, establecer la fecha seleccionada y emitir el evento
    this.userSelectedDate = dateStr;
    const formattedDate = this.formatDate(dateStr); // Formatear la fecha antes de emitirla
    this.$emit('date-selected', formattedDate);
  }
}


private formatDate(dateStr: string): string {
  const [year, month, day] = dateStr.split('-');
  return `${year}-${month}-${day}`;
}

private isSelected(day: number): boolean {
  const dateStr = `${this.currYear}-${String(this.currMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
  return dateStr === this.userSelectedDate;
}

private isDateAvailable(day: number): boolean {
  const dateStr = `${this.currYear}-${String(this.currMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
  return this.fechasDisponibles.some(fecha => fecha.value === dateStr);
}

private changeMonth(increment: boolean): void {
  this.currMonth = increment
    ? (this.currMonth + 1) % 12
    : (this.currMonth + 11) % 12;
  if (increment && this.currMonth === 0) this.currYear++;
  if (!increment && this.currMonth === 11) this.currYear--;
  this.renderCalendar();
}

private renderCalendar(): void {
  let firstDayofMonth = new Date(this.currYear, this.currMonth, 1).getDay();
  let lastDateofMonth = new Date(
    this.currYear,
    this.currMonth + 1,
    0
  ).getDate();

  // Ajusta el índice de inicio si la semana comienza en Domingo (0) para que sea Lunes (1)
  let startDayIndex = firstDayofMonth === 0 ? 6 : firstDayofMonth - 1;

  this.days = [];
  this.currentDate = `${this.months[this.currMonth]} ${this.currYear}`;

  // Añadir los últimos días del mes anterior si el mes no comienza en Lunes
  for (let i = 0; i < startDayIndex; i++) {
    this.days.push(null);
  }

  // Rellenar el array de días para el mes actual
  for (let day = 1; day <= lastDateofMonth; day++) {
    this.days.push(day);
  }

  // Añadir más días del siguiente mes si el mes no termina en Domingo
  let endDayIndex = 7 - (this.days.length % 7);
  if (endDayIndex < 7) {
    for (let i = 0; i < endDayIndex; i++) {
      this.days.push(null);
    }
  }

  this.currentDate = `${this.months[this.currMonth]} ${this.currYear}`;
}

private isToday(day: number): boolean {
  const today = new Date();
  return (
    day === today.getDate() &&
    this.currYear === today.getFullYear() &&
    this.currMonth === today.getMonth()
  );
}

private isBeforeToday(day: number): boolean {
  const dateToCheck = new Date(this.currYear, this.currMonth, day);
  const currentDate = new Date();
  currentDate.setHours(0, 0, 0, 0); // Remover la hora actual para comparar solo la fecha
  return dateToCheck < currentDate;
}

private resetSelectedDate() {
  this.userSelectedDate = null;
}

}
</script>
