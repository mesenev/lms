import Vue from 'vue';
import * as Sentry from '@sentry/vue';
import { Integrations } from '@sentry/tracing';
import App from '@/App.vue';

import router from '@/router';
import store from '@/store';
import CarbonComponentsVue from '@carbon/vue/src/index';
import axios from 'axios';
import VueClipboard from 'vue-clipboard2';

if (process.env.VUE_APP_ENVIRONMENT !== 'development') {
    Sentry.init({
	    Vue,
	    environment: process.env.VUE_APP_ENVIRONMENT,
	    release: `${process.env.VUE_APP_NAME}@${process.env.VUE_APP_VERSION}`,
	    dsn: process.env.SENTRY_FRONTEND_DSN,
	    integrations: [
		    new Integrations.BrowserTracing({
			    tracingOrigins: [process.env.APPLICATION_URL, /^\//],
			}),
		],
		debug: process.env.VUE_APP_ENVIRONMENT  !==  'production',
		tracesSampleRate: process.env.VUE_APP_ENVIRONMENT === 'production' ? 0.2 : 1,
		tracingOptions: {
			trackComponents: true,
		},
		// Vue specific
		logErrors: process.env.VUE_APP_ENVIRONMENT === 'production' ? false : true,
		attachProps: true,
		attachStacktrace: true,
	});
}

Vue.use(VueClipboard);
Vue.use(CarbonComponentsVue);
VueClipboard.config.autoSetContainer = true;

Vue.config.productionTip = false;
Vue.config.devtools = true;

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

interface UserDataWrapper {
  userData: object;
}

new Vue({
  router,
  store,
  render(h) { return h(App); },
}).$mount('#app');
