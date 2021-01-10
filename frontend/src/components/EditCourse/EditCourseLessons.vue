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
                      :main-icon="TrashCan"
                      :second-icon="Settings"
                      :manipulation="deleteLesson">
          </LessonCard>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
</template>

<script lang="ts">
import searchByLessons from '@/common/searchByLessons';
import LessonCard from '@/components/EditCourse/LessonCard.vue';
import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import Settings20 from '@carbon/icons-vue/es/settings/20';
import TrashCan20 from '@carbon/icons-vue/es/trash-can/20';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({
  components: {
    LessonCard,
    TrashCan20,
    Settings20,
  },
})
export default class EditCourseLessons extends Vue {
  @Prop({ required: true }) course!: CourseModel;

  TrashCan = TrashCan20;

  Settings = Settings20;

  searchQueryForCourseLessons = '';

  get courseLessons(): LessonModel[] {
    return searchByLessons(this.searchQueryForCourseLessons, this.course.lessons);
  }

  deleteLesson(lesson: LessonModel) {
    //
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
