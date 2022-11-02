import store from '@/store';
import userStore from '@/store/modules/user';
import api from "@/store/services/api";
import * as urls from '@/store/services/urls';
import { Action, getModule, Module, Mutation, VuexModule, } from 'vuex-module-decorators';
import router from "@/router";

@Module({ namespaced: true, name: 'token', store, dynamic: true })
class TokenModule extends VuexModule {
  isAuthenticated = false;
  next_url = '';

  @Mutation setNextUrl(new_next_url: string){
    this.next_url = new_next_url;
  }

  @Action({rawError: true})
  async login(payload: { username: string; password: string; next_url: string }) {

    await api.post(urls.OBTAIN_TOKEN_URL,
      { username: payload.username, password: payload.password }).then(
      response => {
        if (response.data.access && response.data.refresh) {
          localStorage.setItem('access', response.data.access);
          localStorage.setItem('refresh', response.data.refresh);
        }
      }
    ).catch(error =>{
      return Promise.reject(error)
    })

    if (String(localStorage.getItem('access'))) {
      await api.get(urls.PROTECTED_USER_DATA_URL).then(
        response => {
          userStore.receiveUser(response.data);
          this.acceptAuthentication();
          router.replace(payload.next_url)
        }
      )
    }
  }

  @Action
  async setupTokenStore() {
    if (String(localStorage.getItem('access')))
      await api.get(urls.PROTECTED_USER_DATA_URL).then(
        response => {
          userStore.receiveUser(response.data);
          this.acceptAuthentication();
        }).catch(error => {
        console.log(error);
      });
  }

  @Action
  async logout() {
    await api.post(
      urls.BLACKLIST_TOKEN_URL,
      { refresh: localStorage.getItem('refresh') }
    ).then(response => {
      localStorage.setItem('access', '');
      localStorage.setItem('refresh', '');
      this.rejectAuthentication();
      router.replace('/login');
    });
  }

  @Mutation acceptAuthentication() {
    this.isAuthenticated = true;
  }

  @Mutation rejectAuthentication() {
    this.isAuthenticated = false;
  }
}

export default getModule(TokenModule);
