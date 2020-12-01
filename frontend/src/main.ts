import App from '@/App.vue';

import router from '@/router';
import { store } from '@/store';
import CarbonComponentsVue from '@carbon/vue/src/index';
import Vue from 'vue';

Vue.use(CarbonComponentsVue);

new Vue({
  router,
  store,
  render(h) { return h(App); },
}).$mount('#app');
