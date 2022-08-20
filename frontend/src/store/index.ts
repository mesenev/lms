import Vue from 'vue';
import Vuex from 'vuex';
import axios from "axios";
import UserModel from "@/models/UserModel";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    access: '',
    refresh: '',
  },
  getters: {},
  mutations:{
    initializeStore(state){
      if ( localStorage.getItem('access') ){
        state.access = String(localStorage.getItem('access'));
      }
      else{
        state.access = '';
      }
    },
    setAccess(state, access){
      state.access = access;
    }
  },
  actions: {},
})
