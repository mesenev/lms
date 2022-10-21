import axios from "axios";
import store from '@/store';
import userStore from '@/store/modules/user';
import { Action, getModule, Module, Mutation, VuexModule, } from 'vuex-module-decorators';

@Module({ namespaced: true, name: 'token', store, dynamic: true })
class TokenModule extends VuexModule {
  OBTAIN_TOKEN_URL = '/api/auth/jwt/create/';
  REFRESH_TOKEN_URL = '/api/auth/jwt/refresh/';
  PROTECTED_USER_DATA_URL = '/api/auth/users/me/';
  VERIFY_TOKEN_URL = '/api/auth/jwt/verify/';
  BLACKLIST_TOKEN_URL = '/api/logout/';
  isAuthenticated = false;

  @Action
  async login(payload: { username: string; password: string }) {
    await axios.post(this.OBTAIN_TOKEN_URL,
      { username: payload.username, password: payload.password }).then(
      response => {
        debugger;
        if (response.data.access && response.data.refresh) {
          localStorage.setItem('access', response.data.access);
          localStorage.setItem('refresh', response.data.refresh);
        }
      }
    ).catch(error => console.log(error));
    if (String(localStorage.getItem('access'))) {
      await axios.get(this.PROTECTED_USER_DATA_URL).then(
        response => {
          userStore.context.commit('receiveUser', response.data);
          this.context.commit('acceptAuthentication');
        }
      ).catch(error => {
        console.log(error);
      })
    }
  }

  @Action
  async setupTokenStore() {
    await axios.get(this.PROTECTED_USER_DATA_URL).then(response => {
      userStore.receiveUser(response.data);
      this.context.commit('acceptAuthentication');
    }).catch(error => {
      console.log(error);
    });
  }

  @Action
  async logout() {
    console.log('logout')
    await axios.post(
      this.BLACKLIST_TOKEN_URL,
      { refresh: localStorage.getItem('refresh') }
    ).then(response => {
      localStorage.setItem('access', '');
      localStorage.setItem('refresh', '');
      this.context.commit('rejectAuthentication');
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
