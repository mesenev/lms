import useUserStore from "@/stores/modules/user";
import api from "@/stores/services/api";
import * as urls from '@/stores/services/urls';
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'


export const useTokenStore = defineStore('token', () => {

  const userStore = useUserStore()

  const loading = ref(false);
  const authentication = ref(false);

  const isLoading = computed(() => { return loading.value })
  const isLogin = computed(() => { return authentication.value })



  async function login(payload: { username: string; password: string}) {
    await api.post(urls.OBTAIN_TOKEN_URL,
      { username: payload.username, password: payload.password }).then(
          (response: { data: { access: string; refresh: string; }; }) => {
        if (response.data.access && response.data.refresh) {
          localStorage.setItem('access', response.data.access);
          localStorage.setItem('refresh', response.data.refresh);
        }
      }
    ).catch((error: any) =>{
      return Promise.reject(error)
    })

    if (String(localStorage.getItem('access'))) {
      await api.get(urls.PROTECTED_USER_DATA_URL).then(
          (response: { data: any; }) => {
          userStore.receiveUser(response.data);
          acceptAuthentication();
        }
      )
    }
  }

  async function setupTokenStore() {
    if (String(localStorage.getItem('access')))
      setIsLoading();
      console.log(isLoading.value)
      await api.get(urls.PROTECTED_USER_DATA_URL).then(
          (response: { data: any; }) => {
          userStore.receiveUser(response.data);
          acceptAuthentication();
        }).catch(error => {
        console.log(error);
      });
      denyIsLoading();
      console.log(isLoading.value)

  }

  async function logout() {
    await api.post(
      urls.BLACKLIST_TOKEN_URL,
      { refresh: localStorage.getItem('refresh') }
    ).then((response: any) => {
      localStorage.setItem('access', '');
      localStorage.setItem('refresh', '');
      rejectAuthentication();
    });
  }

  function acceptAuthentication() {
    authentication.value = true;
  }

  function rejectAuthentication() {
    authentication.value = false;
  }

  function setIsLoading(){
    loading.value = true;
  }

  function denyIsLoading(){
    loading.value = false;
  }

  return { loading, authentication, isLoading, isLogin, login, setupTokenStore, logout,
      acceptAuthentication, rejectAuthentication, setIsLoading, denyIsLoading }
})

