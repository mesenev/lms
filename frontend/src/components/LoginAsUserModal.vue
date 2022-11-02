<template>
  <div>
    <a
      v-if="isSessionUser"
      @click="logoutFromUser"
      class="cv-switcher-item-link bx--switcher__item-link"
    >
      Вернуться в свой аккаунт
    </a>
    <a
      v-else-if="isSuperUser"
      @click="showModal"
      class="cv-switcher-item-link bx--switcher__item-link"
    >
      Войти пользователем
    </a>
    <cv-modal
      :visible="modalVisible"
      class="login_as_user_modal" size="small"
      @modal-hidden="modalHidden"
    >
      <template slot="title">
        Войти пользователем
      </template>
      <template slot="content">
        <cv-inline-notification
          v-if="showNotification"
          :kind="notificationKind"
          :sub-title="notificationText"
          @close="hideNotification"
        />
        <div class="content_container">
          <cv-text-input
            placeholder="Введите username"
            v-model.trim="username"
            data-modal-primary-focus
              />
          <cv-button
            class="content_btn"
            :disabled="emptyUsername"
            @click="loginAsUser"
          >
            Войти
          </cv-button>
        </div>
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">

import {Component} from 'vue-property-decorator';
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import userStore from "@/store/modules/user";
import UserModel from "@/models/UserModel";
import api from '@/store/services/api';


@Component({ components: {} })
export default class LoginAsUserModal extends NotificationMixinComponent {
  store = userStore;

  username = "";

  sessionUser: UserModel | undefined | string;

  modalVisible = false;

  isSessionUser = false;
  isSuperUser= false;

  async created() {
    this.sessionUser = await this.store.fetchUserFromSession();
    await this.checkUserStatus();
    if (typeof this.sessionUser === 'object') {
      this.isSessionUser = true;
    }
  }

  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
  }

  get emptyUsername(): boolean {
    return this.username.length === 0;
  }

  async checkUserStatus() {
    await api.get('/api/issuperuser')
        .then(response => {
          this.isSuperUser = response.data
        })
        .catch(error => {
          console.log(error);
        })
  }

  async loginAsUser() {
    await api.post('/api/anotheruserlogin', { username: this.username })
        .then(response => {
          location.replace('/');
        })
        .catch(error => {
          this.notificationKind = 'error';
          this.notificationText = `Что-то пошло не так: ${error.message}`;
          this.showNotification = true;
        })
  }

  async logoutFromUser() {
    await api.get('/api/anotheruserlogout')
        .then(response => {
          location.replace('/');
        })
  }
}
</script>

<style scoped lang="stylus">

.content_container
  display inline-flex

.content_btn
  margin-left 10px

</style>
