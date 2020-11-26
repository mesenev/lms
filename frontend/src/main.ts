import { createApp, Component } from 'vue';
import router from '@/router';
import store from '@/store';
import App from './App.vue';

createApp(
  App as unknown as Component,
).use(store).use(router).mount('#app');
