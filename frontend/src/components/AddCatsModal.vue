<template>
  <div>
    <cv-button class="cats-btn" @click="showModal">
      Добавить аккаунт cats
    </cv-button>
    <cv-modal
      :visible="modalVisible"
      class="add_cats_modal" size="small"
      @modal-hidden="modalHidden">
      <template slot="title">
        Добавить аккаунт
      </template>
      <template slot="content">
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
            <template slot="helper-text">
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

<script lang="ts">


import { Component } from 'vue-property-decorator';
import api from '@/store/services/api'
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import userStore from "@/store/modules/user";


@Component({ components: {} })
export default class AddCatsModal extends NotificationMixinComponent {
  modalVisible = false;
  catsLogin = '';
  catsPassword = '';
  catsPasswordRepeat = '';
  transmittingData = false;
  userStore = userStore;


  get isButtonDisabled() {
    return this.catsPassword.length === 0 || (this.catsPassword !== this.catsPasswordRepeat);
  }

  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
  }

  async buttonHandler() {
    this.transmittingData = true;
    await api.post('/api/cats_account/', {
      login: this.catsLogin,
      passwd: this.catsPassword
    })
      .then(response => {
        this.notificationKind = 'success';
        if (response.status === 201) {
          this.notificationText = 'Аккаунт успешно привязан';
        }
        if (response.status === 202) {
          this.notificationText = 'Аккаунт успешно обновлён';
        }
        this.userStore.receiveUser({
          ...this.userStore.user,
          cats_account: response.data.cats_id
        });
        this.$emit('fetch-cats-account');
        this.showNotification = true;
      })
      .catch(error => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так: ${error.message}`;
        this.showNotification = true;
        console.error(error);
      })
    this.transmittingData = false;
  }
}
</script>

<style scoped lang="stylus">
.add_cats_modal
  /deep/ .bx--modal-container
    width: fit-content

  /deep/ .bx--modal-content
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
