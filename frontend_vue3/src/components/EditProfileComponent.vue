<template>
  <div class="info-block">
    <div class="info">
      <h3>Редактирование</h3>
    </div>
    <div class="list">
      <cv-inline-notification
        v-if="showNotification"
        :kind="notificationKind"
        :sub-title="notificationText"
        @close="hideNotification"
      />
      <cv-structured-list>
        <template v-slot:items>
          <cv-structured-list-item class="list-item">
            <cv-structured-list-data>Имя</cv-structured-list-data>
            <cv-structured-list-data>
              <cv-text-input v-model.trim="curUser.first_name"/>
            </cv-structured-list-data>
          </cv-structured-list-item>
          <cv-structured-list-item class="list-item">
            <cv-structured-list-data>Фамилия</cv-structured-list-data>
            <cv-structured-list-data>
              <cv-text-input v-model.trim="curUser.last_name"/>
            </cv-structured-list-data>
          </cv-structured-list-item>
          <cv-structured-list-item class="list-item">
            <cv-structured-list-data>Логин</cv-structured-list-data>
            <cv-structured-list-data>
              <cv-text-input v-model.trim="curUser.username">
                <template
                  v-if="checkUsername"
                  v-slot:invalid-message>
                  Логин должен содержать от 4 до 10 символов
                  и может состоять из латинских букв и цифр
                </template>
              </cv-text-input>
            </cv-structured-list-data>
          </cv-structured-list-item>
          <cv-structured-list-item class="list-item">
            <cv-structured-list-data>Учебная группа</cv-structured-list-data>
            <cv-structured-list-data>
              <cv-combo-box
                :options="studyGroups"
                :auto-filter="true"
                label="Выберите группу"
                v-model="curUser.study_group"/>
            </cv-structured-list-data>
          </cv-structured-list-item>
          <cv-structured-list-item class="list-item">
            <cv-structured-list-data>Почта</cv-structured-list-data>
            <cv-structured-list-data>
              <cv-text-input v-model.trim="curUser.email">
                <template v-if="checkEmail" v-slot:invalid-message>
                  Введите корректный Email
                </template>
              </cv-text-input>
            </cv-structured-list-data>
          </cv-structured-list-item>
        </template>
      </cv-structured-list>
    </div>
    <div class="info-btns">
      <cv-button :disabled="isDataValid" @click="editButtonHandler">Сохранить</cv-button>
      <cv-button kind="tertiary" @click="hideEdit">Назад</cv-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import type { PropType } from "vue";
import type { UserModel } from "@/models/UserModel";
import { computed, onMounted, ref } from "vue";
import api from "@/stores/services/api";
import _ from 'lodash';

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  user: { type: Object as PropType<UserModel>, required: true }
})

const emits = defineEmits(['updateUser', 'back'])

const curUser = ref<UserModel>(_.cloneDeep(props.user));

const isLoginValid = ref(false);
const isEmailValid = ref(false);

const studyGroups = ref<Array<any>>([]);

onMounted(async () => {
  // await fetch_study_groups();
  // studyGroups.value = studyGroups.value.map(item => {
  //   return {
  //     name: item.study_group,
  //     label: item.study_group,
  //     value: item.study_group,
  //   };
  // });
})

// async function fetch_study_groups() {
//   await api.get(`/api/studygroups/`)
//     .then(response => {
//       if (response.data)
//         studyGroups.value = response.data;
//     })
//     .catch(error => {
//       console.log(error);
//     })
// }

function setLoginValidStatus(status: boolean) {
  isLoginValid.value = status;
}

function setEmailValidStatus(status: boolean) {
  isEmailValid.value = status;
}

const isDataValid = computed((): boolean => {
  return isEmailValid.value || isLoginValid.value;
})

const checkUsername = computed((): boolean => {
  if (curUser.value.username) {
    const valid = !/^[a-zA-Z0-9]+$/.test(curUser.value.username)
    if (valid || (curUser.value.username.length < 4 || curUser.value.username.length > 10)) {
      setLoginValidStatus(true);
      return true;
    }
    setLoginValidStatus(false);
    return false;
  }
  return true;
})

const checkEmail = computed((): boolean => {
  if (curUser.value.email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    const valid = !re.test(curUser.value.email);
    if (valid) {
      setEmailValidStatus(true);
      return true;
    }
    setEmailValidStatus(false);
    return false;
  }
  setEmailValidStatus(true);
  return true;
})

async function editButtonHandler() {
  await api.patch(`/api/users/${curUser.value.id}/`, {
    first_name: curUser.value.first_name,
    last_name: curUser.value.last_name,
    study_group: curUser.value.study_group,
    username: curUser.value.username,
    email: curUser.value.email,
  })
    .then(response => {
      emits('updateUser', curUser.value);
      notificationKind.value = 'success';
      notificationText.value = "Профиль успешно изменен";
      showNotification.value = true;
    })
    .catch(error => {
      notificationKind.value = 'error';
      notificationText.value = `Что-то пошло не так: ${error.message}`;
      showNotification.value = true;
    })
}

function hideEdit() {
  emits('back');
}

</script>

<style scoped lang="stylus">
:deep() .bx--text-input,
:deep() .bx--combo-box
  background-color var(--cds-ui-background)

.list
  margin-top 2rem
  padding-bottom 0
  margin-bottom 0

.info-btns
  margin-top 0
  display flex
  flex-direction row
  justify-content space-between

.info
  margin-bottom 20px
  display flex
  flex-direction row
  justify-content space-between
  color var(--cds-text-01)

.list-item
  display flex
  align-items center
  justify-content space-between

</style>
