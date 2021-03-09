<template>
  <div>
    <Edit32 class="change-btn" @click="showModal"/>
    <cv-modal size="default"
              class="add_lesson_modal"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              :primary-button-disabled="!avatarChanged"
              @primary-click="changeAvatar">
      <template slot="title">
        Изменить фото профиля
      </template>
      <template slot="content">
        <div class="bx--col-lg-4, content">
          <cv-inline-notification
          v-if="showNotification"
          :kind="notificationKind"
          :sub-title="notificationText"
          @close="() => showNotification=false"
          />
          <input type="file" ref="file" :v-model="file" accept="image/*" v-on:change="Upload($event.target.files)"/>
          <label>Предварительный просмотр</label>
          <img v-bind:src="imagePreview" v-show="showPreview" alt="картинка" class="preview"/>
        </div>
      </template>
      <template slot="primary-button">
        Добавить
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">

import UserModel from "@/models/UserModel";
import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import Edit32 from '@carbon/icons-vue/es/edit/32';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';
import axios from "axios";
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { AddAlt20, SubtractAlt20, Edit32 } })
export default class EditAvatarModal extends Vue {
  @Prop() user!: UserModel;
  imagePreview: string | null | ArrayBuffer = '';
  showPreview = false;
  AddAlt32 = AddAlt20;
  SubtractAlt32 = SubtractAlt20;
  avatarChanged = false;
  modalVisible = false;
  showNotification = false;
  notificationText = '';
  notificationKind = 'success';
  file = new Blob();

  showModal() {
    this.modalVisible = true;

  }

  modalHidden() {
    this.modalVisible = false;
    this.avatarChanged = false;
    this.showNotification = false;
    this.showPreview = false;
  }

  changeAvatar() {
    const fd = new FormData();
    fd.append('avatar_url',this.file );
    const request = axios.post('/api/change-avatar/', fd);
    request.then(response => {
      this.notificationKind = 'success';
      this.notificationText = "Фото профиля успешно изменено!";
      this.showNotification = true;
      this.user.avatar_url = response.data.message;
      setTimeout(this.modalHidden, 2000);
    }).catch(error => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;

    })
    return;
  }

  Upload(fileList: never) {
    this.file = fileList[0] ;
    const reader = new FileReader();
    reader.addEventListener("load", () => {
      this.showPreview = true;
      this.imagePreview = reader.result;
    })
    if (this.file) {
      reader.readAsDataURL(this.file);
      this.avatarChanged = true;
    }
  }
}
</script>

<style scoped lang="stylus">
.bx--modal-content:focus
  outline none

.content {
  padding-left: 100px;
}

.lesson_list
  margin-bottom 0

.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)

.switcher
  margin-bottom: 5px

.add_lesson_modal .bx--modal-container
  height 75vh

.add_lesson_modal .bx--modal-footer
  height 3.5rem

.add_lesson_modal .bx--btn
  height 3rem
  border none

.add_lesson_modal .bx--btn--secondary
  background-color var(--cds-hover-secondary)

  &:hover, &:active, &:focus
    outline none
    box-shadow none
    border none

.add_lesson_modal .bx--btn--primary[disabled = disabled],
.add_lesson_modal .bx--btn--primary
  background-color var(--cds-ui-05)

.modal--content
  height 400px

.file-upload {
  width 650px;
  padding-right 20px;
}

.btn {

 }

.preview {
  padding-top: 50px;
  width: 250px;
  height: 250px;
  object-fit:cover;
}

.btns {
  float left;
  cursor: pointer;
  clear: both;
  display flex;
  flex-direction row;
}
</style>
