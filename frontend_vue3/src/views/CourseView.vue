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
            v-model.trim="searchValue"
            class="search"
            label="label"
            placeholder="Введите название урока"
            size="size"/>
          <div class="lessons-list-wrapper">
            <cv-structured-list class="lessons-list">
              <template slot="items" v-if="filterLessons.length > 0">
                <cv-structured-list-item
                  class="item"
                  v-for="lesson in filterLessons"
                  :key="lesson.id">
                </cv-structured-list-item>
              </template>
              <template slot="items" v-if="isStaff && lessonsNotInSchedule.length > 0">
                <cv-structured-list-item
                  class="item"
                  v-for="lesson in lessonsNotInSchedule"
                  :key="lesson.id">
                </cv-structured-list-item>
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
        </div>
      </div>
    </div>

  </div>
</template>


<script lang="ts" setup>
import UserComponent from '@/components/UserComponent.vue';
import UserProblemListComponent from "@/components/UserProblemListComponent.vue"
import CourseModel from '@/models/CourseModel';
import LessonModel from "@/models/LessonModel";
import { UserModel } from "@/models/UserModel";
import useCourseStore from "@/stores/modules/course";
import useLessonStore from "@/stores/modules/lesson";
import useUserStore from '@/stores/modules/user';
import { defineProps, Ref, ref, onMounted, computed } from 'vue';
import CourseScheduleModel, { ScheduleElement } from "@/models/ScheduleModel";
import EmptyListComponent from "@/components/EmptyListComponent.vue";

const props = defineProps(['courseId'])
const courseStore = useCourseStore()
const lessonStore = useLessonStore()
const userStore = useUserStore()

const searchValue: Ref<string> = ref('')
const loading: Ref<boolean> = ref(true)
const schedule: Ref<CourseScheduleModel> | Ref<undefined> = ref(undefined)
const emptyText: Ref<string> = ref('В данный момент нет доступных уроков.')
const user: Ref<UserModel>  = ref(userStore.user)

onMounted(async ()=>{
  schedule.value = await courseStore.fetchCourseScheduleByCourseId(props.courseId);
  await lessonStore.fetchLessonsByCourseId(props.courseId);
  loading.value = false;
})

const isStaff = computed(()=>{
  return user.staff_for.includes(Number(props.courseId));
})

const course = computed(() => {
  return courseStore.currentCourse;
})

const sortedCourseSchedule = computed(() =>{
  if (schedule === undefined || schedule.lessons === undefined)
      return new Array<LessonModel>();
    const schedule_ptr = (schedule as CourseScheduleModel);
    const schedule_lessons = this.lessons.filter(
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
  sortedCourseSchedule.map(lesson =>
      this.lessons.find(elem => elem.name === lesson.name))
      .filter(lesson => typeof lesson != "undefined");
    if (!isStaff) {
      const sortedCourseSchedule = sortedCourseSchedule.filter(
        lesson => lesson.name.toLowerCase().includes(searchValue.toLowerCase())
      );
      if (sortedCourseSchedule.length)
        return sortedCourseSchedule;
    }
    return sortedCourseSchedule
})

const lessons = computed((): Array<LessonModel> =>{
  if (!(props.courseId in lessonStore.lessonsByCourse))
      return [];
    const lessons = lessonStore.lessonsByCourse[props.courseId].filter(lesson => {
      return lesson.name.toLowerCase().includes(searchValue.toLowerCase());
    });
    if (isStaff)
      if (lessons.length)
        return lessons;
    return lessonStore.lessonsByCourse[this.courseId];
})

const lessonsNotInSchedule = computed(() => {
    return lessons.filter(lesson => !filterLessons.map(lesson => lesson.id)
      .includes(lesson.id)).sort((a: LessonModel, b: LessonModel) => {
      return a.id - b.id;
    });
})

const dateForLesson = computed((lesson_id: number) => {
    return ((this.schedule as CourseScheduleModel)
      .lessons.find(x => x.lesson_id === lesson_id) as ScheduleElement).date;
})





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
