<template>
  <div class="shell-login">
    <cv-form @submit.prevent="authorization" class="login">
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
      <router-link :to="{ name: 'ResetPasswordView' }">Забыли пароль?</router-link>
      <div class="submit-btn">
        <cv-button type="submit" @click="authorization">Войти</cv-button>
      </div>
    </cv-form>
  </div>
</template>

<script lang="ts" setup>
import {useTokenStore} from "@/stores/modules/token";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import {ref} from "vue";

const {notificationText, notificationKind, showNotification, hideNotification} = useNotificationMixin();
const login = ref('');
const password = ref('');
const tokenStore = useTokenStore();

function authorization() {
  if (!login.value || !password.value) {
    console.log('ERROR');
    notificationText.value = `Пожалуйста заполните все поля`;
    notificationKind.value = 'error';
    showNotification.value = true;
    return;
  }
  tokenStore.login({
    username: login.value,
    password: password.value,
  }).catch(error => {
    if (error.response.status == 401) {
      notificationText.value = `Неверные логин или пароль`;
      notificationKind.value = 'error';
      showNotification.value = true;
    } else {
      notificationText.value = `Ошибка получения данных`;
      notificationKind.value = 'error';
      showNotification.value = true;
    }
  });
}

</script>

<style lang="stylus" scoped>
.login
  width 20%
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

:deep() .bx--password-input-wrapper
  padding-top 1rem
  padding-bottom 0.25rem

.pass-form
  padding-bottom 0.5rem

.main
  text-align center
  padding 5rem

.login-form
  padding 3rem
  background-color var(--cds-ui-background)
</style>
