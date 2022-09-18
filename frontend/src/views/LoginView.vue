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
import tokenStore from "@/store/modules/token";

@Component({ components: {} })
export default class LoginView extends Vue {
  login = '';
  password = '';

  async authorization(){
    const payload = {
      username: this.login,
      password: this.password
    }
    await tokenStore.login(payload);
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
