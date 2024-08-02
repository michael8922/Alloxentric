<template>
  <div class="container-fluid cont-all full-height bg-all">
    <!-- HEADER -->
    <header class="header">
      <h1 class="header__title">
        <strong style="color: #01a79d">Agendamiento</strong> Medico
      </h1>
      <p>
        ¡Prioriza tu salud! Sigue estos simples pasos y agenda tu cita médica
        hoy<br />
        para cuidar de ti con bienestar y tranquilidad.
      </p>
    </header>
    <!-- END HEADER -->

    <!-- CONTENIDO -->
    <div class="content">
      <div class="content__inner">
        <div class="container overflow-hidden">
          <div class="multisteps-form">
            <div class="row">
              <div class="col-12 col-lg-8 ml-auto mr-auto mb-4">
                <div class="multisteps-form__progress">
                  <button
                    class="multisteps-form__progress-btn js-active"
                    type="button"
                    title="User Info"
                  >
                    Paso 1
                  </button>
                  <button
                    class="multisteps-form__progress-btn"
                    type="button"
                    title="Address"
                  >
                    Paso 2
                  </button>
                  <button
                    class="multisteps-form__progress-btn"
                    type="button"
                    title="Order Info"
                  >
                    Paso 3
                  </button>
                  <button
                    class="multisteps-form__progress-btn"
                    type="button"
                    title="Message"
                  >
                    Paso 4
                  </button>
                  <button
                    class="multisteps-form__progress-btn"
                    type="button"
                    title="Prueba"
                  >
                    Paso 5
                  </button>
                  <button
                    class="multisteps-form__progress-btn"
                    type="button"
                    title="Prueba"
                  >
                    Paso 6
                  </button>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-12 col-lg-8 m-auto">
                <form class="multisteps-form__form user">
                  <div
                    class="multisteps-form__panel shadow p-4 rounded bg-white js-active"
                    data-animation="scaleIn"
                  >
                    <h3 class="multisteps-form__title">
                      Ingrese su RUT y el tipo de prestación*
                    </h3>
                    <div class="multisteps-form__content">
                      <div class="form-row mt-4">
                        <!-- Input Rut -->
                        <div class="col-12 col-sm-6">
                          <input
                            type="text"
                            class="form-control form-control-user"
                            id="rut"
                            placeholder="Ingrese su rut"
                            v-model="selectRut"
                            required
                          />
                        </div>

                        <div class="col-12 col-sm-6">
                          <!-- Select Prestación -->
                          <select
                            class="custom-select form-control form-control-user"
                            id="ElementArrayPrevision"
                            v-model="selectPrevision"
                            @change="SelectedPrevisionChange"
                            required
                          >
                            <option
                              class="alert-success font-weight-bold"
                              value=""
                              disabled
                              selected
                            >
                              Seleccione una Previsión
                            </option>
                            <option
                              v-for="option in ElementArrayPrevision"
                              :value="option.value"
                              :key="option.value"
                            >
                              {{ option.text }}
                            </option>
                            <!-- Agrega opciones de comuna aquí -->
                          </select>
                          <!-- End Select Especialidad -->
                        </div>
                      </div>

                      <div class="button-row d-flex mt-4">
                        <button
                          @click="handleFormButtonClick"
                          class="btn btn-primary ml-auto js-btn-next"
                          type="button"
                          title="Next"
                        >
                          Continuar
                        </button>
                      </div>
                    </div>
                  </div>

                  <div
                    class="multisteps-form__panel shadow p-4 rounded bg-white"
                    data-animation="scaleIn"
                  >
                    <h3 class="multisteps-form__title">
                      Seleccione especialidad y centro médico para su atención*
                    </h3>
                    <div class="multisteps-form__content">
                      <div class="form-row mt-4">
                        <!-- Select Especialidad -->
                        <div class="col-12 col-sm-6">
                          <select
                            class="custom-select form-control form-control-user"
                            id="ElementArrayCentroMedico"
                            v-model="selectEspecialidad"
                            @change="saveSelectedValueEspecialidad"
                            required
                          >
                            <option
                              class="alert-success font-weight-bold p-1"
                              value=""
                              disabled
                              selected
                            >
                              Seleccione una especialidad
                            </option>
                            <option
                              v-for="option in ElementArrayEspecialidad"
                              :value="option.value"
                              :key="option.value"
                            >
                              {{ option.text }}
                            </option>
                          </select>
                          <!-- End Select Especialidad -->
                        </div>

                        <!-- Select CMedico -->
                        <div class="col-6 col-sm-6">
                          <select
                            class="custom-select form-control form-control-user"
                            id="ElementArrayCentroMedico"
                            v-model="selectCentroMedico"
                            @change="saveSelectedValueCentroMedico"
                            required
                          >
                            <option
                              class="alert-success font-weight-bold p-1"
                              value=""
                              disabled
                              selected
                            >
                              Seleccione un Centro Medico
                            </option>
                            <option
                              v-for="option in ElementArrayCentroMedico"
                              :value="option.value"
                              :key="option.value"
                            >
                              {{ option.text }}
                            </option>
                          </select>
                          <!-- End Select CMedico -->
                        </div>
                      </div>

                      <div class="button-row d-flex mt-4">
                        <button
                          @click="handleFormButtonClick"
                          class="btn btn-primary js-btn-prev"
                          type="button"
                          title="Prev"
                        >
                          volver
                        </button>
                        <button
                          @click="handleFormButtonClick"
                          class="btn btn-primary ml-auto js-btn-next"
                          type="button"
                          title="Next"
                        >
                          Continuar
                        </button>
                      </div>
                    </div>
                  </div>

                  <div
                    class="multisteps-form__panel shadow p-4 rounded bg-white"
                    data-animation="scaleIn"
                  >
                    <h3 class="multisteps-form__title">
                      Selecciona la fecha de su cita*
                    </h3>
                    <div class="multisteps-form__content">
                      <div class="row">
                        <div class="col-12 col-md-12">
                          <!-- Calendario -->
                          <App-Calendario
                            ref="appCalendario"
                            :fechas-disponibles="fechasDisponibles"
                            @date-selected="handleDateSelected"
                          />
                        </div>
                      </div>
                      <div class="row">
                        <div class="button-row d-flex mt-4 col-12">
                          <button
                            @click="handleFormButtonClick"
                            class="btn btn-primary js-btn-prev"
                            type="button"
                            title="Prev"
                          >
                            Volver
                          </button>
                          <button
                            @click="handleFormButtonClick"
                            class="btn btn-primary ml-auto js-btn-next"
                            type="button"
                            title="Next"
                          >
                            Continuar
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div
                    class="multisteps-form__panel shadow p-4 rounded bg-white"
                    data-animation="scaleIn"
                  >
                    <h3 class="multisteps-form__title">
                      Su fecha de atención es
                      <strong>{{ selectedDate }}</strong> <br />A continuación
                      selecciona el doctor de su consulta*
                    </h3>

                    <div class="multisteps-form__content">
                      <div class="form-row mt-4">
                        <div class="col-md-12 scroll-card">
                          <div
                            v-for="(carta, index) in cartas"
                            :key="index"
                            class="card mb-3"
                          >
                            <div class="card-body">
                              <div
                                class="header-card d-flex align-items-center"
                              >
                                <img
                                  :src="require('@/assets/img/img_prueba.png')"
                                  alt="Dr. Nombre"
                                  class="imagen-circular"
                                />
                                <div>
                                  <h5 class="card-title">
                                    {{ carta.nombre_medico }}
                                  </h5>
                                  <h6 class="card-subtitle mb-2">
                                    Especialidad:
                                    <strong>{{ carta.especialidad }}</strong>
                                  </h6>
                                </div>
                              </div>
                              <div class="content-card">
                                <p class="card-text">
                                  <i
                                    class="fa-solid fa-hospital"
                                    style="color: #01a79d"
                                  ></i>
                                  Centro Médico
                                  <strong>{{ carta.centro_medico }}</strong>
                                </p>
                                <!-- Horarios disponibles -->
                                <div class="d-flex flex-wrap">
                                  <button
                                    v-for="cita in carta.citas"
                                    :key="cita.hora"
                                    @click.prevent="
                                      selectHour(carta, cita.hora)
                                    "
                                    type="button"
                                    :class="[
                                      'btn',
                                      'btn-sm',
                                      'm-1',
                                      {
                                        'btn-primary':
                                          selectedHour === cita.hora,
                                        'btn-outline-primary':
                                          selectedHour !== cita.hora,
                                      },
                                    ]"
                                  >
                                    {{ cita.hora }}
                                  </button>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="button-row d-flex mt-4">
                        <button
                          @click="handleFormButtonClick"
                          class="btn btn-primary js-btn-prev"
                          type="button"
                          title="Prev"
                        >
                          Volver
                        </button>
                        <button
                          @click="handleFormButtonClick"
                          class="btn btn-primary ml-auto js-btn-next"
                          type="button"
                          title="Next"
                        >
                          Continuar
                        </button>
                      </div>
                    </div>
                  </div>

                  <div
                    class="multisteps-form__panel shadow p-4 rounded bg-white"
                    data-animation="scaleIn"
                  >
                    <h3 class="multisteps-form__title">
                      Ingresa tu nombre, telefono y correo electronico*
                    </h3>

                    <div class="multisteps-form__content user">
                      <div class="form-row mt-4">
                        <div class="col-12 col-sm-6">
                          <input
                            type="text"
                            class="form-control form-control-user"
                            id="nombre"
                            placeholder="Ingrese nombre y apellido"
                            v-model="selectNombre"
                            required
                          />
                        </div>
                        <div class="col-12 col-sm-6">
                          <input
                            type="number"
                            class="form-control form-control-user"
                            id="telefono"
                            placeholder="Ingrese telefono"
                            v-model="selectTelefono"
                            required
                          />
                        </div>
                        <div class="col-12 col-sm-12">
                          <input
                            type="email"
                            class="form-control form-control-user"
                            id="correo"
                            placeholder="Ingrese correo electronico"
                            v-model="selectCorreo"
                            required
                          />
                        </div>
                      </div>
                      <div class="button-row d-flex mt-4">
                        <button
                          @click="handleFormButtonClick"
                          class="btn btn-primary js-btn-prev"
                          type="button"
                          title="Prev"
                        >
                          Volver
                        </button>
                        <button
                          @click="handleFormButtonClick"
                          class="btn btn-primary ml-auto js-btn-next"
                          type="button"
                          title="Send"
                        >
                          Continuar
                        </button>
                      </div>
                    </div>
                  </div>

                  <div
                    class="multisteps-form__panel shadow p-4 rounded bg-white"
                    data-animation="scaleIn"
                  >
                    <h3 class="multisteps-form__title">
                      <strong
                        >¡Estás a un clic de concretar tu agendamiento
                        &#128512;!</strong
                      ><br />Verifica la información para finalizar el proceso*
                    </h3>

                    <div class="multisteps-form__content user">
                      <div class="form-row mt-4">
                        <div class="col-12 col-sm-12">
                          <h4>
                            <strong style="color: #01a79d; font-weight: 800"
                              >Detalle</strong
                            >
                          </h4>
                          <table class="table table-bordered mt-3">
                            <tbody>
                              <tr>
                                <th scope="row">N° de Orden</th>
                                <td>{{ selectedOrderNumber || "-" }}</td>
                              </tr>
                              <tr>
                                <th scope="row">Rut</th>
                                <td>{{ selectRut || "-" }}</td>
                              </tr>
                              <tr>
                                <th scope="row">Nombre Paciente</th>
                                <td>{{ selectNombre || "-" }}</td>
                              </tr>
                              <tr>
                                <th scope="row">Teléfono</th>
                                <td>{{ selectTelefono || "-" }}</td>
                              </tr>
                              <tr>
                                <th scope="row">Correo</th>
                                <td>{{ selectCorreo || "-" }}</td>
                              </tr>
                              <tr>
                                <th scope="row">Previsión</th>
                                <td>{{ selectPrevision || "-" }}</td>
                              </tr>
                              <tr>
                                <th scope="row">Centro Medico</th>
                                <td>
                                  {{ selectedCarta?.centro_medico || "-" }}
                                </td>
                              </tr>
                              <tr>
                                <th scope="row">Especialidad</th>
                                <td>
                                  {{ selectedCarta?.especialidad || "-" }}
                                </td>
                              </tr>
                              <tr>
                                <th scope="row">Nombre Medico</th>
                                <td>
                                  {{ selectedCarta?.nombre_medico || "-" }}
                                </td>
                              </tr>
                              <tr>
                                <th scope="row">Fecha de atención</th>
                                <td>{{ selectedDate || "-" }}</td>
                              </tr>
                              <tr>
                                <th scope="row">Hora de atención</th>
                                <td>{{ selectedHour || "-" }}</td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                      <div class="button-row d-flex mt-4">
                        <button
                          @click="handleFormButtonClick"
                          class="btn btn-primary js-btn-prev"
                          type="button"
                          title="Prev"
                        >
                          Volver
                        </button>
                        <button
                          @click="sendEdit()"
                          class="btn btn-success ml-auto"
                          type="button"
                          title="Send"
                          data-toggle="modal"
                          data-target="#VerDatoModal"
                        >
                          Agendar
                        </button>
                      </div>
                    </div>
                  </div>
                </form>
                <a v-bind:href="'/MainLogin'" class="btn btn-primary ml-auto js-btn-next btn-block">Volver a la pantalla de selección</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- END CONTENIDO -->

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
              Gracias <strong>{{ selectNombre }}</strong>
            </h5>
          </div>
          <div class="modal-body">
            <div class="box-nro">
              Tu cita a sido agendata exitosamente, tu numero de atención es:
              <div class="nro_modal mt-3">
                <h4>{{ selectedOrderNumber }}</h4>
              </div>
            </div>
          </div>
          <div class="modal-footer d-flex justify-content-center">
            <a class="btn btn-primary" v-bind:href="'/MainUsuario'"
              >Volver a la pantalla de inicio</a
            >
          </div>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { ILabels } from "@/model/main/Ilabels";
import axios from "axios";
import AppCalendario from "@/components/util/AppCalendario.vue";
// Importar NodeListOf desde el archivo de definiciones de TypeScript dom
type NodeListOf<T extends Node> = NodeList<T>;

@Component({
  name: "MainUsuario",
  components: {
    AppCalendario,
  },
})
export default class MainUsuario extends Vue {
  //Rut
  public selectRut = "";

  //Prevision
  public selectPrevision = "";
  public ElementArrayPrevision = [];

  //Especialidad
  public selectEspecialidad = "";
  public ElementArrayEspecialidad = [];

  //Centro Medico
  public selectCentroMedico = "";
  public ElementArrayCentroMedico = [];

  //Fechas
  public fechasDisponibles = [];
  public selectedDate = "";
  public selectCarta = null;

  //Cartas
  public cartas = [];
  public selectedHour: string | null = null;
  public selectedOrderNumber: string | null = null;

  //DatosPaciente
  public selectNombre = "";
  public selectTelefono = "";
  public selectCorreo = "";

  //Modal
  public isModalVisible = false;

  private stepsBtnClass = "multisteps-form__progress-btn";
  private stepsBtns: NodeListOf<Element> | null = null;
  private stepsBar: Element | null = null;
  private stepsForm: Element | null = null;
  private stepsFormTextareas: NodeListOf<Element> | null = null;
  private stepFormPanelClass = "multisteps-form__panel";
  private stepFormPanels: NodeListOf<Element> | null = null;
  private stepPrevBtnClass = "js-btn-prev";
  private stepNextBtnClass = "js-btn-next";

  mounted(): void {
    this.getDataPrevision();
    this.getDataEspecialidad();
    this.getDataCentroMedico();
    this.getDataFechasDisponibles();
    this.handleDateSelected();

    // Esperamos a que el DOM esté completamente cargado
    this.$nextTick(() => {
      this.stepsBtns = document.querySelectorAll(`.${this.stepsBtnClass}`);
      this.stepsBar = document.querySelector(".multisteps-form__progress");
      this.stepsForm = document.querySelector(".multisteps-form__form");
      this.stepsFormTextareas = document.querySelectorAll(
        ".multisteps-form__textarea"
      );
      this.stepFormPanels = document.querySelectorAll(
        ".multisteps-form__panel"
      );

      const defaultAnimationType = "slideHorz";
      this.setAnimationType(defaultAnimationType);

      const animationSelect: any = document.querySelector(
        ".pick-animation__select"
      );
      animationSelect.value = defaultAnimationType;

      animationSelect.addEventListener("change", () => {
        const newAnimationType = animationSelect.value;
        this.setAnimationType(newAnimationType);
      });
    });
  }

  @Watch("selectedDate")
  onSelectedDateChanged(value: string, oldValue: string) {
    // Verifica que la fecha sea válida y que las otras propiedades también estén establecidas
    if (value && this.selectEspecialidad && this.selectCentroMedico) {
      this.getDataDoctorConsulta();
    }
  }

  private setAnimationType(newType: string): void {
    if (this.stepFormPanels) {
      this.stepFormPanels.forEach((elem: Element) => {
        elem.dataset.animation = newType;
      });
    }
  }

  private removeClasses(elemSet: NodeListOf<Element>, className: string): void {
    elemSet.forEach((elem: Element) => {
      elem.classList.remove(className);
    });
  }

  private findParent(elem: Element, parentClass: string): Element {
    let currentNode: Element | null = elem;

    while (currentNode) {
      console.log("Checking node:", currentNode);

      if (
        currentNode.classList &&
        currentNode.classList.contains(parentClass)
      ) {
        console.log("Found parent with class:", parentClass);
        break;
      }

      currentNode = currentNode.parentNode as Element;
    }

    return currentNode || elem;
  }

  private getActiveStep(elem: Element): number {
    return Array.from(this.stepsBtns || []).indexOf(elem);
  }

  private setActiveStep(activeStepNum: number): void {
    if (this.stepsBtns) {
      this.removeClasses(this.stepsBtns, "js-active");

      this.stepsBtns.forEach((elem: Element, index: number) => {
        if (index <= activeStepNum) {
          elem.classList.add("js-active");
        }
      });
    }
  }

  private getActivePanel(): Element | undefined {
    let activePanel;

    if (this.stepFormPanels) {
      this.stepFormPanels.forEach((elem: Element) => {
        if (elem.classList.contains("js-active")) {
          activePanel = elem;
        }
      });
    }

    return activePanel;
  }

  private setActivePanel(activePanelNum: number): void {
    if (this.stepFormPanels) {
      this.removeClasses(this.stepFormPanels, "js-active");

      this.stepFormPanels.forEach((elem: Element, index: number) => {
        if (index === activePanelNum) {
          elem.classList.add("js-active");
          this.setFormHeight(elem);
        }
      });
    }
  }

  private formHeight(activePanel: Element): void {
    const activePanelHeight = (activePanel as HTMLElement).offsetHeight;

    if (this.stepsForm) {
      (this.stepsForm as HTMLElement).style.height = `${activePanelHeight}px`;
    }
  }

  private setFormHeight(): void {
    const activePanel = this.getActivePanel();

    if (activePanel) {
      this.formHeight(activePanel);
    }
  }

  private handleStepsButtonClick(e: Event): void {
    const eventTarget = e.target as Element;

    if (eventTarget.classList.contains(this.stepsBtnClass)) {
      const activeStep = this.getActiveStep(eventTarget);
      this.setActiveStep(activeStep);
      this.setActivePanel(activeStep);
    } else {
      this.handleFormButtonClick(eventTarget);
    }
  }

  private handleFormButtonClick(event: Event): void {
    const target = event.target as Element;
    const isPrevButton = target.classList.contains(this.stepPrevBtnClass);
    const activePanel = this.findParent(target, this.stepFormPanelClass);

    if (activePanel) {
      const activePanelNum = Array.from(this.stepFormPanels || []).indexOf(
        activePanel
      );
      const stepChange = isPrevButton ? -1 : 1;
      const nextPanelNum = activePanelNum + stepChange;

      if (
        nextPanelNum >= 0 &&
        nextPanelNum < (this.stepFormPanels || []).length
      ) {
        if (isPrevButton) {
          // Si se presiona el botón 'Volver', resetear los datos del paso actual antes de cambiar de panel
          this.resetFormData(activePanelNum);
        } else {
          // Si se presiona el botón 'Continuar', validar antes de cambiar al siguiente panel
          if (!this.validateForm(activePanelNum)) {
            console.log("Completa todos los campos antes de avanzar.");
            return;
          }
        }

        // Cambiar al panel anterior o siguiente
        this.setActiveStep(nextPanelNum);
        this.setActivePanel(nextPanelNum);
      }
    }
  }

  private resetFormData(panelNumber: number): void {
    switch (panelNumber) {
      case 1:
        // No hay nada que resetear en el primer panel
        break;
      case 2:
        // Resetear los datos del segundo panel
        this.selectEspecialidad = "";
        this.selectCentroMedico = "";
        break;
      case 3:
        // Resetear los datos del tercer panel
        this.selectedDate = "";
        this.selectedHour = null;
        this.cartas = [];
        this.$refs.appCalendario.resetSelectedDate();
        break;
      // Agregar más casos si hay más paneles con datos que resetear
    }
  }

  private windowResize(): void {
    window.addEventListener("resize", this.setFormHeight, false);
  }

  created(): void {
    if (this.stepsBtns) {
      this.stepsBtns.forEach((btn: Element) => {
        btn.addEventListener("click", this.handleStepsButtonClick);
      });
    }
    if (this.stepsForm) {
      this.stepsForm.addEventListener("click", this.handleStepsFormClick);
    }

    this.windowResize();
  }

  //GetData Prevision
  private getDataPrevision() {
    this.isLoading = true;
    let config = {
      method: "get",
      url: `${process.env.VUE_APP_API_3}/previsiones/prevision`,
      headers: { Authorization: `Bearer ${this.$store.state.token}` },
    };

    axios(config)
      .then((response) => {
        this.data = response.data as Array<ILabels>;
        if (!this.selectPrevision) {
          this.selectPrevision = this.data[0].prevision; // o cualquier lógica que elijas para mantener el valor seleccionado
        }
        this.ElementArrayPrevision = [];
        this.data.forEach((item) => {
          // Modificar para incluir el campo value con el _id
          this.ElementArrayPrevision.push({
            text: item.prevision,
            value: item.prevision,
          });
          this.selectPrevision = "";
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
  public SelectedPrevisionChange(event) {
    this.selectedValue = this.selectPrevision; // Asignar el valor de selectRegion a selectedValue
    console.log(this.selectPrevision); // Verificar el valor de selectRegion
  }

  //GetData Especialidad
  private getDataEspecialidad() {
    this.isLoading = true;
    let config = {
      method: "get",
      url: `${process.env.VUE_APP_API_3}/especialidades/especialidad`,
      headers: { Authorization: `Bearer ${this.$store.state.token}` },
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
          this.ElementArrayEspecialidad.push({
            text: item.especialidad,
            value: item.especialidad,
          });
          this.selectEspecialidad = "";
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
    this.selectEspecialidad = event.target.value;
    console.log("Especialidad seleccionada: ", this.selectEspecialidad);
    // Ahora que tienes la especialidad, puedes buscar los centros médicos
    this.getDataCentroMedico();
  }

  // GetData Centro Medico
  private getDataCentroMedico() {
    this.isLoading = true;
    let config = {
      method: "get",
      url: `${process.env.VUE_APP_API_4}/conf_medicos/calendario/${this.selectEspecialidad}`,
      headers: { Authorization: `Bearer ${this.$store.state.token}` },
    };

    axios(config)
      .then((response) => {
        this.data = response.data as Array<ILabels>;
        if (this.data.length > 0 && this.data[0].centro_medico) {
          this.selectCentroMedico = this.data[0].centro_medico;
        }
        // Limpiar el array antes de agregar nuevas fechas
        this.ElementArrayCentroMedico = [];

        // Crear un conjunto para almacenar centros médicos únicos
        const centrosMedicosUnicos = new Set();

        this.data.forEach((item) => {
          // Verificar si el documento tiene la propiedad centro_medico antes de agregarla al conjunto
          if (item.centro_medico) {
            centrosMedicosUnicos.add(item.centro_medico);
          }
        });

        // Convertir el conjunto en un array y crear las opciones del select
        Array.from(centrosMedicosUnicos).forEach((centroMedico) => {
          this.ElementArrayCentroMedico.push({
            text: centroMedico,
            value: centroMedico,
          });
          this.selectCentroMedico = "";
        });
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        this.isLoading = false;
      });
  }

  private getDataFechasDisponibles() {
    this.isLoading = true;
    let config = {
      method: "get",
      url: `${process.env.VUE_APP_API_4}/conf_medicos/calendario/${this.selectEspecialidad}/${this.selectCentroMedico}`,
      headers: { Authorization: `Bearer ${this.$store.state.token}` },
    };

    axios(config)
      .then((response) => {
        if (response.data.length > 0 && response.data[0].fecha) {
          // Limpiar fechasObtenidas antes de asignar nuevos valores
          this.fechasObtenidas = [];

          response.data.forEach((item) => {
            // Verificar si el objeto tiene la propiedad 'fecha' antes de agregarla
            if (item.fecha) {
              this.fechasObtenidas.push({
                text: item.fecha,
                value: item.fecha,
              });
            }
          });

          // Limpiar fechasDisponibles antes de asignar nuevos valores
          this.fechasDisponibles = this.fechasObtenidas.map((item) => ({
            text: item.text,
            value: item.value,
          }));

          // Agregar un console.log para verificar el contenido de fechasDisponibles
          //console.log("Fechas Disponibles después del mapeo: ", this.fechasDisponibles);
          // Emitir un evento con las fechas disponibles
          this.$emit("fechas-disponibles", this.fechasDisponibles);
        } else {
          console.error(
            "El array 'data' está vacío o no contiene la propiedad 'fecha'."
          );
        }
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        this.isLoading = false;
      });
  }

  // En el método saveSelectedValueCentroMedico
  public saveSelectedValueCentroMedico(event) {
    this.selectCentroMedico = event.target.value;
    console.log("Centro médico seleccionado: ", this.selectCentroMedico);
    // Ahora que tienes el centro médico, puedes buscar las fechas disponibles
    this.getDataFechasDisponibles();
  }

  // Cuando seleccionas la fecha
  private handleDateSelected(date) {
    console.log("Fecha seleccionada recibida en el componente padre: ", date);
    this.selectedDate = date;
    console.log("this.selectedDate después de asignación:", this.selectedDate);
    if (this.selectedDate) {
      // Si la fecha es válida, procede con la obtención de datos
      this.getDataDoctorConsulta();
    } else {
      console.error("Fecha seleccionada es undefined");
    }
  }

  // Método para seleccionar una hora
  selectHour(carta, hora) {
    // Actualizar la hora seleccionada
    if (this.selectedHour === hora) {
      this.selectedHour = null;
      this.selectedOrderNumber = null; // Resetear el número de orden seleccionado
    } else {
      this.selectedHour = hora;
      const citaSeleccionada = carta.citas.find(c => c.hora === hora);
      if (citaSeleccionada) {
        this.selectedOrderNumber = citaSeleccionada.nro_orden; // Guarda el número de orden
        console.log("Número de orden actualizado a:", this.selectedOrderNumber);
      }
    }
    this.selectedCarta = carta;
  }

  private getDataDoctorConsulta() {
    console.log("getDataDoctorConsulta se está ejecutando");
    if (
      this.selectEspecialidad &&
      this.selectCentroMedico &&
      this.selectedDate
    ) {
      this.isLoading = true;
      let url = `${
        process.env.VUE_APP_API_4
      }/conf_medicos/calendario/${encodeURIComponent(
        this.selectEspecialidad
      )}/${encodeURIComponent(this.selectCentroMedico)}/${encodeURIComponent(
        this.selectedDate
      )}`;
      console.log("URL de la solicitud DataDoctor:", url);

      axios
        .get(url, {
          headers: { Authorization: `Bearer ${this.$store.state.token}` },
        })
        .then((response) => {
          if (response.data && response.data.length > 0) {
            const grouped = response.data.reduce((acc, item) => {
              // La clave sigue siendo una combinación de médico, especialidad y centro médico
              const key = `${item.nombre_medico}-${item.especialidad}-${item.centro_medico}`;
              if (!acc[key]) {
                acc[key] = {
                  centro_medico: item.centro_medico,
                  nombre_medico: item.nombre_medico,
                  especialidad: item.especialidad,
                  citas: [{ hora: item.hora, nro_orden: item.nro_orden }], // Inicia un arreglo de objetos cita
                };
              } else {
                // Agrega al arreglo existente un nuevo objeto cita
                acc[key].citas.push({ hora: item.hora, nro_orden: item.nro_orden });
              }
              return acc;
            }, {});

            // Ordenar las citas por hora dentro de cada agrupación
            for (let key in grouped) {
              grouped[key].citas.sort((a, b) => a.hora.localeCompare(b.hora));
            }

            this.cartas = Object.values(grouped);
          } else {
            console.error("El array 'data' está vacío.");
          }
        })
        .catch((error) => {
          console.error("Error en la solicitud de la API:", error);
        })
        .finally(() => {
          this.isLoading = false;
        });
    } else {
      console.error(
        "getDataDoctorConsulta llamado sin las variables necesarias establecidas"
      );
    }
  }

  public sendEdit() {
    let dt = JSON.stringify({
        'correo': this.selectCorreo,
        'telefono': this.selectNombre,
        'rut': this.selectRut,
        'prevision': this.selectPrevision,
        'nombre_paciente': this.selectNombre,
    })
    console.log("N° de orden: ", this.selectedOrderNumber)
    let config = {
        //aqui llamamos al endpoint desde el back que necesitamos utilizar
    method: 'put',
    url: `${process.env.VUE_APP_API_4}/conf_medicos/update_appointment/${this.selectedOrderNumber}`,
            data: dt,
    headers: {
                Authorization: `Bearer ${this.$store.state.token}`,
                'Content-Type': 'application/json'
            }
  };
        axios(config)
  .then(response => {
    //this.getData();
    this.dialogUpdate = false;
  })
}

  // Método para validar el formulario actual
  private validateForm(activePanelNum: number): boolean {
    // Agrega lógica de validación según el formulario actual (usando activePanelNum)
    switch (activePanelNum) {
      case 0:
        // Validación para el primer formulario
        return this.selectRut && this.selectPrevision;
      case 1:
        // Validación para el segundo formulario
        return this.selectEspecialidad && this.selectCentroMedico;
      case 2:
        // Validación para el tercer formulario
        return !!this.selectedDate;
      case 3:
        // Puedes agregar lógica específica para el tercer formulario aquí
        return this.selectedHour;
      // ... Puedes continuar agregando casos para otros formularios si es necesario
      case 4:
        // Puedes agregar lógica específica para el tercer formulario aquí
        return this.selectNombre && this.selectTelefono && this.selectCorreo;
    }
  }


}
</script>
