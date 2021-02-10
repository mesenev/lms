<template>
  <transition mode="out-in" name="fade">
    <router-view/>
  </transition>
</template>

<script lang="ts">
import CourseModel from '@/models/CourseModel';
import courseStore from "@/store/modules/course";
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class CourseViewLayout extends Vue {
  @Prop({ required: true }) courseId!: number;

  course: CourseModel | null = null;
  courseStore = courseStore;

  async created() {
    this.courseStore.changeCurrentCourse(null);
    this.course = await this.courseStore.fetchCourseById(this.courseId);
    this.courseStore.changeCurrentCourse(this.course);
  }

}

</script>
