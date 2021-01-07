<template>
  <div>
    <cv-structured-list class="problem--list" v-if="lesson.problems.length">
      <template slot="headings">
        <cv-structured-list-heading>
          <h4>Задания</h4>
        </cv-structured-list-heading>
      </template>
      <template slot="items">
        <cv-search label="Поиск"
                   v-model="searchQueryForLessonProblems">
        </cv-search>
        <cv-structured-list-item class="problem-card"
                                 v-for="problem in lessonProblems"
                                 :key="problem.id">
          <ProblemCard :problem="problem"
                      :main-icon="TrashCan32"
                      :second-icon="Settings32"
                      :manipulation="deleteProblem">
          </ProblemCard>
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
import Lesson from "@/components/Lesson.vue";
import ProblemModel from "@/models/ProblemModel";
import ProblemCard from "@/components/EditLesson/ProblemCard.vue";

@Component({components: {
    ProblemCard,
    TrashCan32,
    Settings32,
}})
export default class EditLessonProblemss extends Vue {
  @Prop({ required: true }) course!: LessonModel;

  TrashCan32 = TrashCan32;

  Settings32 = Settings32;

  store = mainStore;

  searchQueryForLessonProblems = '';

  get courseLessons(): ProblemModel[] {
    return searchByProblems(this.searchQueryForLessonProblems, this.course.problems);
  }

  deleteProblem(lesson: ProblemModel) {
    this.store.deleteProblem(problem);
  }
}
</script>

<style lang="stylus">
  .bx--modal-content:focus
    outline none

  .problem--list
    margin-bottom 0

  .problem-card:hover
    border-bottom 1px solid var(--cds-ui-05)
</style>
