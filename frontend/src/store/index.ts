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
  mutations:{
    initializeStore(state){
      if ( localStorage.getItem('access') && localStorage.getItem('refresh') ){
        console.log('LOCALSTORAGE-ACCESS:', localStorage.getItem('access'));
        console.log('LOCALSTORAGE-REFRESH', localStorage.getItem('refresh'));
        state.access = String(localStorage.getItem('access'));
        state.refresh = String(localStorage.getItem('refresh'));
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + state.access;
      }
      else{
        state.access = '';
        state.refresh = '';
      }
    },
    setAccess(state, access){
      state.access = access;
      localStorage.setItem('access', access);
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + state.access;
    },
    deleteAccess(state){
      localStorage.setItem('access', '');
      state.access = '';
      axios.defaults.headers.common['Authorization'] = '';
    },
    setRefresh(state, refresh){
      state.refresh = refresh;
      localStorage.setItem('refresh', refresh);
    },
    deleteRefresh(state){
      localStorage.setItem('refresh', '');
      state.refresh = '';
    }
  },
  actions: {},
})
