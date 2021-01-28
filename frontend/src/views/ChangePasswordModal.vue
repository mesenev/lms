<template>
  <div>
    <cv-button class="change-pass-btn" kind="ghost" @click="showModal">
      Сменить пароль
    </cv-button>
    <cv-modal
      :visible="modalVisible"
      class="add_cats_modal" size="xs"
      @modal-hidden="modalHidden">
      <template slot="title">
        Смена пароля
      </template>
      <template slot="content">
        <cv-inline-notification
          v-if="showNotification"
          :kind="notificationKind"
          :sub-title="notificationText"
          @close="() => showNotification=false"
        />
        <div class="bx--col-lg-12, content">
          <cv-text-input class="old-pass" label="Введите старый пароль:" v-model.trim="old_pass" password-hide-label="*">
            <template v-if="checkOldPassword" slot="invalid-message">
              Введён неверный пароль<p></p></template>
          </cv-text-input>
          <br>
          <cv-text-input class="new-pass" label="Введите новый пароль:" v-model.trim="new_pass" :password-visible="passw">
            <template v-if="checkNewPassword" slot="invalid-message">
              Длина пароля должна быть от 8 до 25<p></p></template>
          </cv-text-input>
          <br>
          <cv-text-input class="new-pass-repeat" label="Введите новый пароль ещё раз:" v-model.trim="new_pass_repeat">
            <template v-if="checkRepeatPassword" slot="invalid-message">
              Пароли должны совпадать
            </template>
          </cv-text-input>
          <br>
          <cv-button class="btn" @click="Finished"> Изменить</cv-button>
        </div>
      </template>
    </cv-modal>
  </div>

</template>

<script lang="ts">

import {Component, Vue} from 'vue-property-decorator';
import axios from "axios";
import user from "@/store/modules/user";


@Component({components: {}})

export default class ChangePasswordModal extends Vue {
  modalVisible = false;
  showNotification = false;
  notificationText = '';
  notificationKind = 'success';

  old_pass = '';
  new_pass = '';
  new_pass_repeat = '';

  //TODO: code below is not working
  get checkOldPassword() {
    return false;
  }

  get checkNewPassword() {
    if (this.new_pass) {
      return this.new_pass.length < 8 || this.new_pass.length > 20;
    }
    return false;
  }

  get checkRepeatPassword(): boolean {
    if (this.new_pass_repeat) {
      return this.new_pass !== this.new_pass_repeat;
    }
    return false;
  }

  async Finished() {
    const data =  {old_password: this.old_pass, new_password: this.new_pass};
    const request = axios.post('http://localhost:8000/api/change-password/', data);
    request.then(response => {
      this.notificationKind = 'success';
      this.notificationText = "Пароль успешно сменён!";
      this.showNotification = true;
    }).catch(error => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    })

  }


  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
  }
}
</script>

<style scoped lang="stylus">
.btns {
  float left;
  padding: 10px 24px;
  cursor: pointer;
  clear: both;
  display flex;
  flex-direction column;
}

.content {
  padding-left: 6px;
}

.input {
  width 650px;
  padding-right 20px;
}

.btn {
  margin-left: 130px;
}

</style>
