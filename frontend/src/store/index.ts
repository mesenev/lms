import Vuex from 'vuex';
import { getModule } from 'vuex-module-decorators';
import MainStore from './MainStorage';

export const store = new Vuex.Store({
  state: {},
  modules: {
    MainStore,
  },
});

export const mainStore = getModule(MainStore, store);
