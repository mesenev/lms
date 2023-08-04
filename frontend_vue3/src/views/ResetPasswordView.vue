<template>
  <div class="form">
    <h3 class="form-header">Восстановление пароля</h3>
    <cv-inline-notification
      @close="hideNotification"
      v-if="showNotification"
      :kind="notificationKind"
      :sub-title="notificationText">
    </cv-inline-notification>
    <cv-form @submit.prevent="buttonHandler" class="reset-password" v-if="!isCorrectTokenProvided">
      <cv-text-input
        class="log-form"
        label="Email"
        placeholder="Введите свой Email"
        type="email"
        v-model="email">
      </cv-text-input>
      <div class="submit-btn">
        <cv-button>Восстановить пароль</cv-button>
      </div>
    </cv-form>
    <cv-form class="reset-password" @submit.prevent="resetPassword" v-else-if="isTokenProvided">
      <cv-text-input
        class="log-form"
        label="Новый пароль"
        placeholder="Введите новый"
        type="password"
        v-model="password">
      </cv-text-input>
      <cv-text-input
        class="log-form"
        label="Подтверждение пароля"
        placeholder="Введите пароль еще раз"
        type="password"
        v-model="password_repeat">
      </cv-text-input>
      <div class="submit-btn">
        <cv-button :disabled="password === '' || password_repeat === ''">Изменить пароль</cv-button>
      </div>
    </cv-form>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import api from "@/store/services/api";

@Component({ components: {} })
export default class ResetPasswordView extends NotificationMixinComponent {
  email = '';
  password = '';
  password_repeat = '';
  isCorrectTokenProvided = false;

  async buttonHandler() {
    await api.post('/api/password_reset/request_token', { "email": this.email })
      .then(response => {
        this.notificationKind = 'success';
        this.notificationText = 'Ссылка для восстановления пароля была отправлена на вашу электронную почту.';
        if (response.status === 200)
          this.showNotification = true;
      })
      .catch(error => {
        this.notificationKind = 'error';
        if (error.response && error.response.status === 404)
          this.notificationText = 'Пользователя с таким адресом электронной почты не существует';
        else
          this.notificationText = `Что-то пошло не так: ${error.message}`;
      })
      .finally(() => this.showNotification = true)
  }

  async resetPassword() {
    if (this.password === this.password_repeat) {
      api.post('/api/password_reset/with_token', {
        password: this.password,
        token: this.token
      }, { params: { token: this.token } })
        .then(() => {
          this.$router.push('/login')
        })
        .catch(error => {
          this.notificationKind = 'error';
          this.notificationText = `Что-то пошло не так: ${error.message}`
        })
        .finally(() => this.showNotification = true)
    } else {
      this.notificationKind = 'error';
      this.notificationText = 'Пароли не совпадают';
      this.showNotification = true;
    }
  }

  get isTokenProvided() {
    return this.$route.query.hasOwnProperty('token');
  }

  get token() {
    return this.$route.query.token;
  }

  created() {
    if (this.$route.query.hasOwnProperty('token'))
      api.get('/api/password_reset/verify_token', { params: { token: this.$route.query.token } })
        .then(() => {
          this.isCorrectTokenProvided = true;
        })
        .catch(() => {
          this.isCorrectTokenProvided = false;
          this.notificationKind = 'error';
          this.notificationText = 'Что-то пошло не так: Токен для восстановления пароля неверный.';
          this.showNotification = true;
        })
  }
}
</script>

<style lang="stylus" scoped>


.reset-password
  width 20%
  text-align end
  @media (min-width: 401px)
    min-width 400px
  @media (max-width: 400px)
    min-width 80%

.form
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
