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
      <div class="items bx--col-lg-6">
        <cv-search
          v-model.trim="searchValue"
          class="search"
          label="label"
          placeholder="search"
          size="size"/>
        <cv-data-table-skeleton v-if="loading" :columns="1" :rows="6"/>
        <cv-structured-list v-else>
          <template slot="items" v-if="filterLessons.length > 0">
            <cv-structured-list-item
              class="item"
              v-for="lesson in filterLessons"
              :key="lesson.id">
              <lesson-list-component :date-prop="dateForLesson(lesson.id)" :lesson-prop='lesson'/>
            </cv-structured-list-item>
          </template>
          <template slot="items" v-if="isStaff && lessonsNotInSchedule.length > 0">
            <h3>Следующие уроки не входят в нынешнее расписание, и ученики их не видят:</h3>
            <cv-structured-list-item
              class="item"
              v-for="lesson in lessonsNotInSchedule"
              :key="lesson.id">
              <lesson-list-component :lesson-prop='lesson'/>
            </cv-structured-list-item>
          </template>
          <!--          <template slot="items" v-else>-->
          <!--            <h1 v-if="course && user.staff_for.includes(course.id)">-->
          <!--              Расписание для курса не составлено-->
          <!--            </h1>-->
          <!--          </template>-->
        </cv-structured-list>
      </div>
      <div v-if='course' class="submits bx--col-lg-4">
        <user-submit-list-component v-if="isStaff" :course-id="course.id"/>
        <user-problem-list-component v-else :course-id="course.id"/>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
import LessonListComponent from "@/components/lists/LessonListComponent.vue";
import UserComponent from '@/components/UserComponent.vue';
import UserProblemListComponent from "@/components/UserProblemListComponent.vue"
import UserSubmitListComponent from "@/components/UserSubmitListComponent.vue"
import CourseModel from '@/models/CourseModel';
import LessonModel from "@/models/LessonModel";
import courseStore from "@/store/modules/course";
import lessonStore from "@/store/modules/lesson";
import userStore from '@/store/modules/user';
import { Component, Prop, Vue } from 'vue-property-decorator';
import CourseScheduleModel, { ScheduleElement } from "@/models/ScheduleModel";

@Component({
  components: {
    UserProblemListComponent, LessonListComponent, UserComponent, UserSubmitListComponent,
  },
})
export default class CourseView extends Vue {
  @Prop({ required: true }) courseId!: number;
  courseStore = courseStore;
  lessonStore = lessonStore;
  searchValue = "";
  loading = true;
  schedule: CourseScheduleModel | undefined;
  private userStore = userStore;
  private user = this.userStore.user;

  async created() {
    this.schedule = await this.courseStore.fetchCourseScheduleByCourseId(this.courseId);
    await this.lessonStore.fetchLessonsByCourseId(this.courseId);
    this.loading = false;
  }

  get isStaff(): boolean {
    return this.user.staff_for.includes(Number(this.courseId));
  }

  get lessons(): Array<LessonModel> {
    if (!(this.courseId in this.lessonStore.lessonsByCourse))
      return [];
    return this.lessonStore.lessonsByCourse[this.courseId];
  }

  get lessonsNotInSchedule() {
    return this.lessons.filter(lesson => !this.filterLessons.map(lesson => lesson.id)
      .includes(lesson.id)).sort((a: LessonModel, b: LessonModel) => {
        return a.id - b.id;
    });
  }

  get course(): CourseModel | null {
    return this.courseStore.currentCourse;
  }

  get filterLessons() {
    this.sortedCourseSchedule.map(lesson =>
      this.lessons.find(elem => elem.name === lesson.name))
      .filter(lesson => typeof lesson != "undefined");
    return this.sortedCourseSchedule;
  }

  get sortedCourseSchedule() {
    if (this.schedule === undefined || this.schedule.lessons === undefined)
      return new Array<LessonModel>();
    const schedule = (this.schedule as CourseScheduleModel);
    const schedule_lessons = this.lessons.filter(
      lesson => schedule.lessons.find(elem => elem.lesson_id === lesson.id)?.lesson_id)
    return schedule_lessons.sort(
      (a: LessonModel, b: LessonModel) => {
        const dateA = schedule.lessons.find(x => x.lesson_id === a.id)?.date as number;
        const dateB = schedule.lessons.find(x => x.lesson_id === b.id)?.date as number;
        return (dateA < dateB) ? -1 : 1;
      },
    );
  }

  dateForLesson(lesson_id: number) {
    return ((this.schedule as CourseScheduleModel)
      .lessons.find(x => x.lesson_id === lesson_id) as ScheduleElement).date;
  }

}

</script>
