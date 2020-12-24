<template>
  <div>
    <cv-structured-list class="lesson__list" v-if="course.lessons.length">
      <template slot="headings">
        <cv-structured-list-heading>
          <h4>Уроки</h4>
        </cv-structured-list-heading>
      </template>
      <template slot="items">
        <cv-search label="Поиск"
                   v-model="searchQueryForCourseLessons">
        </cv-search>
        <cv-structured-list-item class="lesson-card"
                                 v-for="(lesson, id) in courseLessons"
                                 :key="id">
          <LessonCard :lesson="lesson"
                      :icon="TrashCan32"
                      :second-icon="Settings32"
                      :manipulation="deleteLesson">
          </LessonCard>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
    <cv-button class="change__btn" @click="showModal">
      Добавить урок
    </cv-button>
    <cv-modal size="default"
              class="add_lesson_modal"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              :primary-button-disabled="!arrayOfLessons.length && !currentLesson.name"
              @primary-click="addLesson"
              @secondary-click="() => {}">
      <template slot="label">{{ course.name }}</template>
      <template slot="title">
        Добавить урок
        <cv-content-switcher class="switcher" @selected="currentLesson = emptyLesson">
          <cv-content-switcher-button content-selector=".content-1"
                                      selected>
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
                    <cv-structured-list-item class="lesson-card"
                                           v-for="(lesson, id) in allLessons"
                                           :key="id">
                      <LessonCard :lesson="lesson"
                                  :icon="AddAlt32"
                                  :on-click-icon="SubtractAlt32"
                                  :manipulation="chooseLesson">
                      </LessonCard>
                    </cv-structured-list-item>
                </template>
              </cv-structured-list>
            </div>
          </div>
          <div class="content-2" hidden>
            <cv-text-input label="Название урока"
                           v-model.trim="currentLesson.name">
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
import {Component, Prop, Vue} from 'vue-property-decorator';
import { mainStore } from '@/store';
import LessonModel from '@/models/LessonModel';
import CourseModel from '@/models/CourseModel';
import LessonCard from '@/components/courseEdit/LessonCard.vue';
import { TrashCan32, AddAlt32, Settings32, SubtractAlt32 } from '@carbon/icons-vue/es/index';

@Component({components: {
  LessonCard,
  TrashCan32,
  AddAlt32,
  Settings32,
  SubtractAlt32,
}})
export default class EditCourseLessons extends Vue {
  @Prop({ required: true }) course!: CourseModel;

  TrashCan32 = TrashCan32;

  AddAlt32 = AddAlt32;

  SubtractAlt32 = SubtractAlt32;

  Settings32 = Settings32;

  modalVisible = false;

  showModal(): void {
    this.modalVisible = true;
  }

  modalHidden(): void {
    this.modalVisible = false;
    this.currentLesson = this.emptyLesson;
  }

  store = mainStore;

  get freeLessons() {
    return this.store.getAllLessons.filter((l) => {
      return !this.course.lessons.map((courseLesson) => courseLesson.id).includes(l.id);
    });
  }

  search(query: string, arrayOfLessons: LessonModel[]): LessonModel[] {
    // if there is no query
    if (!query) {
      return arrayOfLessons;
    }
    // if there is
    return arrayOfLessons.filter((lesson) => {
      return lesson.name.toLowerCase().includes(query.toLowerCase())
    });
  }

  searchQueryForAllLessons = '';

  searchQueryForCourseLessons = '';

  get allLessons(): LessonModel[] {
    return this.search(this.searchQueryForAllLessons, this.freeLessons);
  }

  get courseLessons(): LessonModel[] {
    return this.search(this.searchQueryForCourseLessons, this.course.lessons);
  }

  get getSelected(): string {
    return this.arrayOfLessons.concat(this.currentLesson)
      .map((l) => l.name)
      .sort((a, b) => a < b ? -1 : 1)
      .join(' ');
  }

  get emptyLesson(): LessonModel {
    return {
      id: this.store.getNextLessonId,
      name: '',
      lessonContent: '',
      classwork: [],
      homework: [],
      deadline: '',
    } as LessonModel;
  }

  currentLesson: LessonModel = this.emptyLesson;

  arrayOfLessons: LessonModel[] = [];

  chooseLesson(lesson: LessonModel) {
    if (!this.arrayOfLessons.includes(lesson)) {
      this.arrayOfLessons.push(lesson);
    } else {
      this.arrayOfLessons = this.arrayOfLessons.filter((l) => lesson !== l);
    }
  }

  addLesson() {
    if (this.currentLesson.name) {
      this.arrayOfLessons.push(this.currentLesson);
      this.store.addLessonToAllLesson(this.currentLesson);
    }
    if (this.arrayOfLessons.every((l) => l.name)) {
      this.arrayOfLessons.forEach((lesson) => this.store.addLessonToCourse(lesson));
      this.arrayOfLessons = [];
    }
    this.modalHidden();
  }

  deleteLesson(lesson: LessonModel) {
    this.store.deleteLesson(lesson);
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

  .add_lesson_modal .bx--btn
    height 3.5rem
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
