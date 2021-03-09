<template>
  <transition mode="out-in" name="fade">
    <router-view v-if="course"/>
    <cv-loading v-else/>
  </transition>
</template>

<script lang="ts">
import CourseModel from '@/models/CourseModel';
import UserModel from '@/models/UserModel';
import courseStore from "@/store/modules/course";
import userStore from "@/store/modules/user";
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class CourseViewLayout extends Vue {
  @Prop({ required: true }) courseId!: number;

  course: CourseModel | null = null;
  courseStore = courseStore;
  userStore = userStore;

  async created() {
    this.courseStore.changeCurrentCourse(null);
    this.course = await this.courseStore.fetchCourseById(this.courseId);
    this.courseStore.changeCurrentCourse(this.course);
    const users = this.course.students.reduce(
      (previousValue: { [key: number]: UserModel }, currentValue) => {
        previousValue[currentValue.id] = currentValue;
        return previousValue;
      }, {});
    this.userStore.fetchStudentsMutation(users);
  }

}

</script>
