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
        <template slot="items" class>
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
                  slot="invalid-message">
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
          </cv-structured-list-item >
          <cv-structured-list-item class="list-item">
            <cv-structured-list-data>Почта</cv-structured-list-data>
            <cv-structured-list-data>
              <cv-text-input v-model.trim="curUser.email">
                <template v-if="checkEmail" slot="invalid-message">
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

<script lang="ts">

import UserModel from "@/models/UserModel";
import axios from "axios";
import {Component, Prop} from 'vue-property-decorator';
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";

@Component({ components: {} })
export default class EditProfileComponent extends NotificationMixinComponent {
  @Prop() user!: UserModel;

  curUser: UserModel = {...this.user};

  isLoginValid = false;
  isEmailValid = false;

  studyGroups = [] as Array<any>;

  async created() {
    await this.fetch_study_groups();
    this.studyGroups = this.studyGroups.map(item => {
      return {
        name: item.study_group,
        label: item.study_group,
        value: item.study_group,
      };
    });
  }

  async fetch_study_groups() {
    await axios.get(`/api/studygroups/`)
      .then(response => {
        if (response.data)
          this.studyGroups = response.data;
      })
      .catch(error => {
        console.log(error);
      })
  }

  get isDataValid(): boolean {
    return this.isEmailValid || this.isLoginValid;
  }

  get checkUsername(): boolean {
    if (this.curUser.username) {
      const valid = !/^[a-zA-Z0-9]+$/.test(this.curUser.username)
      if (valid || (this.curUser.username.length < 4 || this.curUser.username.length > 10)) {
        this.isLoginValid = true;
        return true;
      }
      this.isLoginValid = false;
      return false;
    }
    return true;
  }

  get checkEmail(): boolean {
    if (this.curUser.email) {
      const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      const valid = !re.test(this.curUser.email);
      if (valid) {
        this.isEmailValid = true;
        return true;
      }
      this.isEmailValid = false;
      return false;
    }
    this.isEmailValid = true;
    return true;
  }

  async editButtonHandler() {
    await axios.post('/api/edit-profile/', {
        first_name: this.curUser.first_name,
        last_name: this.curUser.last_name,
        study_group: this.curUser.study_group,
        username: this.curUser.username,
        email: this.curUser.email,
    })
      .then(response => {
        this.$emit('updateUser', this.curUser);
        this.notificationKind = 'success';
        this.notificationText = "Профиль успешно изменен";
        this.showNotification = true;
      })
      .catch(error => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так: ${error.message}`;
        this.showNotification = true;
      })
  }

  hideEdit() {
    this.$emit('back');
  }

}
</script>

<style scoped lang="stylus">

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

.list-item
  display flex
  align-items center
  justify-content space-between

</style>
