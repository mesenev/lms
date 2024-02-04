<template>
  <div>
    <cv-button
        kind="tertiary"
        @click="showModal"
        :icon="Edit32"
    >Изменить
    </cv-button>
    <cv-modal class="add_lesson_modal"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              :primary-button-disabled="!avatarChanged"
              @primary-click="changeAvatar">
      <template v-slot:title>
        Изменить фото профиля
      </template>
      <template v-slot:content>
        <div class="bx--col-lg-4, content">
          <cv-inline-notification
              v-if="showNotification"
              :kind="notificationKind"
              :sub-title="notificationText"
              @close="() => showNotification=false"
          />
          <input type="file" accept="image/*" @change="Upload($event)"/>
          <label>Предварительный просмотр</label>
          <img :src="imagePreview?.toString()" v-show="showPreview" alt="avatar" class="preview"/>
        </div>
      </template>
      <template v-slot:primary-button>
        Добавить
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts" setup>

import type {UserModel} from "@/models/UserModel";
import Edit32 from '@carbon/icons-vue/es/edit/32';
import api from '@/stores/services/api'
import {ref} from "vue";
import type { PropType } from 'vue';
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";

const {notificationText, notificationKind, showNotification, hideNotification} = useNotificationMixin();

const props = defineProps({
  user: {type: Object as PropType<UserModel>, required: true}
});
const emits = defineEmits(['update-user']);
const imagePreview = ref<String | null | ArrayBuffer>('');
const showPreview = ref(false);
const avatarChanged = ref(false);
const modalVisible = ref(false);
const file = ref(new Blob());

function showModal() {
  modalVisible.value = true;
}

function modalHidden() {
  modalVisible.value = false;
  avatarChanged.value = false;
  showNotification.value = false;
  showPreview.value = false;
}

function changeAvatar() {
  const fd = new FormData();
  fd.append('avatar_url', file.value);
  api.post('/api/change-avatar/', fd, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
      .then(response => {
        notificationKind.value = 'success';
        notificationText.value = "Фото профиля успешно изменено!";
        showNotification.value = true;
        emits('update-user', {...props.user, avatar_url: response.data.message});
        setTimeout(modalHidden, 2000);
      })
      .catch(error => {
        notificationKind.value = 'error';
        notificationText.value = `Что-то пошло не так: ${error.message}`;
        showNotification.value = true;
      })
  return;
}

function Upload(event: Event) {
  const inputElement = event.target as HTMLInputElement;
  if (inputElement.files !== null) {
    const fileList = inputElement.files;
    file.value = fileList[0];
    const reader = new FileReader();
    reader.addEventListener("load", () => {
      showPreview.value = true;
      imagePreview.value = reader.result;
    })
    if (file.value) {
      reader.readAsDataURL(file.value);
      avatarChanged.value = true;
    }
  }

  const reader = new FileReader();
  reader.addEventListener("load", () => {
    showPreview.value = true;
    imagePreview.value = reader.result;
  })
  if (file.value) {
    reader.readAsDataURL(file.value);
    avatarChanged.value = true;
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
  object-fit: cover;
}

.btns {
  float left;
  cursor: pointer;
  clear: both;
  display flex;
  flex-direction row;
}
</style>
