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
        v-if="lessonSelected.selected"
        :model="lessonStore.currentLesson"
        page-view="LessonView"
      />
      <lms-breadcrumb-item
        v-if="examSelected.selected"
        :model="examStore.currentExam"
        page-view="TestView"/>
      <lms-breadcrumb-item
        v-if="problemSelected.selected"
        :model="problemStore.currentProblem"
        page-view="ProblemView"
      />
      <lms-breadcrumb-item
        v-if="materialSelected.selected"
        :model="materialStore.currentMaterial"
        page-view="MaterialView"
      />
      <lms-breadcrumb-item
        v-if="courseEditSelected.selected"
        :model="courseEditSelected.value"
        :page-view="courseEditSelected.page_view"
      />
      <lms-breadcrumb-item
        v-if="lessonEditSelected.selected"
        :model="lessonEditSelected.value"
        page-view="lesson-edit"
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

  get courseEditSelected() {
    let selected = false;
    let value = null;
    let page_view;
    if (this.$route.name === 'course-edit') {
      page_view = this.$route.name;
      selected = true;
      value = { id: this.$route.params['courseId'], name: 'Редактирование курса' };
    } else if (this.$route.name === 'course-add') {
      page_view = this.$route.name;
      selected = true;
      value = { id: this.$route.params['courseId'], name: 'Создание курса' };
    }
    return { selected, value, page_view };
  }

  get lessonEditSelected() {
    let selected = false;
    let value = null;
    if (this.$route.name === 'lesson-edit') {
      selected = true;
      value = { id: this.$route.params['lessonId'], name: 'Редактирование урока' };
    }
    return { selected, value };
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
