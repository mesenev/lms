<template>
  <router-link
    :to="openLesson"
    class="list-element"
    v-bind:class="{ 'lesson--hidden': lessonProp.is_hidden, }"
    v-on:click="openLesson"
  >
    <h5 class="list-element--title">{{ lesson.name }}</h5>
    <span class="list-element--info">Дедлайн: {{ lesson.deadline }}</span>
    <span v-if="courseStore.is_staff" class="list-element--info span--hidden">
        {{ (lessonProp.is_hidden) ? "Урок скрыт " : "Урок доступен" }}
        <view-off-icon v-if="lessonProp.is_hidden"/>
        <view-icon v-else/>
      </span>
  </router-link>
</template>

<script lang="ts">
import LessonModel from "@/models/LessonModel";
import courseStore from '@/store/modules/course';
import userStore from '@/store/modules/user';
import viewOffIcon from '@carbon/icons-vue/es/view--off/16';
import viewIcon from '@carbon/icons-vue/es/view/16';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { viewIcon, viewOffIcon } })
export default class LessonListComponent extends Vue {
  @Prop({ required: true }) lessonProp!: LessonModel;

  userStore = userStore;
  courseStore = courseStore;


  get openLesson() {
    return { name: 'LessonView', params: { lessonId: this.lesson.id.toString() } };
  }

  get lesson(): LessonModel {
    return this.lessonProp;
  }

  get isStaff(): boolean {
    const courseId = Number(this.$route.params.courseId);
    return this.userStore.user.staff_for.includes(courseId);
  }
}
</script>

<style scoped lang="stylus">

</style>
