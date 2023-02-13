<template>
  <router-link
    :to="openTest"
    class="list-element"
    v-on:click="openTest"
  >
    <div class="content-wrapper">
      <div class="title-wrapper">
        <h5 class="list-element--title"> Демо тест по экономике </h5>
      </div>
      <div class="date-wrapper">
        <div class="list-element--info">
<!--          <date-view-component v-if="dateProp" :date-as-integer="dateProp" :show-day-week="true"/>-->
        </div>
      </div>
<!--      <span v-if="courseStore.is_staff" class="list-element&#45;&#45;info span&#45;&#45;hidden">-->
<!--          {{ (lessonProp.is_hidden) ? "Урок скрыт " : "Урок доступен" }}-->
<!--          <view-off-icon v-if="lessonProp.is_hidden"/>-->
<!--          <view-icon v-else/>-->
<!--      </span>-->
<!--      <lesson-stats-graph v-else :lesson="lesson" :user="currentUser"/>-->
    </div>
<!--    <cv-tag v-if="notInSchedule"-->
<!--            label="Не состоит в расписании"-->
<!--            kind="red"-->
<!--            :icon="warningAltFilled"/>-->
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
  // @Prop({ required: true }) lessonProp!: LessonModel;
  // @Prop({ required: false, default: null }) dateProp!: number | null;
  // @Prop({ required: false }) notInSchedule!: false | boolean;

  get openTest() {
    return { name: 'TestView'};
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
