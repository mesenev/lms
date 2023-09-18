<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <div class="main-title">
        <h1 v-if="!loading" class=""> Курс: {{ (course) ? course.name : "" }} </h1>
        <cv-skeleton-text v-else :heading="true" :width="'35%'" class="main-title"/>
        <div class="description-container">
          <span v-if="!loading" class="course-description">
            {{ (course) ? course.description : "" }}
          </span>
          <cv-skeleton-text v-else class="course-description" width="'35%'"/>
        </div>
      </div>
    </div>
    <div class=" bx--row">
      <div :class="(lessons.length) ? 'items bx--col-lg-6 bx--col-md-6'
      : 'empty-items bx--col-lg-6 bx--col-md-6'">
        <cv-data-table-skeleton v-if="loading" :columns="1" :rows="6"/>
        <div v-else-if="lessons.length">
          <cv-search
              v-model:value.trim="searchValue"
              class="search"
              label="label"
              placeholder="Введите название урока"/>
          <div class="lessons-list-wrapper">
            <cv-structured-list class="lessons-list">
              <template v-slot:items>
                <template v-if="filterLessons.length > 0">
                  <cv-structured-list-item
                      class="item"
                      v-for="lesson in filterLessons"
                      :key="lesson.id">
                    <lesson-list-component :date-prop="dateForLesson(lesson.id)"
                                           :lesson-prop='lesson'/>
                  </cv-structured-list-item>
                </template>
                <template v-if="lessonsNotInSchedule.length > 0">
                  <cv-structured-list-item
                      class="item"
                      v-for="lesson in lessonsNotInSchedule"
                      :key="lesson.id">
                    <lesson-list-component :lesson-prop='lesson' :not-in-schedule="true"/>
                  </cv-structured-list-item>
                </template>
              </template>
              <!--          <template slot="items" v-else>-->
              <!--            <h1 v-if="course && user.staff_for.includes(course.id)">-->
              <!--              Расписание для курса не составлено-->
              <!--            </h1>-->
              <!--          </template>-->
            </cv-structured-list>
          </div>
        </div>
        <div v-else class="empty-list-wrapper">
          <empty-list-component list-of="lessons" :text="emptyText"/>
        </div>
      </div>
      <div v-if='course' class="submits bx--col-lg-4 bx--col-md-4">
         <user-submit-list-component v-if="isStaff" :course-id="course.id"/>
        <user-problem-list-component v-else :course-id="course.id"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import UserComponent from '@/components/UserComponent.vue';
import type { CourseModel } from '@/models/CourseModel';
import type { LessonModel } from "@/models/LessonModel";
import type { UserModel } from "@/models/UserModel";
import useCourseStore from "@/stores/modules/course";
import useLessonStore from "@/stores/modules/lesson";
import useUserStore from '@/stores/modules/user';
import { ref, onMounted, computed } from 'vue';
import type { ScheduleElement } from "@/models/ScheduleModel";
import type { CourseScheduleModel } from "@/models/ScheduleModel";
import EmptyListComponent from "@/components/lists/EmptyListComponent.vue";
import LessonListComponent from "@/components/lists/LessonListComponent.vue";
import UserProblemListComponent from '@/components/UserProblemListComponent.vue';
import UserSubmitListComponent from '@/components/UserSubmitListComponent.vue';

const props = defineProps({
  courseId: { type: Number, required: true }
})
const courseStore = useCourseStore()
const lessonStore = useLessonStore()
const userStore = useUserStore()

const searchValue = ref<string>("")
const loading = ref<boolean>(true)
const schedule = ref<CourseScheduleModel | undefined>(undefined)
const emptyText = ref<string>('В данный момент нет доступных уроков.')
const user = ref<UserModel>(userStore.user)

onMounted(async () => {
  schedule.value = await courseStore.fetchCourseScheduleByCourseId(props.courseId);
  await lessonStore.fetchLessonsByCourseId(props.courseId);
  loading.value = false;
})

const isStaff = computed(() => {
  return user.value.staff_for.includes(Number(props.courseId));
})

const course = computed(() => {
  return courseStore.currentCourse;
})

const sortedCourseSchedule = computed(() => {
  if (schedule.value === undefined || schedule.value.lessons === undefined)
    return new Array<LessonModel>();
  const schedule_ptr = (schedule.value as CourseScheduleModel);
  const schedule_lessons = lessons.value.filter(
      lesson => schedule_ptr.lessons.find(elem => elem.lesson_id === lesson.id)?.lesson_id)
  return schedule_lessons.sort(
      (a: LessonModel, b: LessonModel) => {
        const dateA = schedule_ptr.lessons.find(x => x.lesson_id === a.id)?.date as number;
        const dateB = schedule_ptr.lessons.find(x => x.lesson_id === b.id)?.date as number;
        return (dateA < dateB) ? -1 : 1;
      },
  );
})

const filterLessons = computed(() => {
  sortedCourseSchedule.value.map(lesson =>
      lessons.value.find(elem => elem.name === lesson.name))
      .filter(lesson => typeof lesson != "undefined");
  if (!isStaff.value) {
    const sortedCourseSchedule_ptr = sortedCourseSchedule.value.filter(
        lesson => lesson.name.toLowerCase().includes(searchValue.value.toLowerCase())
    );
    if (sortedCourseSchedule_ptr.length)
      return sortedCourseSchedule_ptr;
  }
  return sortedCourseSchedule.value
})

const lessons = computed((): Array<LessonModel> => {
  if (!(props.courseId in lessonStore.lessonsByCourse))
    return [];
  const lessons_ptr = lessonStore.lessonsByCourse[props.courseId].filter(lesson => {
    return lesson.name.toLowerCase().includes(searchValue.value.toLowerCase());
  });
  if (isStaff.value)
    if (lessons_ptr.length)
      return lessons_ptr;
  return lessonStore.lessonsByCourse[props.courseId];
})

const lessonsNotInSchedule = computed(() => {
  return lessons.value.filter(lesson => !filterLessons.value.map(lesson => lesson.id)
      .includes(lesson.id)).sort((a: LessonModel, b: LessonModel) => {
    return a.id - b.id;
  });
})

function dateForLesson(lesson_id: number) {
  return ((schedule.value as CourseScheduleModel)
      .lessons.find(x => x.lesson_id === lesson_id) as ScheduleElement).date;
}

</script>

<style scoped lang="stylus">
.description-container
  display flex
  max-width 70%
  word-break break-word
  color var(--cds-text-02)
  font-weight var(--cds-display-02-font-weight)
  margin-top var(--cds-spacing-03)

.items
  padding-top 1rem
  padding-bottom 1rem
  margin-bottom 1rem
  margin-right 1rem
  background-color var(--cds-ui-01)

  /deep/ .bx--search-input
    background-color var(--cds-ui-background)

.lessons-list-wrapper
  max-height 50vh;
  overflow-y auto

.submits
  padding-left 0
  margin-bottom 1rem

  /deep/ .submit-list-data
    background-color var(--cds-ui-01)

.empty-items
  background-color var(--cds-ui-01)
  display flex
  align-items center
  margin-bottom 1rem
  margin-right 1rem
  padding-bottom 1rem

.lessons-list
  margin-bottom 0

</style>
