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
            v-model.trim="catsPasswordRepeat"
          />
          <span class="form__notification">Пароль для аккаунта не сохраняется
            <cv-tooltip tip="Пароль используется исключительно для верификации аккаунта"/>
          </span>
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


import { Component, Vue } from 'vue-property-decorator';
import axios from "axios";
import SubmitModel from "@/models/SubmitModel";
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";


@Component({ components: {} })
export default class AddCatsModal extends NotificationMixinComponent {
  modalVisible = false;
  catsLogin = '';
  catsPassword = '';
  catsPasswordRepeat = '';
  transmittingData = false;


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
    await axios.post('/api/cats_account/', {
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
.add_cats_modal /deep/ .bx--modal-container {
  width: 25%;
}

.btns
  float left;
  cursor: pointer;
  clear: both;
  display flex;
  flex-direction row;

.form__notification
  font-size small
  color var(--cds-text-02)
  margin 1rem 0

.input
  width 300px
  padding-bottom 24px
</style>
