<template>
  <router-link
    :to="openLesson"
    class="list-element"
    v-bind:class="{ 'lesson--hidden': lessonProp.is_hidden, }"
    v-on:click="openLesson"
  >
    <div class="content-wrapper">
      <div class="title-wrapper">
        <h5 class="list-element--title">{{ lesson.name }}</h5>
      </div>
      <div class="date-wrapper">
        <div class="list-element--info">
          <date-view-component v-if="dateProp" :date-as-integer="dateProp" :show-day-week="true"/>
        </div>
      </div>
      <span v-if="courseStore.is_staff" class="list-element--info span--hidden">
          {{ (lessonProp.is_hidden) ? "Урок скрыт " : "Урок доступен" }}
          <view-off-icon v-if="lessonProp.is_hidden"/>
          <view-icon v-else/>
      </span>
      <lesson-stats-graph v-else :lesson="lesson" :user="currentUser"/>
    </div>
    <cv-tag v-if="notInSchedule"
            label="Не состоит в расписании"
            kind="red"
            :icon="warningAltFilled"/>
  </router-link>
</template>

<script lang="ts">
import LessonModel from "@/models/LessonModel";
import courseStore from '@/store/modules/course';
import userStore from '@/store/modules/user';
import viewOffIcon from '@carbon/icons-vue/es/view--off/16';
import viewIcon from '@carbon/icons-vue/es/view/16';
import warningAltFilled from '@carbon/icons-vue/es/warning--alt--filled/16';
import { Component, Prop, Vue } from 'vue-property-decorator';
import DateViewComponent from "@/components/common/DateViewComponent.vue"
import LessonStatsGraph from "@/components/LessonStatsGraph.vue";

@Component({
  components: {
    viewIcon,
    viewOffIcon,
    warningAltFilled,
    DateViewComponent,
    LessonStatsGraph
  }
})
export default class LessonListComponent extends Vue {
  @Prop({ required: true }) lessonProp!: LessonModel;
  @Prop({ required: false, default: null }) dateProp!: number | null;
  @Prop({ required: false }) notInSchedule!: false | boolean;

  userStore = userStore;
  courseStore = courseStore;
  warningAltFilled = warningAltFilled;

  get openLesson() {
    return { name: !this.lesson.is_control_work ? 'LessonView' : 'ControlWorkView',
      params: { controlWorkId: this.lesson.id.toString() } };
  }

  get lesson(): LessonModel {
    return this.lessonProp;
  }

  get isStaff(): boolean {
    const courseId = Number(this.$route.params.courseId);
    return this.userStore.user.staff_for.includes(courseId);
  }

  get currentUser() {
    return this.userStore.user;
  }
}
</script>

<style scoped lang="stylus">
.list-element
  display flex
  flex-direction row
  justify-content space-between
  align-items center

.cv-tag
  display flex
  align-items stretch
  margin-right 1rem
</style>
