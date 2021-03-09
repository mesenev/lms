<template>
  <div>
    <cv-button class="change-pass-btn" kind="ghost" @click="showModal">
      Сменить пароль
    </cv-button>
    <cv-modal
      :visible="modalVisible"
      size="small"
      class="add_cats_modal"
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
        <div>
          <cv-text-input class="old-pass"
                         type="password"
                         label="Введите старый пароль:"
                         v-model.trim="old_pass"
          >
          </cv-text-input>
          <cv-text-input class="new-pass"
                         type="password"
                         label="Введите новый пароль:"
                         v-model.trim="new_pass">
            <template v-if="!checkNewPassword"
                      slot="invalid-message">
              Длина пароля должна быть от 8 до 25
            </template>
          </cv-text-input>
          <cv-text-input class="new-pass-repeat"
                         type="password"
                         label="Введите новый пароль ещё раз:"
                         v-model.trim="new_pass_repeat">
            <template v-if="!checkRepeatPassword"
                      slot="invalid-message"
            >
              Пароли должны совпадать
            </template>
          </cv-text-input>
          <br>
          <cv-button class="btn"
                     :disabled="!correctPassword"
                     @click="Finished"
          >
            Изменить
          </cv-button>
        </div>
      </template>
    </cv-modal>
  </div>

</template>

<script lang="ts">

import axios from "axios";
import { Component, Vue } from 'vue-property-decorator';


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

  get checkNewPassword(): boolean {
    if (this.new_pass.length === 0) return true;
    return this.new_pass.length >= 8 && this.new_pass.length <= 20;
  }

  get checkRepeatPassword(): boolean {
    if (this.new_pass_repeat.length === 0) return true;
    return this.new_pass === this.new_pass_repeat;
  }

  async Finished() {
    const data = { old_password: this.old_pass, new_password: this.new_pass };
    const request = axios.post('/api/change-password/', data);
    request.then(response => {
      this.notificationKind = 'success';
      this.notificationText = "Пароль успешно сменён!";
      this.showNotification = true;
      setTimeout(this.modalHidden, 2000);
    }).catch(error => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    })

  }

  get correctPassword() {
    return (
      !!this.new_pass_repeat && !!this.new_pass && !!this.old_pass
      && this.checkNewPassword && this.checkRepeatPassword
    );
  }

  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
    this.notificationText = '';
    this.showNotification = false;
    this.notificationKind = 'success';
    this.old_pass = this.new_pass = this.new_pass_repeat = '';
  }
}
</script>

<style scoped lang="stylus">
  .add_cats_modal /deep/ .bx--modal-container
    height 50%

  .new-pass, .new-pass-repeat
    & /deep/ .bx--text-input__field-wrapper .bx--text-input__invalid-icon
      transform: translateY(-50%) translateX(-20px)

  .add_cats_modal /deep/ .cv-text-input.bx--form-item:not(:first-child)
    margin-top 1rem
</style>
