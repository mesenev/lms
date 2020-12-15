<template>
  <div class="bx--grid">
    <cv-form-group>
      <template slot="content">
        <cv-form-item>
          <h4>Название курса</h4>
          <input :class="`bx--text-input`"
                 type="text"
                 v-model="courseTitle">
          <cv-button class="change__btn"
                     :disabled="canChangeCourseName"
                     @click="changeCourseName">
            Сменить название
          </cv-button>
        </cv-form-item>
        <cv-form-item>
          <h4>Описание курса</h4>
          <input :class="`bx--text-input`"
                 type="text"
                 v-model="courseDescription">
          <cv-button class="change__btn"
                     :disabled="canChangeCourseDescription"
                     @click="changeCourseDescription">
            Сменить описание
          </cv-button>
        </cv-form-item>
        <cv-form-item v-if="getLessons">
          <h4>Уроки</h4>
          <cv-structured-list>
            <template slot="items">
              <cv-structured-list-item v-for="(lesson, id) in getCourse.lessons" :key="id">
                <LessonCard :lesson="lesson"
                            :delete-lesson="deleteLesson">
                </LessonCard>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
          <!-- TODO Maingart is doing -->
          <cv-button class="change__btn">Добавить урок</cv-button>
        </cv-form-item>
      </template>
    </cv-form-group>
  </div>
</template>

<script lang="ts">
import {Prop, Component, Vue} from 'vue-property-decorator';
import {mainStore} from '@/store';
import LessonCard from '@/components/LessonCard.vue';
import LessonModel from '@/models/LessonModel';

@Component({components: {
  LessonCard,
}})
export default class CourseCalendarView extends Vue {
  @Prop() courseId!: number;

  store = mainStore;

  get getCourse() {
    return this.store.getCourse;
  }

  get getLessons() {
    return this.getCourse.lessons;
  }

  courseTitle: string = this.getCourse.name;

  courseDescription: string = this.getCourse.description || '';

  get canChangeCourseName() {
    return this.getCourse.name === this.courseTitle;
  }

  changeCourseName() {
    this.store.changeCourseName(this.courseTitle);
  }

  get canChangeCourseDescription() {
    return (this.getCourse.description || '') === this.courseDescription;
  }

  changeCourseDescription() {
    this.store.changeCourseDescription(this.courseDescription);
  }

  deleteLesson(lesson: LessonModel) {
    this.store.deleteLesson(lesson);
  }
}
</script>

<style lang="stylus">
  .change__btn
    margin-top: 10px
    background-color: var(--cds-ui-05)
    &:hover
      background-color: var(--cds-ui-04)
</style>
