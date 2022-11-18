<template>
  <router-link
    :to="{ name: 'CourseView', params: { courseId: this.course.id.toString() } }"
    class="list-element">
    <div class="list-element--main">
      <h5 class="list-element--title">{{ course.name }}</h5>
      <span class="list-element--info">Преподаватель: {{ teacher }}</span>
    </div>
    <div class="list-element--btns list-element" v-if="isStaff">
      <component class="trash-icon" :is="TrashCan" @click.prevent.stop="deleteCourse(course)"/>
      <component class="settings-icon" :is="Settings" @click.prevent.stop="editCourse(course)"/>
    </div>
    <!--    <span class="list-element&#45;&#45;info">Следующий урок: {{ "24/1" }}</span>-->
  </router-link>
</template>

<script lang="ts">
import CourseModel from '@/models/CourseModel';
import { Component, Prop, Vue } from 'vue-property-decorator';
import TrashCan from '@carbon/icons-vue/es/trash-can/20';
import Settings from '@carbon/icons-vue/es/settings/20';
import router from "@/router";
import userStore from '@/store/modules/user';

@Component
export default class CourseListComponent extends Vue {
  @Prop({ required: true }) courseProp!: CourseModel;
  TrashCan = TrashCan;
  Settings = Settings;
  userStore = userStore;

  get course(): CourseModel {
    return this.courseProp;
  }

  get teacher(): string {
    if (!this.course.author)
      return '';
    if (this.course.author.middle_name)
      return `${this.course.author.first_name} `
        + `${this.course.author.middle_name} `
        + `${this.course.author.last_name}`;
    return `${this.course.author.first_name} ${this.course.author.last_name}`;
  }

  get isStaff() {
    return this.userStore.user.staff_for.includes(this.course.id);
  }

  editCourse(course: CourseModel) {
    router.push({ name: 'course-edit', params: { courseId: course.id.toString() } });
  }

  deleteCourse(course: CourseModel) {
    this.$emit('show-confirm-modal', course);
  }
}
</script>

<style scoped lang="stylus">
.list-element
  display flex
  flex-direction row
  justify-content space-between
  padding-right 0.5rem

.trash-icon
  margin-right 0.5rem

</style>
