import store from '@/store';
import userStore from '@/store/modules/user';
import api from "@/store/services/api";
import * as urls from '@/store/services/urls';
import { Action, getModule, Module, Mutation, VuexModule, } from 'vuex-module-decorators';

@Module({ namespaced: true, name: 'token', store, dynamic: true })
class TokenModule extends VuexModule {
  isAuthenticated = false;

  @Action
  async login(payload: { username: string; password: string }) {
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
    console.log('logout')
    await api.post(
      urls.BLACKLIST_TOKEN_URL,
      { refresh: localStorage.getItem('refresh') }
    ).then(response => {
      localStorage.setItem('access', '');
      localStorage.setItem('refresh', '');
      this.rejectAuthentication();
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
