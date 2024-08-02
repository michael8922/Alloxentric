<template>

    <!-- Begin Page Content -->
    <div class="container-fluid cont-all bg-all">

    <!-- Page Heading -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">Lista de espera</h1>
    </div>

    <!-- Content Row -->
    <div class="row">

        <div class="col-lg-12 mb-4">

            <!-- Illustrations -->
            <div class="card shadow mb-4">
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                            <thead>
                                <tr>
                                    <th>Nombres</th>
                                    <th>Fecha de registro</th>
                                    <th>Teléfono</th>
                                    <th>Correo</th>
                                </tr>
                            </thead>
                            <tfoot>
                                <tr>
                                    <th>Nombres</th>
                                    <th>Fecha de registro</th>
                                    <th>Teléfono</th>
                                    <th>Correo</th>
                                </tr>
                            </tfoot>
                            <tbody>
                                <tr class="table-link">
                                    <td>Saul Suazo</td>
                                    <td>09/10/2023</td>
                                    <td>+56 9 80631458</td>
                                    <td>S.suazo@gmail.com</td>
                                </tr>
                                <tr class="table-link">
                                    <td>Saul Suazo</td>
                                    <td>09/10/2023</td>
                                    <td>+56 9 80631458</td>
                                    <td>S.suazo@gmail.com</td>
                                </tr>
                                <tr class="table-link">
                                    <td>Saul Suazo</td>
                                    <td>09/10/2023</td>
                                    <td>+56 9 80631458</td>
                                    <td>S.suazo@gmail.com</td>
                                </tr>
                                <tr class="table-link">
                                    <td>Saul Suazo</td>
                                    <td>09/10/2023</td>
                                    <td>+56 9 80631458</td>
                                    <td>S.suazo@gmail.com</td>
                                </tr>
                                <tr class="table-link">
                                    <td>Saul Suazo</td>
                                    <td>09/10/2023</td>
                                    <td>+56 9 80631458</td>
                                    <td>S.suazo@gmail.com</td>
                                </tr>
                                <tr class="table-link">
                                    <td>Saul Suazo</td>
                                    <td>09/10/2023</td>
                                    <td>+56 9 80631458</td>
                                    <td>S.suazo@gmail.com</td>
                                </tr>
                                <tr class="table-link">
                                    <td>Saul Suazo</td>
                                    <td>09/10/2023</td>
                                    <td>+56 9 80631458</td>
                                    <td>S.suazo@gmail.com</td>
                                </tr>
                                <tr class="table-link">
                                    <td>Saul Suazo</td>
                                    <td>09/10/2023</td>
                                    <td>+56 9 80631458</td>
                                    <td>S.suazo@gmail.com</td>
                                </tr>
                                <tr class="table-link">
                                    <td>Saul Suazo</td>
                                    <td>09/10/2023</td>
                                    <td>+56 9 80631458</td>
                                    <td>S.suazo@gmail.com</td>
                                </tr>
                            </tbody>
                        </table>
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
	@Component({
		name: 'MainInicio',
	})
	export default class MainInicio extends Vue {
		public message = this.$t("Main.message");
	}
</script>