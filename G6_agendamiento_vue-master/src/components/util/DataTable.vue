<template>
    <div>
        <!--Titulo de la vista-->
        <v-card-title primary-title>
            {{ title }}
        </v-card-title>
        <!-- btn para poder agregar un nuevo registro -->
        <v-row justify="center">
            <!-- al apretar el btn "agregar" se abre un dialog donde podremos agregar los datos--->
            <v-dialog v-model="dialog" persistent max-width="600px">
                <template v-slot:activator="{ on, attrs }">
                <v-btn
                color="lime"
                dark
                v-bind="attrs"
                v-on="on">
                {{ btnAdd }}
                </v-btn>
            </template>
            <!-- este componente "v-card" es el que abre el dialog para poder agregar los nuevos registros -->
            <v-card>
                <v-card-title>
                    <span class="text-h5"> {{ datos }} </span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <!-- aqui se agrega el nombre -->
                            <v-col cols="12">
                                <v-text-field
                                :label="name"
                                required
                                v-model="nameElement">
                                <v-textarea>
                                </v-textarea>
                                </v-text-field>
                            </v-col>
                            <!-- aqui se agrega el número -->
                            <v-col cols="12">
                                <v-text-field
                                :label="number"
                                required
                                v-model="descriptionElement">
                                <v-textarea></v-textarea>
                                </v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <!-- aqui se encuentran los btn para guardar o cancelar el dialog para agregar datos -->
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                    color="#26c6da"
                    text
                    @click="dialog = false">
                    {{ btnClose }}
                    </v-btn>
                    <v-btn
                    color="#26c6da"
                    text
                    :disabled= "isLoading"
                    @click="aggregateItem()">
                    {{ btnSave }}
                    </v-btn>
                </v-card-actions>
            </v-card>
            </v-dialog>
        </v-row>
        <v-spacer></v-spacer>
        <!-- aqui comienza la tabla para ver los datos que hemos agregado, ademas se mostraran los btn para editar o eliminar los registros -->
        <v-col>
            <v-data-table
            :headers="header"
            :items="rows"
            class="elevation-1">
            <template v-slot:item="row">
                <tr>
                    <td>{{row.item.Nombre}}</td>
                    <td>{{row.item.Número}}</td>
                    <td>
                    <!-- aqui se editan los registros -->
                    <v-icon
                    small
                    class="mr-2"
                    @click="editItem(row.item)">
                    mdi-pencil
                    </v-icon>
                    </td>
                    <td>
                    <!-- aqui se eliminan los registros -->
                    <v-icon
                    small
                    @click="deleteItem(row.item)">
                    mdi-delete
                    </v-icon>
                    </td>
                </tr>
            </template>
            </v-data-table>
        </v-col>
        <!-- este dialog se abre para poder editar los datos ya guardados -->
        <v-dialog
        v-model="dialogUpdate"
        max-width="900px"
        persistent>
        <v-card>
            <v-card-title primary-title>
            {{ btnEdit}}
            </v-card-title>
            <v-col cols="12">
                <v-textarea
                v-model="edit_number">
                </v-textarea>   
            </v-col>
            <v-card-actions>
                <!-- btn para cerrar el dialog para editar -->
                <v-btn
                color="#26c6da"
                text
                @click="dialogUpdate = false">
                {{ btnClose }}
                </v-btn>
                <!-- btn para guardar el dialog para editar -->
                <v-btn
                color="#26c6da"
                text
                :disabled= "isLoading"
                @click="sendEdit()">
                {{ btnSave }}
                </v-btn>
            </v-card-actions>
        </v-card>
        </v-dialog>
        <!-- este dialog es para confirmar si se quiere eliminar el registro -->
        <v-dialog
        v-model="dialogDelete"
        max-width="900px"
        persistent>
        <v-card>
        <v-card-title primary-title>
        {{ textDelete }}
        </v-card-title>
        <v-card-actions class="justify-end">
            <!-- btn para confirmar eliminar el registro -->
            <v-btn color="#06B7B2" dark @click="sendDelete()">
            {{ btnDelete }}
            </v-btn>
            <!-- btn para cerrar el dialog para eliminar -->
            <v-btn color="pink" dark @click="dialogDelete = false">
            {{ btnCancel }}
            </v-btn>
        </v-card-actions>
       </v-card>
    </v-dialog>
</div>
</template>
<script lang="ts">
     import {Vue, Component} from 'vue-property-decorator';
     import { IDataTable } from '@/model/main/IDataTable';
     import { IHeaderTable } from '@/model/main/IHeaderTable';
     import { internet } from '@/utils/Internet';
     import Util from '@/utils/Util';
     import { ILabels } from '@/model/labels/ILabels';
     import axios from "axios";


@Component({
    name: 'DataTable'
    })
    export default class DataTable extends Vue{
        //frases i18n
        public title = this.$t("dataTable.title");
        public btnAdd = this.$t("dataTable.btnAdd");
        public datos = this.$t("dataTable.datos");
        public name = this.$t("dataTable.name");
        public number = this.$t("dataTable.number");
        public btnClose = this.$t("dataTable.btnClose");
        public btnSave = this.$t("dataTable.btnSave");
        public btnEdit = this.$t("dataTable.btnEdit");
        public textDelete = this.$t("dataTable.textDelete");
        public btnDelete = this.$t("dataTable.btnDelete");
        public btnCancel = this.$t("dataTable.btnCancel");
        // dataTable
        public rows: Array<IDataTable> = [];
        public header: Array<IHeaderTable<IDataTable>> = [];
        public data: Array<ILabels> = [];
        //dialog
        public dialog = false;
        public isLoading = false;
        public dialogUpdate = false;
        public dialogDelete = false;
        //v-card
        public nameElement = "";
        public descriptionElement = "";
        public edit_number = "";
        public current_item = {'Nombre': '', 'Número': ''}; 
    mounted(): void {
        this.getData();
    }

    private getData() {
        this.isLoading = true;
        //aqui llamamos al endpoint desde el back que necesitamos utilizar
        let config = {
				method: 'get',
				url: process.env.VUE_APP_API + "/example/example2",
                headers: { Authorization: `Bearer ${this.$store.state.token}`}
			};
            axios(config)
            .then((response) => {
                this.data = response.data as Array<ILabels>;
                const dataTable: Array<IDataTable> = [];
                for (let item of this.data) {
                   // console.log(item);
                    const row: IDataTable = {};
                    row['Nombre'] = item.name;
                    row['Número'] = item.number;
                    row['Editar'] = "";
                    row['Eliminar'] = "";
                    //console.log(JSON.stringify(item.tunning))
                    dataTable.push(row);
                }
                const header: Array<IHeaderTable<
                    IDataTable
                >> = Object.keys(dataTable[0]).map(
                    (
                        key: string
                    ): IHeaderTable<IDataTable> => {
                        let text = key;
                        switch (key) {
                            case 'name':
                                text = "Nombre";
                                break;
                            case 'number':
                                text = "Número";
                                break;
                                }
                            return {
                                text,
                                value: key,
							};
                        }
                    ) as Array<IHeaderTable<IDataTable>>;
                    this.rows = dataTable;
                    this.header = header;
                    })
                .catch(console.log)
                .finally(() => {
                this.isLoading = false;
            });
        }

    public editItem(item:ILabels){
        let number = item.Número; 
        this.edit_number = number;
        this.dialogUpdate = true;
        this.current_item = item;
    }
    public sendEdit() {
        let nombre = this.current_item.Nombre;
        let dt = JSON.stringify({
            'name': nombre, 
            'number': this.edit_number
        })
        let config = {
            //aqui llamamos al endpoint desde el back que necesitamos utilizar
				method: 'put',
				url: process.env.VUE_APP_API + "/example/example2",
                data: dt,
				headers: { 
                    Authorization: `Bearer ${this.$store.state.token}`,
                    'Content-Type': 'application/json'
                }
			};
            axios(config)
			.then(response => {
				this.getData();
                this.dialogUpdate = false;
			})	
    }

    public deleteItem(item:ILabels){
        this.current_item = item;
        this.dialogDelete = true;
    }

    public sendDelete(){
        let nombre = this.current_item.Nombre;
        console.log("delete");
        let config = {
            //aqui llamamos al endpoint desde el back que necesitamos utilizar para eliminar
            method: 'delete',
            url: process.env.VUE_APP_API + "/example/example2",
            params: {'name': nombre},
            headers: { Authorization: `Bearer ${this.$store.state.token}`}
        };
        axios(config)
        .then(response => {
            // sacar el item del front
            this.dialogDelete = false;
            this.getData();
        })
    }

    public aggregateItem(){
        let name = this.nameElement;
        let number = this.descriptionElement;
        let dt = JSON.stringify({
            'name': name, 
            'number': number
        })
        let config = {
            //aqui llamamos al endpoint desde el back que necesitamos utilizar para agregar registros
            method: 'post',
            url: process.env.VUE_APP_API + "/example/example2",
            data: dt,
            headers: { 
                Authorization: `Bearer ${this.$store.state.token}`,
                'Content-Type': 'application/json'
            }
        };
        axios(config)
			.then(response => {
                this.dialog = false;
                this.nameElement = "";
                this.descriptionElement = "";
                this.getData();
			})
    }


    }  
</script>