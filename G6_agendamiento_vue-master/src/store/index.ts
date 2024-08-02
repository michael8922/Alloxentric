import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: null,
    tokenParsed: null,
    permissions: null,
    isConnected: false,
    agent_connected: false,
    conversations: [],
    client: "",
    chatOpen: false
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    setTokenParsed(state, tokenParsed) {
      state.tokenParsed = tokenParsed;
      state.client = tokenParsed.groups[0];
      //console.log("cliente:", state.client)
    },
    setPermissions(state, permissions) {
      state.permissions = permissions;
    },
  },
  getters: {
  },
  actions: {
    guardarToken({ commit }, keycloak) {
      if (keycloak) {
        //Se valida si usuario viene con un grupo asignado en keycloak si no lo tiene se desloguea automaticamente
        if (!keycloak.tokenParsed.groups[0]) {
          console.log("Error: Usuario no tiene grupo asignado en keycloak")
          keycloak.logout()
        }
        console.log("Cliente:", keycloak.tokenParsed.groups[0])
        localStorage.setItem("token", keycloak.token)
        commit("setToken", keycloak.token)
        commit("setTokenParsed", keycloak.tokenParsed)

        const config = {
          headers: { Authorization: `Bearer ${keycloak.token}` }
        };

        const params = new URLSearchParams()
        params.append('grant_type', 'urn:ietf:params:oauth:grant-type:uma-ticket')
        params.append('audience', process.env.VUE_APP_KEYCLOAK_AUDIENCE)
        params.append('response_mode', 'permissions')

        axios.post(process.env.VUE_APP_KEYCLOAK_TOKEN_URL, params, config)
          .then(function (response) {
            //console.log(response.data)
            commit("setPermissions", response.data)

            if (response.data.error) {
              console.log(response.data.error)
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },
  },
  modules: {
  }
})
