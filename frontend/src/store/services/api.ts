import axios from "axios";
import tokenStore from '@/store/modules/token'


const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(async config=>{
  console.log('access: ', String(localStorage.getItem('access')))
  console.log('refresh: ', localStorage.getItem('refresh'))
  if ( config.url != tokenStore.OBTAIN_TOKEN_URL && String(localStorage.getItem('access')) ) {
    await axios.post(tokenStore.VERIFY_TOKEN_URL, { token: String(localStorage.getItem('access')) }).then(
      response => {
        config.headers['Authorization'] = 'Bearer ' + String(localStorage.getItem('access'));
      }).catch(error =>{
        localStorage.setItem('access', '');
    });
    if ( !localStorage.getItem('access') && localStorage.getItem('refresh') ){
      const refresh = String(localStorage.getItem('refresh'));
      await axios.post(tokenStore.REFRESH_TOKEN_URL, {refresh: localStorage.getItem('refresh') }).then(
        response =>{
          localStorage.setItem('access', response.data.access);
          config.headers['Authorization'] = 'Bearer ' + String(localStorage.getItem('access'));
        }
      ).catch(error=>{
        localStorage.setItem('refresh', '');
        tokenStore.context.commit('rejectAuthentication');
      })

      if ( !localStorage.getItem('refresh') ) {
        await axios.post(tokenStore.BLACKLIST_TOKEN_URL, { refresh: refresh })
      }
    }
  }
  return config;
})


export default api;
