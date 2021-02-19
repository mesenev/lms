<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить урок
    </cv-button>
    <cv-modal size="default"
              class="add_lesson_modal"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              :primary-button-disabled="!lessons.length && !currentLesson.name"
              @primary-click="addLesson"
              @secondary-click="() => {}">
      <template slot="label">{{ course.name }}</template>
      <cv-inline-notification
        v-if="showNotification"
        @close="notificationKind"
        kind="error"
        :sub-title="notificationText"
      />
      <template slot="title">
        Добавить урок
        <cv-content-switcher class="switcher" @selected="actionSelected">
          <cv-content-switcher-button content-selector=".content-1" selected>
            Создать новый
          </cv-content-switcher-button>
          <cv-content-switcher-button content-selector=".content-2">
            Выбрать из существующих
          </cv-content-switcher-button>
        </cv-content-switcher>
      </template>
      <template slot="content">
        <section class="modal--content">
          <div class="content-1">
            <cv-text-input label="Название курса" v-model.trim="course.name" disabled/>
            <cv-text-input label="Автор" v-model.trim="course.author.username" disabled/>
            <cv-text-input label="Название урока" v-model.trim="currentLesson.name"/>
            <cv-text-input label="Описание урока" v-model.trim="currentLesson.description"/>
            <span>Добавление к уроку материалов и задач доступно после создания урока</span>
          </div>
          <div class="content-2" hidden>
            <div>
              <cv-structured-list>
                <template slot="items">
                  <cv-search v-model="searchQueryForAllLessons"></cv-search>
                  <cv-structured-list-item
                    class="lesson-card"
                    v-for="lesson in allLessons"
                    :key="lesson.id">
                    <LessonCard
                      :lesson="lesson"
                      :main-icon="AddAlt32"
                      :change-main-icon="SubtractAlt32"
                      :manipulation="chooseLesson">
                    </LessonCard>
                  </cv-structured-list-item>
                </template>
              </cv-structured-list>
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

<!-- TODO: get counts from num-input -->

<script lang="ts">

import searchByLessons from '@/common/searchByTutorial';
import NotificationMixinComponent from '@/components/common/NotificationMixinComponent.vue';
import LessonCard from '@/components/EditCourse/LessonCard.vue';
import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import courseStore from '@/store/modules/course';
import lessonStore from '@/store/modules/lesson';
import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';
import axios from 'axios';

import { Component, Prop } from 'vue-property-decorator';

@Component({ components: { LessonCard, AddAlt20, SubtractAlt20 } })
export default class EditCourseModal extends NotificationMixinComponent {
  @Prop({ required: true }) course!: CourseModel;

  AddAlt32 = AddAlt20;
  SubtractAlt32 = SubtractAlt20;
  courseStore = courseStore;
  lessonStore = lessonStore;
  currentLesson: LessonModel = { ...this.lessonStore.getNewLesson, course: this.course.id };
  fetchingLessons = true;
  selectedNew = true;
  creationLoader = false;

  lessons: LessonModel[] = [];
  modalVisible = false;
  searchQueryForAllLessons = '';

  get allLessons(): LessonModel[] {
    return searchByLessons(this.searchQueryForAllLessons, this.freeLessons);
  }

  get freeLessons(): LessonModel[] {
    // TODO: fix this
    return [];
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

  get getSelected(): string {
    return this.lessons.concat(this.currentLesson)
      .map((l) => l.name)
      .sort((a, b) => a < b ? -1 : 1)
      .join(' ');
  }

  chooseLesson(lesson: LessonModel) {
    if (!this.lessons.includes(lesson)) {
      this.lessons.push(lesson);
    } else {
      this.lessons = this.lessons.filter((l) => lesson !== l);
    }
  }

  async addLesson() {
    if (this.selectedNew) {
      this.creationLoader = true;
      await this.createNewLesson();
      this.creationLoader = false;
    }
    if (this.lessons.every((l) => l.name)) {
      // this.lessons.forEach((lesson) => this.lessonStore.addLessonToCourse(lesson));
      // this.lessons = [];
    }
  }


  async createNewLesson() {
    delete this.currentLesson.id;
    const request = axios.post('http://localhost:8000/api/lesson/', this.currentLesson);
    request.then(response => {
      this.course.lessons.push(response.data as LessonModel);
      this.modalHidden();
    });
    request.catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    });
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
