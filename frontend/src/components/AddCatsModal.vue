<template>
  <div>
    <cv-button class="cats-btn" @click="showModal">
      Добавить аккаунт cats
    </cv-button>
    <cv-modal
        :visible="modalVisible"
        class="add_cats_modal" size="small"
        @modal-hidden="modalHidden">
      <template v-slot:title>
        Добавить аккаунт
      </template>
      <template v-slot:content>
        <cv-inline-notification
            v-if="showNotification"
            :kind="notificationKind"
            :sub-title="notificationText"
            @close="hideNotification"
        />
        <div>
          <cv-text-input
              class="input"
              label="Введите логин cats:"
              v-model.trim="catsLogin"
          />
          <cv-text-input
              class="input"
              type="password"
              label="Введите пароль cats:"
              v-model.trim="catsPassword"
          />
          <cv-text-input
              class="input"
              type="password"
              label="Повторите пароль:"
              v-model.trim="catsPasswordRepeat">
            <template v-slot:helper-text>
              <span class="form__notification">Пароль для аккаунта не сохраняется
              <cv-tooltip tip="Пароль используется исключительно для верификации аккаунта"/>
              </span>
            </template>
          </cv-text-input>
        </div>
        <div class="btns">
          <cv-button-skeleton class="btn" v-if="transmittingData">Добавить</cv-button-skeleton>
          <cv-button
              :disabled="isButtonDisabled"
              v-else
              class="btn"
              @click="buttonHandler">
            Добавить
          </cv-button>
        </div>
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts" setup>


import api from '@/stores/services/api'
import useUserStore from "@/stores/modules/user";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import {computed, ref} from "vue";


const {notificationText, notificationKind, showNotification, hideNotification} = useNotificationMixin();

const emits = defineEmits(['fetch-cats-account']);

const modalVisible = ref(false);
const catsLogin = ref('');
const catsPassword = ref('');
const catsPasswordRepeat = ref('');
const transmittingData = ref(false);
const userStore = useUserStore();


const isButtonDisabled = computed(() => {
  return catsPassword.value.length === 0 || (catsPassword.value !== catsPasswordRepeat.value);
})

function showModal() {
  modalVisible.value = true;
}

function modalHidden() {
  modalVisible.value = false;
}

async function buttonHandler() {
  transmittingData.value = true;
  await api.post('/api/cats_account/', {
    login: catsLogin.value,
    passwd: catsPassword.value
  })
      .then(response => {
        notificationKind.value = 'success';
        if (response.status === 201) {
          notificationText.value = 'Аккаунт успешно привязан';
        }
        if (response.status === 202) {
          notificationText.value = 'Аккаунт успешно обновлён';
        }
        userStore.receiveUser({
          ...userStore.user,
          cats_account: response.data.cats_id
        });
        emits('fetch-cats-account');
        showNotification.value = true;
      })
      .catch(error => {
        notificationKind.value = 'error';
        notificationText.value = `Что-то пошло не так: ${error.message}`;
        showNotification.value = true;
        console.error(error);
      })
  transmittingData.value = false;
}
</script>

<style scoped lang="stylus">
.add_cats_modal
  :deep() .bx--modal-container
    width: fit-content

  :deep() .bx--modal-content
    padding 0 4rem 0 0
    margin-left 1rem
    margin-bottom 1rem
    overflow hidden

.btns
  float left;
  cursor: pointer;
  clear: both;
  display flex;
  flex-direction row;

.form__notification
  display flex
  align-items center
  font-size small
  gap 0.5rem
  color var(--cds-text-02)

.input
  width 300px
  padding-bottom 24px
</style>
