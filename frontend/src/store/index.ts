import Vue from 'vue';
import Vuex from 'vuex';

import { getModule } from 'vuex-module-decorators';
import MainStore from './MainStorage';

Vue.use(Vuex);
export const store = new Vuex.Store({
  state: {},
  modules: {
    MainStore,
  },
});

export const mainStore = getModule(MainStore, store);
