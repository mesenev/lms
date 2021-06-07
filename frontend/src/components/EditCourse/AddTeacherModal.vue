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
            <cv-search
              label="label"
              placeholder="search"
              v-model.trim="searchValue"/>
          </template>
          <template slot="items">
            <cv-structured-list-item v-for="k in teachersArray" :key="k.id" checked>
              <cv-structured-list-data>
                <cv-checkbox
                  value="selectedNew"
                  v-on:click="actionSelected(k)">
                </cv-checkbox>
              </cv-structured-list-data>
              <cv-structured-list-data>{{k.username}} </cv-structured-list-data>
            </cv-structured-list-item>
            <cv-button
              disabled="True"
              v-if="pickedTeachers.length === 0">
                Подтвердить выбор
            </cv-button>
            <cv-button v-else
            v-on:click="addStuff()">
              Подтвердить выбор
            </cv-button>
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
    console.log(this.courseId)
    if (val.length >= 4) {
      await axios.get(
        `/api/teachersbymail/${this.courseId}/${this.searchValue}/`
      ).then(response => {
        if (response.data == "No match found :("){
        } else {
          this.teachersArray = response.data;
          console.log(this.teachersArray[0].staff_for)
        }
        },
      ).catch(error => {
        console.log(error);
      })
    }
  };
  selectedNew = false;
  userStore = userStore;
  teachersArray: UserModel[] = [];
  pickedTeachers: UserModel[] = [];
  modalVisible = false;


  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
  }

  addStuff() {
    axios.post(`/api/assignteacher/${this.courseId}/`, this.pickedTeachers)
      .then(response => {
        console.log(response.data)
      })
      .catch(error => {
        console.log(error);
      });
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
