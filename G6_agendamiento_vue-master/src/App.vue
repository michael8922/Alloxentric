<template>

    <!-- Page Wrapper -->
    <div id="app">

        <div id="content-wrapper" class="d-flex flex-column">

            <div id="content">

                <router-view :keycloak="keycloak"></router-view>

            </div>

        </div>

    </div>
    <!-- End of Page Wrapper -->

</template>

<script lang="ts">
	import { Component, Vue, Prop} from 'vue-property-decorator';

	@Component({
		name: 'App',
	})
	export default class App extends Vue {
		@Prop() readonly keycloak!: string
	}
</script>
