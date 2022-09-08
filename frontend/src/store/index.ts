import Vue from 'vue';
import Vuex from 'vuex';
import axios from "axios";
import UserModel from "@/models/UserModel";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    obtain_token_url: '/api/auth/jwt/create/',
    refresh_token_url: '/api/auth/jwt/refresh/',
    protected_user_data_url: '/api/auth/users/me/',
    access: '',
    refresh: '',
  },
  getters: {},
  mutations:{},
  actions: {},
})
