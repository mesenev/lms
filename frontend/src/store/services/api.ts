import axios from "axios";
import tokenStore from '@/store/modules/token';

const BASE_URL = (process.env.NODE_ENV === "production")
  ? process.env.APPLICATION_URL : "http://localhost:8000";

axios.defaults.baseURL = BASE_URL;
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

const api = axios.create({
  headers: { "Content-Type": "application/json" }
});

api.interceptors.request.use(async config => {
  if (config.url != tokenStore.OBTAIN_TOKEN_URL) {
    await axios.post(
      tokenStore.VERIFY_TOKEN_URL,
      { token: String(localStorage.getItem('access')) }
    ).then(response => {
      config.headers['Authorization'] = 'Bearer ' + String(localStorage.getItem('access'));
    }).catch(error => {
      localStorage.setItem('access', '');
    });
    if (!localStorage.getItem('access')) {
      const refresh = String(localStorage.getItem('refresh'));
      await axios.post(
        tokenStore.REFRESH_TOKEN_URL,
        { refresh: localStorage.getItem('refresh') }
      ).then(response => {
          localStorage.setItem('access', response.data.access);
          config.headers['Authorization'] = 'Bearer ' + String(localStorage.getItem('access'));
        }
      ).catch(error => {
        localStorage.setItem('refresh', '');
        tokenStore.context.commit('rejectAuthentication');
      });

      if (!localStorage.getItem('refresh'))
        await axios.post(tokenStore.BLACKLIST_TOKEN_URL, { refresh: refresh });
    }
  }
  return config;
})


export default api;
