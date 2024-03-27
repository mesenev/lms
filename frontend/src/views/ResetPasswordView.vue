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

<script lang="ts" setup>
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import { computed, onMounted, ref } from "vue";
import api from "@/stores/services/api";
import { useRoute, useRouter } from "vue-router";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const route = useRoute();
const router = useRouter();

const email = ref('');
const password = ref('');
const password_repeat = ref('');
const isCorrectTokenProvided = ref(false);

const isTokenProvided = computed(() => {
  return route.query.hasOwnProperty('token');
})

const token = computed(() => {
  return route.query.token;
})

async function buttonHandler() {
  await api.post('/api/password_reset/request_token', { "email": email.value })
      .then(response => {
        notificationKind.value = 'success';
        notificationText.value = 'Ссылка для восстановления пароля была отправлена на вашу электронную почту.';
        if (response.status === 200)
          showNotification.value = true;
      })
      .catch(error => {
        notificationKind.value = 'error';
        if (error.response && error.response.status === 404)
          notificationText.value = 'Пользователя с таким адресом электронной почты не существует';
        else
          notificationText.value = `Что-то пошло не так: ${error.message}`;
      })
      .finally(() => showNotification.value = true)
}

async function resetPassword() {
  if (password.value === password_repeat.value) {
    api.post('/api/password_reset/with_token', {
      password: password.value,
      token: token
    }, { params: { token: token } })
        .then(() => {
          router.push('/login')
        })
        .catch(error => {
          notificationKind.value = 'error';
          notificationText.value = `Что-то пошло не так: ${error.message}`
        })
        .finally(() => showNotification.value = true)
  } else {
    notificationKind.value = 'error';
    notificationText.value = 'Пароли не совпадают';
    showNotification.value = true;
  }
}

onMounted(() => {
  if (route.query.hasOwnProperty('token'))
    api.get('/api/password_reset/verify_token', { params: { token: route.query.token } })
        .then(() => {
          isCorrectTokenProvided.value = true;
        })
        .catch(() => {
          isCorrectTokenProvided.value = false;
          notificationKind.value = 'error';
          notificationText.value = 'Что-то пошло не так: Токен для восстановления пароля неверный.';
          showNotification.value = true;
        })
})

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
