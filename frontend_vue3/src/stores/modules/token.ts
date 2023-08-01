import userStore from 'src/stores/modules/user';
import api from "src/stores/services/api";
import * as urls from 'src/stores/services/urls';
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useTokenStore = defineStore('token', () => {

  const isLoading = ref(false);
  const isAuthenticated = ref(false);

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
          isAuthenticated.value = true;
        }
      )
    }
  }

  async function setupTokenStore() {
    if (String(localStorage.getItem('access')))
      isLoading.value = true
      await api.get(urls.PROTECTED_USER_DATA_URL).then(
          (response: { data: any; }) => {
          userStore.receiveUser(response.data);
          isAuthenticated.value = true;
        }).catch(error => {
        console.log(error);
      });
      isLoading.value= false;
  }

  async function logout() {
    await api.post(
      urls.BLACKLIST_TOKEN_URL,
      { refresh: localStorage.getItem('refresh') }
    ).then((response: any) => {
      localStorage.setItem('access', '');
      localStorage.setItem('refresh', '');
      isAuthenticated.value = false;
    });
  }

  return { isLoading, isAuthenticated, login, setupTokenStore, logout }
})

