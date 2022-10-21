import axios from "axios";
import store from '@/store';
import * as urls from '@/store/services/urls';

const BASE_URL = (process.env.NODE_ENV === "production")
  ? process.env.APPLICATION_URL : "http://localhost:8000";

axios.defaults.baseURL = BASE_URL;
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

const api = axios.create({
  headers: { "Content-Type": "application/json" }
});

api.interceptors.request.use(async config => {
  if (config.url != urls.OBTAIN_TOKEN_URL) {
    await axios.post(
      urls.VERIFY_TOKEN_URL,
      { token: String(localStorage.getItem('access')) }
    ).then(response => {
      config.headers['Authorization'] = 'Bearer ' + String(localStorage.getItem('access'));
    }).catch(error => {
      localStorage.setItem('access', '');
    });
    if (!localStorage.getItem('access')) {
      const refresh = String(localStorage.getItem('refresh'));
      await axios.post(
        urls.REFRESH_TOKEN_URL,
        { refresh: localStorage.getItem('refresh') }
      ).then(response => {
          localStorage.setItem('access', response.data.access);
          config.headers['Authorization'] = 'Bearer ' + String(localStorage.getItem('access'));
        }
      ).catch(error => {
        localStorage.setItem('refresh', '');
        store.commit('token/rejectAuthentication');
      });

      if (!localStorage.getItem('refresh'))
        await axios.post(urls.BLACKLIST_TOKEN_URL, { refresh: refresh });
    }
  }
  return config;
})


export default api;
