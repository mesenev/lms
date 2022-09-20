import store from '@/store';
import userStore from '@/store/modules/user'
import {Action, getModule, Module, Mutation, VuexModule,} from 'vuex-module-decorators';
import api from '@/store/services/axiosInstance'
import setupInterseptor from '@/store/services/interceptors'

@Module({ namespaced: true, name: 'token', store, dynamic: true })
class TokenModule extends VuexModule{
  OBTAIN_TOKEN_URL = '/api/auth/jwt/create/';
  REFRESH_TOKEN_URL = '/api/auth/jwt/refresh/';
  PROTECTED_USER_DATA_URL = '/api/auth/users/me/';
  VERIFY_TOKEN_URL = '/api/auth/jwt/verify/';
  KILL_TOKEN_URL = '/api/auth/jwt/logout/'
  access = '';
  refresh = '';
  isAuthenticated = false;

  @Action async login(payload: {username: string; password: string}){
    await api.post(this.OBTAIN_TOKEN_URL, {username: payload.username, password: payload.password}).then(
      response => {
        if ( response.data.access && response.data.refresh ){
          this.context.commit("setAccess",  response.data.access);
          this.context.commit("setRefresh", response.data.refresh);
        }
      }
    );
    if ( this.access ){
      await api.get(this.PROTECTED_USER_DATA_URL).then(
        response => {
          console.log(response.data);
          userStore.context.commit('receiveUser', response.data);
          this.context.commit('acceptAuthentication');
        }
      ).catch(error => {
        console.log(error);
      })
    }
  }

  @Action async setupTokenStore(){
    if ( localStorage.getItem('access') && localStorage.getItem('refresh') ){
      this.context.commit('getAccessFromLocalStorage');
      this.context.commit('getRefreshFromLocalStorage');
      await api.get(this.PROTECTED_USER_DATA_URL).then(response =>{
        userStore.receiveUser(response.data);
        this.context.commit('acceptAuthentication');
      }).catch(error =>{
        console.log(error);
      });
    }
  }

  @Action async logout(){
    await api.post(this.KILL_TOKEN_URL).then(response =>
      this.context.commit('rejectAuthentication'));
  }

  @Mutation acceptAuthentication(){
    this.isAuthenticated = true;
  }

  @Mutation rejectAuthentication(){

    localStorage.setItem('access', '');
    this.access = '';
    api.defaults.headers.common['Authorization'] = '';

    localStorage.setItem('refresh', '');
    this.refresh = '';
    this.isAuthenticated = false;
  }

  @Mutation getAccessFromLocalStorage(){
    this.access = String(localStorage.getItem('access'));
    api.defaults.headers.common['Authorization'] = 'Bearer ' + this.access;
  }

  @Mutation getRefreshFromLocalStorage(){
    this.refresh = String(localStorage.getItem('refresh'));
  }

  @Mutation setAccess(access: string){
      this.access = access;
      localStorage.setItem('access', access);
      api.defaults.headers.common['Authorization'] = 'Bearer ' + this.access;
  }

  @Mutation deleteAccess(){
      localStorage.setItem('access', '');
      this.access = '';
      api.defaults.headers.common['Authorization'] = '';
  }

  @Mutation setRefresh(refresh: string){
      this.refresh = refresh;
      localStorage.setItem('refresh', refresh);
  }

  @Mutation deleteRefresh(){
      localStorage.setItem('refresh', '');
      this.refresh = '';
    }
}

export default getModule(TokenModule);
