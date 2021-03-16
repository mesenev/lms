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
        <cv-structured-list>
          <template slot="headings">
            <cv-structured-list-heading>Выбор</cv-structured-list-heading>
            <cv-structured-list-heading>ФИО преподавателя</cv-structured-list-heading>
          </template>
          <template slot="items">
            <cv-structured-list-item v-for="k in teachersArray" :key="k.id" checked>
              <cv-structured-list-data>
                <cv-checkbox
                  value="selectedNew"
                  v-on:click="actionSelected(k)">
                </cv-checkbox>
              </cv-structured-list-data>
              <cv-structured-list-data>{{ k.first_name }} {{ k.last_name }}</cv-structured-list-data>
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

import { Component } from 'vue-property-decorator';

@Component({})
export default class AddTeacherModal extends NotificationMixinComponent {

  fetchingLessons = true;
  selectedNew = false;
  userStore = userStore;
  creationLoader = false;
  teachersArray: UserModel[] = [];
  pickedTeachers: UserModel[] = [];
  modalVisible = false;

  created() {
    if (this.userStore.user.staff_for.length != 0) {
      this.teachersArray.push(this.userStore.user);
    }
  }

  appendTeachers(teacher: UserModel) {
    this.pickedTeachers.push(teacher);
    console.log(this.pickedTeachers)
  }

  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
  }

  actionSelected(user: UserModel) {
    this.selectedNew = !this.selectedNew;
    if (this.selectedNew) {
      this.pickedTeachers.push(user);
    } else {
      this.pickedTeachers = this.pickedTeachers.filter((x: UserModel) => x.id != user.id)
    }
  }
}
</script>

<style lang="stylus" scoped>
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
