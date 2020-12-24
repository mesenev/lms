import App from '@/App.vue';

import router from '@/router';
import { store } from '@/store';
import CarbonComponentsVue from '@carbon/vue/src/index';
import Vue from 'vue';

import { CarbonIconsVue } from '@carbon/icons-vue';

Vue.use(CarbonComponentsVue);
// TODO долго собирается/перезагружается страница
Vue.use(CarbonIconsVue, {
  components: {},
});

new Vue({
  router,
  store,
  render(h) { return h(App); },
}).$mount('#app');
