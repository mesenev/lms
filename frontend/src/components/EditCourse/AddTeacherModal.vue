<template>
  <div>
    <cv-button class="change-btn" kind="secondary" @click="showModal">
      Перейти к выбору преподавателей
    </cv-button>
    <cv-modal :visible="modalVisible"
              class="add_lesson_modal"
              size="default"
              @modal-hidden="modalHidden"
              @secondary-click="() => {}">
      <template slot="title">
        <h3>Выбор преподавателей</h3>
      </template>
      <template slot="content">
        <cv-inline-notification
          v-if="showNotification"
          :kind="notificationKind"
          :sub-title="notificationText"
          @close="hideNotification"
        />
        <cv-structured-list>
          <template slot="headings">
            <cv-structured-list-heading>
              <cv-search
                label="label"
                placeholder="Введите почту прeподавателя"
                v-model.trim="searchValue"/>
            </cv-structured-list-heading>
            <cv-structured-list-heading>
              <div class="list-headings">
                <cv-button
                  class="heading-btn"
                  :disabled="teacherNotPicked"
                  @click="addStuff()">
                  Добавить
                </cv-button>
              </div>
            </cv-structured-list-heading>
          </template>
          <template slot="items">
            <cv-structured-list-item v-for="k in teachersArray" :key="k.id" checked>
              <cv-structured-list-data>
                {{k.first_name + " " + k.last_name}}
              </cv-structured-list-data>
              <cv-structured-list-data>
                <cv-checkbox
                  class="list-checkbox"
                  value="value"
                  @click="actionSelected(k)">
                </cv-checkbox>
              </cv-structured-list-data>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">

import NotificationMixinComponent from '@/components/common/NotificationMixinComponent.vue';
import UserModel from "@/models/UserModel";
import userStore from '@/store/modules/user';

import {Component, Prop, Watch} from 'vue-property-decorator';
import axios from "axios";

@Component({})
export default class AddTeacherModal extends NotificationMixinComponent {
  @Prop({required: true}) courseId!: number;
  searchValue = "";
  @Watch('searchValue')
  async onSearchBarChange(val: string) {
    if (val.length >= 4) {
      await axios.get(
        `/api/teachersbymail/${this.courseId}/${this.searchValue}/`
      ).then(response => {
        if (response.data == "No match found :("){
          this.teachersArray = [];
        } else {
          this.teachersArray = response.data;
        }
        this.pickedTeachers.clear();
        this.teacherNotPicked = true;
        },
      ).catch(error => {
        console.log(error);
      })
    }
    else if (val.length === 0) {
      this.teachersArray = [];
      this.pickedTeachers.clear();
      this.teacherNotPicked = true;
    }
  };
  userStore = userStore;
  teachersArray: UserModel[] = [];
  pickedTeachers: Set<UserModel> = new Set<UserModel>();
  modalVisible = false;
  teacherNotPicked = true;

  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
  }

  isAnyTeacherPicked() {
    this.teacherNotPicked = this.pickedTeachers.size <= 0;
  }

  setNotificationText() {
    if (this.pickedTeachers.size > 1) {
      this.notificationText = "Преподаватели успешно добавлены"
    }
    else {
      this.notificationText = "Преподаватель успешно добавлен"
    }
  }

  getPickedTeachers(): Array<UserModel> {
    const curPickedTeachers: Array<UserModel> = []
    for (const elem of this.pickedTeachers) {
      curPickedTeachers.push(elem);
    }
    return curPickedTeachers;
  }

  addStuff() {
    axios.post(`/api/assignteacher/${this.courseId}/`, this.getPickedTeachers())
      .then(response => {
        this.notificationKind = 'success';
        this.setNotificationText();
        this.showNotification = true;
        this.onSearchBarChange(this.searchValue);
        this.pickedTeachers.clear();
        this.isAnyTeacherPicked();
      })
      .catch(error => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так: ${error.message}`;
        this.showNotification = true;
      });
  }

  actionSelected(user: UserModel) {
    if (this.pickedTeachers.has(user)) {
      this.pickedTeachers.delete(user);
    }
    else {
      this.pickedTeachers.add(user);
    }
    this.isAnyTeacherPicked();
  }
}
</script>

<style lang="stylus" scoped>
.list-headings
  display flex
  flex-direction column
  align-items stretch

.list-checkbox
  display flex
  flex-direction row
  justify-content center

.heading-btn
  padding 5px
  display flex
  justify-content center

.bx--modal-content:focus
  outline none

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
  height 500px
</style>
