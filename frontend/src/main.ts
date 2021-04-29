import App from '@/App.vue';
import router from '@/router';

import store from '@/store';
import userStore from '@/store/modules/user';
import CarbonComponentsVue from '@carbon/vue/src/index';
import axios from 'axios';
import Clipboard from 'v-clipboard';
import Vue from 'vue';

Vue.use(Clipboard);
Vue.use(CarbonComponentsVue);

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';


Vue.config.productionTip = false;
Vue.config.devtools = true;


interface UserDataWrapper {
  userData: object;
}

userStore.receiveUser((window as unknown as UserDataWrapper).userData)

new Vue({
  router,
  store,
  render(h) { return h(App); },
}).$mount('#app');
