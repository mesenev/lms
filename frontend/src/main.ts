import App from '@/App.vue';
import router from '@/router';
import { store } from '@/store';
import CarbonComponentsVue from '@carbon/vue/src/index';
import 'carbon-components/css/carbon-components.css';
import { Component, createApp } from 'vue';

createApp(App as unknown as Component)
  .use(store)
  .use(router)
  .use(CarbonComponentsVue)
  .mount('#app');
