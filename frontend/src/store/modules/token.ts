import store from '@/store';
import axios from 'axios';
import {Dictionary} from 'vue-router/types/router';
import {Action, getModule, Module, Mutation, VuexModule,} from 'vuex-module-decorators';

@Module({ namespaced: true, name: 'token', store, dynamic: true })
class TokenModule extends VuexModule{
  obtain_token_url = '/api/auth/jwt/create/';
  refresh_token_url = '/api/auth/jwt/refresh/';
  protected_user_data_url = '/api/auth/users/me/';
  access = '';
  refresh = '';

  @Mutation initializeStore(){
      console.log('InitializeStore:');
      if ( localStorage.getItem('access') && localStorage.getItem('refresh') ){
        console.log('LOCALSTORAGE-ACCESS:', localStorage.getItem('access'));
        console.log('LOCALSTORAGE-REFRESH', localStorage.getItem('refresh'));
        this.access = String(localStorage.getItem('access'));
        this.refresh = String(localStorage.getItem('refresh'));
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.access;
      }
      else{
        this.access = '';
        this.refresh = '';
      }
    }

  @Mutation setAccess(access: string){
      this.access = access;
      localStorage.setItem('access', access);
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.access;
  }

  @Mutation deleteAccess(){
      localStorage.setItem('access', '');
      this.access = '';
      axios.defaults.headers.common['Authorization'] = '';
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
