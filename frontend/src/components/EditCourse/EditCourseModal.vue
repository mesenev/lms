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
      <template slot="title">
        Добавить урок
        <cv-content-switcher class="switcher" @selected="currentLesson = emptyLesson">
          <cv-content-switcher-button content-selector=".content-1" selected>
            Выбрать из существующих
          </cv-content-switcher-button>
          <cv-content-switcher-button content-selector=".content-2">
            Создать новый
          </cv-content-switcher-button>
        </cv-content-switcher>
      </template>
      <template slot="content">
        <section>
          <div class="content-1">
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
          <div class="content-2" hidden>
            <cv-text-input label="Название урока" v-model.trim="currentLesson.name">
            </cv-text-input>
            <cv-date-picker kind="single"
                            date-label="Время окончания"
                            v-model="currentLesson.deadline">
            </cv-date-picker>
            <cv-text-input label="Рабочие материалы"
                           v-model.trim="currentLesson.lessonContent">
            </cv-text-input>
          </div>
        </section>
      </template>
      <template slot="primary-button">
        Добавить
      </template>
      <template slot="secondary-button">
        {{ getSelected }}
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import searchByLessons from '@/common/searchByLessons';
import LessonCard from '@/components/EditCourse/LessonCard.vue';
import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import { courseStore, lessonStore } from '@/store';
import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';

import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { LessonCard, AddAlt20, SubtractAlt20 } })
export default class EditCourseModal extends Vue {
  @Prop({ required: true }) course!: CourseModel;

  AddAlt32 = AddAlt20;
  SubtractAlt32 = SubtractAlt20;
  courseStore = courseStore;
  lessonStore = lessonStore;
  currentLesson: LessonModel = this.emptyLesson;

  lessons: LessonModel[] = [];
  modalVisible = false;
  searchQueryForAllLessons = '';

  get allLessons(): LessonModel[] {
    return searchByLessons(this.searchQueryForAllLessons, this.freeLessons);
  }

  get freeLessons(): LessonModel[] {
    return this.lessonStore.lessons.filter((l) => {
      return !this.course.lessons.map((courseLesson) => courseLesson.id).includes(l.id);
    });
  }

  async created() {
    await this.lessonStore.fetchLessons();
  }

  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
    this.currentLesson = this.emptyLesson;
  }




  get getSelected(): string {
    return this.lessons.concat(this.currentLesson)
      .map((l) => l.name)
      .sort((a, b) => a < b ? -1 : 1)
      .join(' ');
  }

  get emptyLesson(): LessonModel {
    return {
      name: '',
      lessonContent: '',
      classwork: [],
      homework: [],
      materials: [],
      deadline: '',
    } as LessonModel;
  }


  chooseLesson(lesson: LessonModel) {
    if (!this.lessons.includes(lesson)) {
      this.lessons.push(lesson);
    } else {
      this.lessons = this.lessons.filter((l) => lesson !== l);
    }
  }

  addLesson() {
    if (this.currentLesson.name) {
      this.lessons.push(this.currentLesson);
      this.lessonStore.addLessonToAllLesson(this.currentLesson);
    }
    if (this.lessons.every((l) => l.name)) {
      this.lessons.forEach((lesson) => this.store.addLessonToCourse(lesson));
      this.lessons = [];
    }
    this.modalHidden();
  }
}
</script>

<style lang="stylus">
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

</style>
