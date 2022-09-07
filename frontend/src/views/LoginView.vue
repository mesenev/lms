<template>
  <div class="bx--grid main">
    <div class="bx--row">
      <div class="bx--col-lg-6 login-form">
        <cv-form>
          <h3 class="form-header">Авторизация</h3>
          <cv-text-input
            class="log-form"
            label="Логин"
            placeholder="Введите свой логин"
            v-model="login">
          </cv-text-input>
          <cv-text-input
            class="pass-form"
            label="Пароль"
            placeholder="Введите свой пароль"
            v-model="password">
          </cv-text-input>
          <div class="submit-btn">
            <cv-button @click="authorization">Войти</cv-button>
          </div>
        </cv-form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Component from "vue-class-component";
import Vue from "vue";
import axios from "axios";
import userStore from '@/store/modules/user';
import HomeView from "@/views/HomeView.vue";
import UserModel from "@/models/UserModel";

@Component({ components: {} })
export default class LoginView extends Vue {
  login = '';
  password = '';

  authorization(){
    axios.post(this.$store.state.obtain_token_url, {username: this.login, password: this.password}).
    then(response => {
      const access = response.data.access;
      this.$store.commit('setAccess', access);
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + access;
      localStorage.setItem('access', access);
      axios.get(this.$store.state.protected_user_data_url).then(response => {
          userStore.receiveUser(response as unknown as UserModel);
        }
      ).catch(error => console.log('ERROR!!!!', error))
      this.$router.push('/');
      }).catch(error=>{
        console.log(error)
    })
  }
}
</script>

<style lang="stylus" scoped>

.submit-btn
  display flex
  flex-direction row
  justify-content center

.form-header
  padding-bottom 2rem

.log-form
  padding-bottom 2rem

.pass-form
  padding-bottom 2rem

.main
  text-align center
  padding 5rem

.login-form
  padding 3rem
  background-color var(--cds-ui-background)


</style>
