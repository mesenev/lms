<template>
  <div class="bx--grid">
    <cv-breadcrumb>
      <cv-breadcrumb-item>
        <router-link :to="{ path: '/', }">Список курсов</router-link>
      </cv-breadcrumb-item>
      <lms-breadcrumb-item
        v-if="courseSelected.selected"
        :model="courseStore.currentCourse"
        page-view="CourseView"
      />
      <lms-breadcrumb-item
        v-if="courseProgressSelected.selected"
        :model="courseProgressSelected.value"
        :page-view="courseProgressSelected.pageView"/>
      <lms-breadcrumb-item
        v-if="courseScheduleSelected.selected"
        :model="courseScheduleSelected.value"
        :page-view="courseScheduleSelected.pageView"
      />
      <lms-breadcrumb-item
        v-if="courseSolutionsListSelected.selected"
        :model="courseSolutionsListSelected.value"
        :page-view="courseSolutionsListSelected.pageView"
      />
      <lms-breadcrumb-item
        v-if="profileSelected.selected"
        :model="profileSelected.value"
        page-view="profile-page"
      />
      <lms-breadcrumb-item
        v-if="lessonSelected.selected"
        :model="lessonStore.currentLesson"
        page-view="LessonView"
      />
      <lms-breadcrumb-item
        v-if="lessonProgressSelected.selected"
        :model="lessonProgressSelected.value"
        :page-view="lessonProgressSelected.pageView"
      />
      <lms-breadcrumb-item
        v-if="examSelected.selected"
        :model="examStore.currentExam"
        page-view="ExamView"/>
      <lms-breadcrumb-item
        v-if="examSolutionSelected.selected"
        :model="examSolutionSelected.value"
        :page-view="examSolutionSelected.pageView"
      />
      <lms-breadcrumb-item
        v-if="examEditSelected.selected"
        :model="examEditSelected.value"
        :page-view="examEditSelected.pageView"
      />
      <lms-breadcrumb-item
        v-if="problemSelected.selected"
        :model="problemStore.currentProblem"
        page-view="ProblemView"
      />
      <lms-breadcrumb-item
        v-if="submitSelected.selected"
        :model="submitSelected.value"
        :page-view="submitSelected.pageView"
      />
      <lms-breadcrumb-item
        v-if="materialSelected.selected"
        :model="materialStore.currentMaterial"
        page-view="MaterialView"
      />
      <lms-breadcrumb-item
        v-if="courseEditSelected.selected"
        :model="courseEditSelected.value"
        :page-view="courseEditSelected.pageView"
      />
      <lms-breadcrumb-item
        v-if="lessonEditSelected.selected"
        :model="lessonEditSelected.value"
        :page-view="lessonEditSelected.pageView"
      />
      <lms-breadcrumb-item
        v-if="problemEditSelected.selected"
        :model="problemEditSelected.value"
        :page-view="problemEditSelected.pageView"
      />
      <lms-breadcrumb-item
        v-if="materialEditSelected.selected"
        :model="materialEditSelected.value"
        :page-view="materialEditSelected.pageView"
      />
    </cv-breadcrumb>
  </div>
</template>

<script lang="ts">

import LmsBreadcrumbItem from "@/components/LmsBreadcrumbItem.vue";
import courseStore from '@/store/modules/course';
import lessonStore from '@/store/modules/lesson';
import materialStore from '@/store/modules/material';
import problemStore from '@/store/modules/problem';
import examStore from '@/store/modules/exam';
import { Component, Vue } from "vue-property-decorator";

@Component({ components: { LmsBreadcrumbItem } })
export default class LmsBreadcrumb extends Vue {
  problemStore = problemStore;
  lessonStore = lessonStore;
  courseStore = courseStore;
  materialStore = materialStore;
  examStore = examStore;

  private isSelected(param: string) {
    const selected = this.$route.params.hasOwnProperty(param) && !!this.$route.params[param];
    return {
      selected,
      id: selected ? Number(this.$route.params[param]) : NaN,
    };
  }

  selectedView(pageView: string, param: string, crumbName: string) {
    let selected = false;
    let value = null;
    if (this.$route.name === pageView) {
      selected = true;
      value = { id: this.$route.params[param], name: crumbName };
    }
    return { selected, value, pageView };
  }

  get courseSelected() {
    return this.isSelected('courseId');
  }

  get lessonSelected() {
    return this.isSelected('lessonId');
  }

  get problemSelected() {
    return this.isSelected('problemId');
  }

  get materialSelected() {
    return this.isSelected('materialId');
  }

  get examSelected() {
    return this.isSelected('examId');
  }

  get examEditSelected() {
    return this.selectedView(
      'exam-edit',
      'examId',
      'Редактирование теста'
    );
  }

  get courseEditSelected() {
    if (this.$route.name === 'course-edit') {
      return this.selectedView(
        'course-edit',
        'courseId',
        'Редактирование курса'
      );
    }
    return this.selectedView(
      'course-add',
      'courseId',
      'Создание курса'
    );
  }

  get lessonEditSelected() {
    return this.selectedView(
      'lesson-edit',
      'lessonId',
      'Редактирование урока'
    );
  }

  get profileSelected() {
    return this.selectedView(
      'profile-page',
      'userId',
      'Профиль'
    );
  }

  get courseSolutionsListSelected() {
    return this.selectedView(
      'course-solutions-list',
      'courseId',
      'Отправленные решения'
    );
  }

  get courseProgressSelected() {
    return this.selectedView(
      'course-progress',
      'courseId',
      'Успеваемость курса'
    );
  }

  get courseScheduleSelected() {
    return this.selectedView(
      'course-calendar',
      'courseId',
      'Расписание занятий'
    );
  }

  get lessonProgressSelected() {
    return this.selectedView(
      'lesson-progress',
      'lessonId',
      'Успеваемость урока'
    );
  }

  get submitSelected() {
    const submitId = this.$route.params['submitId'];
    return this.selectedView(
      'ProblemViewWithSubmit',
      'submitId',
      `Решение №${submitId}`
    );
  }

  get examSolutionSelected() {
    return this.selectedView(
      'ExamViewWithSolution',
      'solutionId',
      'Решение'
    );
  }

  get materialEditSelected() {
    return this.selectedView(
      'material-edit',
      'materialId',
      'Редактирование материала'
    );
  }

  get problemEditSelected() {
    return this.selectedView(
      'problem-edit',
      'problemId',
      'Редактирование задачи'
    );
  }

}
</script>

<style lang="stylus" scoped>

.fade-enter-active, .fade-leave-active {
  transition: opacity .1s
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */
{
  opacity: 0
}
</style>
