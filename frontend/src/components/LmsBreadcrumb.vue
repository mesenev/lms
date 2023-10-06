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

<script lang="ts" setup>

import useProblemStore from "@/stores/modules/problem";
import useLessonStore from "@/stores/modules/lesson";
import useCourseStore from "@/stores/modules/course";
import useMaterialStore from "@/stores/modules/material";
import useExamStore from "@/stores/modules/exam";
import {computed} from "vue";
import {useRoute} from "vue-router";
import LmsBreadcrumbItem from "@/components/LmsBreadcrumbItem.vue";

const problemStore = useProblemStore();
const lessonStore = useLessonStore();
const courseStore = useCourseStore();
const materialStore = useMaterialStore();
const examStore = useExamStore();

const route = useRoute()

function isSelected(param: string) {
  const selected = route.params.hasOwnProperty(param) && !!route.params[param];
  return {
    selected,
    id: selected ? Number(route.params[param]) : NaN,
  };
}

function selectedView(pageView: string, param: string, crumbName: string) {
  let selected = false;
  let value = null;
  if (route.name === pageView) {
    selected = true;
    value = {id: route.params[param], name: crumbName};
  }
  return {selected, value, pageView};
}

const courseSelected = computed(() => {
  return isSelected('courseId');
})

const lessonSelected = computed(() => {
  return isSelected('lessonId');
})

const problemSelected = computed(() => {
  return isSelected('problemId');
})

const materialSelected = computed(() => {
  return isSelected('materialId');
})

const examSelected = computed(() => {
  return isSelected('examId');
})

const examEditSelected = computed(() => {
  return selectedView(
      'exam-edit',
      'examId',
      'Редактирование теста'
  );
})

const courseEditSelected = computed(() => {
  if (route.name === 'course-edit') {
    return selectedView(
        'course-edit',
        'courseId',
        'Редактирование курса'
    );
  }
  return selectedView(
      'course-add',
      'courseId',
      'Создание курса'
  );
})

const lessonEditSelected = computed(() => {
  return selectedView(
      'lesson-edit',
      'lessonId',
      'Редактирование урока'
  );
})

const profileSelected = computed(() => {
  return selectedView(
      'profile-page',
      'userId',
      'Профиль'
  );
})

const courseSolutionsListSelected = computed(() => {
  return selectedView(
      'course-solutions-list',
      'courseId',
      'Отправленные решения'
  );
})

const courseProgressSelected = computed(() => {
  return selectedView(
      'course-progress',
      'courseId',
      'Успеваемость курса'
  );
})

const courseScheduleSelected = computed(() => {
  return selectedView(
      'course-calendar',
      'courseId',
      'Расписание занятий'
  );
})

const lessonProgressSelected = computed(() => {
  return selectedView(
      'lesson-progress',
      'lessonId',
      'Успеваемость урока'
  );
})

const submitSelected = computed(() => {
  const submitId = route.params['submitId'];
  return selectedView(
      'ProblemViewWithSubmit',
      'submitId',
      `Решение №${submitId}`
  );
})

const examSolutionSelected = computed(() => {
  return selectedView(
      'ExamViewWithSolution',
      'solutionId',
      'Решение'
  );
})

const materialEditSelected = computed(() => {
  return selectedView(
      'material-edit',
      'materialId',
      'Редактирование материала'
  );
})

const problemEditSelected = computed(() => {
  return selectedView(
      'problem-edit',
      'problemId',
      'Редактирование задачи'
  );
})

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
