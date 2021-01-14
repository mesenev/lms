<template>
  <!--              :primary-button-disabled="!lessons.length && !currentLesson.name"
              @primary-click="addLesson"-->
  <!-- TODO: button disable + pick a person => to a list of course view -->
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить пользователя в курс
    </cv-button>
    <cv-modal size="default"
              class="addUser"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              @secondary-click="() => {}">
      <template slot="label">{{ course.name }}</template>
      <cv-inline-notification
        v-if="showNotification"
        @close="() => showNotification=false"
        kind="error"
        :sub-title="notificationText"
      />
      <template slot="title">
        <h3>Добавить пользователя</h3>
        <cv-content-switcher class="switcher" @selected="actionSelected">
          <cv-content-switcher-button content-selector=".content-1" selected>
            Добавить ученика
          </cv-content-switcher-button>
          <cv-content-switcher-button content-selector=".content-2">
            Добавить преподавателя
          </cv-content-switcher-button>
        </cv-content-switcher>
      </template>
      <template slot="content">
        <section class="modal--content">
          <div class="content-1">
            <cv-data-table :columns="columns" :data="students"></cv-data-table>
          </div>
          <div class="content-2" hidden>
            <div>
                <cv-data-table :columns="columns" :data="admins"></cv-data-table>
            </div>
          </div>
        </section>
      </template>
      <template slot="primary-button">
        Добавить
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import UserModel from "@/models/UserModel";
import { lessonStore } from '@/store';

import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { } })
export default class EditCourseModal extends Vue {
  @Prop({ required: true }) course!: CourseModel;

  rowSize = ""
  title = "Table title"
  columns = [
    "id",
    "username",
    "name",
    "surname",
]

  users: Array<UserModel> = [
    {
      id: 1,
      username: 'mel',
      first_name: 'Дарья',
      last_name: 'Пахомова',
      staff_for: [],
    },
    {
      id: 2,
      username: 'oubre',
      first_name: 'Максим',
      last_name: 'Гринев',
      staff_for: [],
    },
    {
      id: 3,
      username: 'main',
      first_name: 'Владислав',
      last_name: 'Маингарт',
      staff_for: [],
    },
    {
      id: 4,
      username: 'tikhonov',
      first_name: 'Руслан',
      last_name: 'Тихонов',
      staff_for: [],
    },
    {
      id: 5,
      username: 'mesenev',
      first_name: 'Павел',
      last_name: 'Месенев',
      staff_for: [5],
    }
  ]
  lessonStore = lessonStore;
  currentLesson: LessonModel = { ...this.lessonStore.getNewLesson, course: this.course.id, };
  fetchingLessons = true;
  selectedNew = true;
  showNotification = false;
  notificationText = '';
  lessons: LessonModel[] = [];
  modalVisible = false;

  addedUsers: Array<UserModel> = [
    {
      id: 0,
      username: 'test',
      first_name: 'Тест',
      last_name: 'Тестович',
      staff_for: [6],
    }
  ];

  get students() {
    return this.users.filter(l => {
      if (!l.staff_for[0]) return l.username })
  }

  get admins() {
    console.log( this.users.filter(l => {
      if (l.staff_for[0]) return l.username }))
    return this.users.filter(l => {
      if (l.staff_for[0]) return l.username })
  }

  addUser(user: UserModel) {
    if (!this.addedUsers.includes(user)) {
      this.addedUsers.push(user);
    } else {
      this.addedUsers = this.addedUsers.filter((l) => user !== l);
    }
  }

  async created() {
    if (this.lessonStore.lessons.length === 0)
      await this.lessonStore.fetchLessons();
    this.fetchingLessons = false;
  }

  showModal() {
    this.modalVisible = true;
    this.showNotification = false;
    this.currentLesson = { ...this.lessonStore.getNewLesson, course: this.course.id };
  }

  modalHidden() {
    this.modalVisible = false;
  }

  actionSelected() {
    this.selectedNew = !this.selectedNew;
  }
}
</script>

<style scoped lang="stylus">
.bx--modal-content:focus
  outline none

.lesson_list
  margin-bottom 0

.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)

.switcher
  margin-bottom: 5px

.addUser .bx--modal-container
  height 75vh

.addUser .bx--modal-footer
  height 3.5rem

.addUser .bx--btn
  height 3rem
  border none

.addUser .bx--btn--secondary
  background-color var(--cds-hover-secondary)

  &:hover, &:active, &:focus
    outline none
    box-shadow none
    border none

.addUser .bx--btn--primary[disabled = disabled],
.addUser .bx--btn--primary
  background-color var(--cds-ui-05)

.modal--content
  height 500px
</style>
