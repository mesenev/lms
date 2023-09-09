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
      <!--  <lesson-stats-graph v-else :lesson="lesson" :user="currentUser"/> -->
    </div>
    <cv-tag v-if="notInSchedule"
            label="Не состоит в расписании"
            kind="red"
            :icon="warningAltFilled"/>
  </router-link>
</template>

<script lang="ts" setup>
import type { PropType } from "vue";
import type { LessonModel } from "@/models/LessonModel";
import useUserStore from "@/stores/modules/user";
import useCourseStore from "@/stores/modules/course";
import viewOffIcon from '@carbon/icons-vue/es/view--off/16';
import viewIcon from '@carbon/icons-vue/es/view/16';
import warningAltFilled from '@carbon/icons-vue/es/warning--alt--filled/16';
import { computed } from "vue";
import DateViewComponent from "@/components/common/DateViewComponent.vue";

const props = defineProps({
  lessonProp: { type: Object as PropType<LessonModel>, required: true },
  dateProp: { type: Number, required: false, default: null },
  notInSchedule: { type: Boolean, required: false, default: false }
})

const userStore = useUserStore();
const courseStore = useCourseStore();

const lesson = computed((): LessonModel => {
  return props.lessonProp;
})

const openLesson = computed(() => {
  return { name: 'LessonView', params: { lessonId: lesson.value.id.toString() } };
})

const currentUser = computed(() => {
  return userStore.user;
})

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
