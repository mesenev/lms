<template>
  <div class="bx--grid breadcrumb">
    <cv-breadcrumb>
      <transition name="fade" mode="out-in">
        <cv-breadcrumb-item>
          <router-link :to="{
            path: '/',
          }">
            Список курсов
          </router-link>
        </cv-breadcrumb-item>
      </transition>
      <transition name="fade" mode="out-in">
        <cv-breadcrumb-item v-if="courseSelected">
          <router-link :to="{
            name: 'CourseView',
            props: this.$route.params.CourseId
          }">
            {{ course }}
          </router-link>
        </cv-breadcrumb-item>
      </transition>
      <transition name="fade" mode="out-in">
        <cv-breadcrumb-item v-if="lessonSelected">
          <router-link :to="{
            name: 'LessonView',
            props: this.$route.params.lessonId
          }">
            {{ lesson }}
          </router-link>
        </cv-breadcrumb-item>
      </transition>
      <transition name="fade" mode="out-in">
        <cv-breadcrumb-item v-if="problemSelected">
          {{ problem }}
        </cv-breadcrumb-item>
      </transition>
    </cv-breadcrumb>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from "vue-property-decorator";
import problemStore from '@/store/modules/problem';
import lessonStore from '@/store/modules/lesson';
import courseStore from '@/store/modules/course';

@Component
export default class VueBreadcrumb extends Vue {

  get courseSelected(): boolean {
    return this.$route.params.hasOwnProperty('courseId');
  }
  get lessonSelected(): boolean {
    return this.$route.params.hasOwnProperty('lessonId');
  }

  get problemSelected(): boolean {
    return this.$route.params.hasOwnProperty('problemId');
  }

  get materialSelected(): boolean {
    return this.$route.params.hasOwnProperty('materialId');
  }

  course = '';
  problem = '';
  lesson = '';

  private async updateBreadCrumb() {
    if (this.courseSelected) {
      const courseId = Number(this.$route.params.courseId);
      const course = await courseStore.fetchCourseById(courseId);
      this.course = course.name;
    }
    if (this.problemSelected) {
      const problemId = Number(this.$route.params.problemId);
      const problem = await problemStore.fetchProblemById(problemId);
      this.problem = problem.name;
    }
    if (this.lessonSelected) {
      const lessonId = Number(this.$route.params.lessonId);
      const lesson = await lessonStore.fetchLessonById(lessonId);
      this.lesson = lesson.name;
    }
  }

  // ToDo old name is displayed 0.001 sec

  async updated() {
    await this.updateBreadCrumb();
  }

  async created() {
    await this.updateBreadCrumb();
  }
}


</script>

<style lang="stylus" scoped>
  .breadcrumb
    margin-top 1rem

  .fade-enter-active, .fade-leave-active {
    transition: opacity .1s
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    opacity: 0
  }
</style>
