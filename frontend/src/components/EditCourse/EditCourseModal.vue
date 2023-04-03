<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить урок
    </cv-button>
    <cv-modal size="default"
              class="add_lesson_modal"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              :primary-button-disabled="primaryButtonDisabled"
              @primary-click="addLesson"
              @secondary-click="() => {}">
      <template slot="label">{{ course.name }}</template>
      <template slot="title">
        Добавить урок
        <cv-content-switcher class="switcher" @selected="actionSelected">
          <cv-content-switcher-button owner-id="create-lesson" selected>
            Создать новый
          </cv-content-switcher-button>
          <cv-content-switcher-button owner-id="select-lesson" :disabled="true">
            Выбрать из существующих
          </cv-content-switcher-button>
        </cv-content-switcher>
      </template>
      <template slot="content">
        <cv-inline-notification
          v-if="showNotification"
          :kind="notificationKind"
          @close="hideNotification"
          :sub-title="notificationText"
        />
        <section class="modal--content">
          <cv-content-switcher-content owner-id="create-lesson">
            <div class="content-1">
              <cv-text-input class="modal--content--input"
                             label="Название курса" v-model.trim="course.name" disabled/>
              <cv-text-input class="modal--content--input"
                             label="Автор" v-model.trim="authorUsername" disabled/>
              <cv-text-input class="modal--content--input"
                             label="Название урока" v-model.trim="currentLesson.name">
                <template slot="invalid-message" v-if="showInvalidMessage && !currentLesson.name">
                  {{ emptyInputInvalidText }}
                </template>
              </cv-text-input>
              <cv-text-input class="modal--content--input"
                             label="Описание урока" v-model.trim="currentLesson.description"/>
              <span style="text-decoration-line: underline">
              Добавление к уроку материалов и задач доступно после создания урока.
            </span>
            </div>
          </cv-content-switcher-content>
          <cv-content-switcher-content owner-id="select-lesson">
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
          </cv-content-switcher-content>
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
import api from '@/store/services/api'
import { Component, Prop, Watch } from 'vue-property-decorator';

@Component({ components: { LessonCard, AddAlt20, SubtractAlt20 } })
export default class EditCourseModal extends NotificationMixinComponent {
  @Prop({ required: true }) courseId!: number;

  AddAlt32 = AddAlt20;
  SubtractAlt32 = SubtractAlt20;
  courseStore = courseStore;
  lessonStore = lessonStore;
  currentLesson: LessonModel = { ...this.lessonStore.getNewLesson, course: this.courseId };
  fetchingLessons = true;
  selectedNew = true;
  creationLoader = false;

  lessons: LessonModel[] = [];
  modalVisible = false;
  searchQueryForAllLessons = '';
  showInvalidMessage = false;
  emptyInputInvalidText = 'Заполните поле!';

  get primaryButtonDisabled(): boolean {
    return !this.lessons.length && this.creationLoader;
  }

  get course() {
    return this.courseStore.currentCourse || this.courseStore.newCourse;
  }

  get allLessons(): LessonModel[] {
    return searchByLessons(this.searchQueryForAllLessons, this.freeLessons);
  }

  get freeLessons(): LessonModel[] {
    // TODO: fix this
    return [];
  }

  get authorUsername() {
    return this.course.author?.username as string;
  }

  async created() {
    //
  }

  showModal() {
    this.modalVisible = true;
    this.showNotification = false;
    this.currentLesson = { ...this.lessonStore.getNewLesson, course: this.courseId };
    this.creationLoader = false;
  }

  modalHidden() {
    this.modalVisible = false;
  }

  actionSelected(value: string) {
    this.selectedNew = value === 'create-lesson';
  }

  get getSelected(): string {
    return this.lessons.concat(this.currentLesson)
      .map((l) => l.name)
      .sort((a, b) => a < b ? -1 : 1)
      .join(' ');
  }

  chooseLesson(lesson: LessonModel) {
    //
  }

  async addLesson() {
    if (this.selectedNew) {
      this.checkCorrectFields();
      if (this.showInvalidMessage)
        return;
      this.creationLoader = true;
      await this.createNewLesson();
    }
  }

  checkCorrectFields() {
    this.showInvalidMessage = !this.currentLesson.name;
  }

  async createNewLesson() {
    await api.post('/api/lesson/', this.currentLesson)
      .then(response => {
        const course = this.courseStore.currentCourse as CourseModel;
        course.lessons.push(response.data as LessonModel);
        this.lessonStore.setLessons({ [course.id]: course.lessons });
        this.modalHidden();
      })
      .catch(error => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так: ${error.message}`;
        this.showNotification = true;
      })
      .finally(() => {
        this.creationLoader = false;
      })
  }
}
</script>

<style scoped lang="stylus">
/deep/ .bx--modal-content:focus
  outline none

.lesson_list
  margin-bottom 0

.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)

.switcher
  margin-bottom: 5px

.modal--content--input
  margin-bottom 1rem

/deep/ .bx--modal-content
  margin-bottom 0

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
