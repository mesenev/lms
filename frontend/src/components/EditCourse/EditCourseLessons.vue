<template>
  <div>
    <cv-structured-list class="lesson--list" v-if="course.lessons.length">
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
                                 v-for="lesson in courseLessons"
                                 :key="lesson.id">
          <LessonCard :lesson="lesson"
                      :main-icon="TrashCan32"
                      :second-icon="Settings32"
                      :manipulation="deleteLesson">
          </LessonCard>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
import { mainStore } from '@/store';
import LessonModel from '@/models/LessonModel';
import CourseModel from '@/models/CourseModel';
import LessonCard from '@/components/EditCourse/LessonCard.vue';
import { TrashCan32, Settings32 } from '@carbon/icons-vue/es/index';
import searchByLessons from '@/common/searchByLessons';

@Component({components: {
  LessonCard,
  TrashCan32,
  Settings32,
}})
export default class EditCourseLessons extends Vue {
  @Prop({ required: true }) course!: CourseModel;

  TrashCan32 = TrashCan32;

  Settings32 = Settings32;

  store = mainStore;

  searchQueryForCourseLessons = '';

  get courseLessons(): LessonModel[] {
    return searchByLessons(this.searchQueryForCourseLessons, this.course.lessons);
  }

  deleteLesson(lesson: LessonModel) {
    this.store.deleteLesson(lesson);
  }
}
</script>

<style lang="stylus">
  .bx--modal-content:focus
    outline none

  .lesson--list
    margin-bottom 0

  .lesson-card:hover
    border-bottom 1px solid var(--cds-ui-05)
</style>
