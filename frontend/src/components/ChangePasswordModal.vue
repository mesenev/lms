<template>
  <div>
    <cv-button class="change-pass-btn" kind="tertiary" @click="showModal">
      Сменить пароль
    </cv-button>
    <cv-modal
        :visible="modalVisible"
        size="small"
        class="add_cats_modal"
        @modal-hidden="modalHidden">
      <template v-slot:title>
        Смена пароля
      </template>
      <template v-slot:content>
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
                      v-slot:invalid-message>
              Длина пароля должна быть от 8 до 25
            </template>
          </cv-text-input>
          <cv-text-input class="new-pass-repeat"
                         type="password"
                         label="Введите новый пароль ещё раз:"
                         v-model.trim="new_pass_repeat">
            <template v-if="!checkRepeatPassword"
                      v-slot:invalid-message
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

<script lang="ts" setup>

import api from '@/stores/services/api'
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import {computed, ref} from "vue";


const {notificationText, notificationKind, showNotification, hideNotification} = useNotificationMixin();
const modalVisible = ref(false);
const old_pass = ref('');
const new_pass = ref('');
const new_pass_repeat = ref('');

//TODO: code below is not working
const checkOldPassword = computed(() => {
  return false;
})

const checkNewPassword = computed(() => {
  if (new_pass.value.length === 0) return true;
  return new_pass.value.length >= 8 && new_pass.value.length <= 20;
})

const checkRepeatPassword = computed(() => {
  if (new_pass_repeat.value.length === 0) return true;
  return new_pass.value === new_pass_repeat.value;
})

async function Finished() {
  const data = {old_password: old_pass.value, new_password: new_pass.value};
  const request = api.post('/api/change-password/', data);
  request.then(response => {
    notificationKind.value = 'success';
    notificationText.value = "Пароль успешно сменён!";
    showNotification.value = true;
    setTimeout(modalHidden, 2000);
  }).catch(error => {
    notificationKind.value = 'error';
    notificationText.value = `Что-то пошло не так: ${error.message}`;
    showNotification.value = true;
  })

}

const correctPassword = computed(() => {
  return (
      !!new_pass_repeat.value && !!new_pass.value && !!old_pass.value
      && checkNewPassword.value && checkRepeatPassword.value
  );
})

function showModal() {
  modalVisible.value = true;
}

function modalHidden() {
  modalVisible.value = false;
  notificationText.value = '';
  showNotification.value = false;
  notificationKind.value = 'success';
  old_pass.value = new_pass.value = new_pass_repeat.value = '';
}
</script>

<style scoped lang="stylus">
.add_cats_modal :deep(.bx--modal-container) {
  height 50%
}

.new-pass, .new-pass-repeat
  & :deep(.bx--text-input__field-wrapper .bx--text-input__invalid-icon) {
    transform: translateY(-50%) translateX(-20px)
  }
    
.add_cats_modal :deep(.cv-text-input.bx--form-item:not(:first-child)) {
  margin-top 1rem
}
</style>
