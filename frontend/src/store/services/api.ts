import axios from "axios";
import store from '@/store';
import * as urls from '@/store/services/urls';
import token from "@/store/modules/token";
import router from '@/router/index'

const BASE_URL = (process.env.NODE_ENV === "production")
  ? process.env.APPLICATION_URL : "http://localhost:8000";

axios.defaults.baseURL = BASE_URL;
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

const api = axios.create({
  headers: { "Content-Type": "application/json" }
});

api.interceptors.request.use(async config => {
  console.log('NEXT URL IN INTERSEPTOR: ', token.next_url)
  if (config.url == urls.OBTAIN_TOKEN_URL)
    return config;

  if (!localStorage.getItem('refresh')) {
    store.commit('token/rejectAuthentication');
    return config;
  }

  if ((localStorage.getItem('access')))

    await axios.post(
      urls.VERIFY_TOKEN_URL,
      { token: (localStorage.getItem('access')) }
    ).then(response => {
      config.headers['Authorization'] = 'Bearer ' + (localStorage.getItem('access'));
      router.replace(token.next_url);
    }).catch(error => {
      localStorage.setItem('access', '');
    });

  if (!localStorage.getItem('access')) {
    const refresh = (localStorage.getItem('refresh'));

    await axios.post(
      urls.REFRESH_TOKEN_URL,
      { refresh: localStorage.getItem('refresh') }
    ).then(response => {
        localStorage.setItem('access', response.data.access);
        config.headers['Authorization'] = 'Bearer ' + (localStorage.getItem('access'));
        router.replace(token.next_url);
      }
    ).catch(error => {
      localStorage.setItem('refresh', '');
      store.commit('token/rejectAuthentication');

    });

    if (!localStorage.getItem('refresh'))
      await axios.post(urls.BLACKLIST_TOKEN_URL, { refresh: refresh });

  }
  return config;

})


export default api;
