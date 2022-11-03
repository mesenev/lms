<template>
  <div class="shell-login">
      <div class="login">
        <cv-inline-notification
        @close="hideNotification"
        v-if="showNotification"
        :kind="notificationKind"
        :sub-title="notificationText">
        </cv-inline-notification>

       <h3 class="form-header">Авторизация</h3>
          <cv-text-input
            class="log-form"
            label="Логин"
            placeholder="Введите свой логин"
            v-model="login">
          </cv-text-input>
          <cv-text-input
            class="pass-form"
            type="password"
            label="Пароль"
            placeholder="Введите свой пароль"
            v-model="password"
          >
          </cv-text-input>
        <cv-link >Забыли пароль?</cv-link>
          <div class="submit-btn">
            <cv-button @click="authorization">Войти</cv-button>
          </div>
      </div>
    </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import tokenStore from "@/store/modules/token";
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";

@Component({ components: {} })
export default class LoginView extends NotificationMixinComponent {
  login = '';
  password = '';
  tokenStore = tokenStore;
  async authorization(){
    if (!this.login || !this.password){
      this.notificationText = `Пожалуйста заполните все поля`;
      this.notificationKind = 'error';
      this.showNotification = true;
      return;
    }
    await this.tokenStore.login({
      username: this.login,
      password: this.password,
    }).catch( error=> {
      if(error.response.status == 401) {

        this.notificationText = `Неверные логин или пароль`;
        this.notificationKind = 'error';
        this.showNotification = true;
      }
      else{
        this.notificationText = `Ошибка получения данных`;
        this.notificationKind = 'error';
        this.showNotification = true;
      }
      })

  }
}
</script>

<style lang="stylus" scoped>


.login
  width 40%
  text-align end
  @media (min-width: 401px)
    min-width 400px
  @media (max-width: 400px)
    min-width 80%

.shell-login
  position absolute
  width 100%
  height 100%
  display flex
  flex-direction column
  align-items center
  justify-content center

.submit-btn
  display flex
  flex-direction row
  justify-content center

.form-header
  text-align center
  padding-bottom 2rem

.log-form
  padding-bottom 2rem

.pass-form
  padding-bottom 0.5rem

.main
  text-align center
  padding 5rem

.login-form
  padding 3rem
  background-color var(--cds-ui-background)


</style>
