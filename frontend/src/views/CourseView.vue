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
        {{courseSchedule()}}
        <cv-data-table-skeleton v-if="loading" :columns="1" :rows="6"/>
        <cv-structured-list v-else>
          <template slot="items" v-if="filterLessons.length > 0">
            <cv-structured-list-item
              class="item"
              v-for="lesson in filterLessons"
              :key="lesson.id">
              <lesson-list-component :lesson-prop='lesson'/>
            </cv-structured-list-item>
          </template>
          <template slot="items" v-else>
              <h1 v-if="user.staff_for.includes(course.id)">Расписание для курса не составлено</h1>
          </template>
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
import {Component, Prop, Vue} from 'vue-property-decorator';
import CourseScheduleModel from "@/models/ScheduleModel";

@Component({
  components: {
    UserProblemListComponent, LessonListComponent, UserComponent,
    UserSubmitListComponent,
  },
})
export default class CourseView extends Vue {
  @Prop({ required: true }) courseId!: number;
  courseStore = courseStore;
  lessonStore = lessonStore;
  searchValue = "";
  loading = true;
  schedule = Array<CourseScheduleModel>();
  private userStore = userStore;
  private user = this.userStore.user;

  async created() {
    await this.lessonStore.fetchLessonsByCourseId(this.courseId);
    this.loading = false;
  }

  get isStaff(): boolean {
    return this.user.staff_for.includes(Number(this.courseId));
  }

  get lessons(): Array<LessonModel> {
    if (!(this.courseId in this.lessonStore.lessonsByCourse)) {
      return [];
    }

    return this.lessonStore.lessonsByCourse[this.courseId];
  }

  get course(): CourseModel | null {
    return this.courseStore.currentCourse;
  }

  get filterLessons() {
    // return this.lessons.filter((l: LessonModel) => {
    //   return l.name.toLowerCase().includes(this.searchValue.toLowerCase());
    // });
    const filteredLessons = Array<LessonModel>();
    for (let i = 0; i < this.sortedCourseSchedule.size; i++)
    {
      if (typeof this.sortedCourseSchedule.get(i) != "undefined") {
        const name = this.sortedCourseSchedule.get(i).name;
        this.lessons.forEach(lesson => {
          if (lesson.name === name) {
            filteredLessons[i] = lesson;
          }
        })
      }
    }
    return filteredLessons
  }

   courseSchedule() {
     courseStore.fetchCourseScheduleByCourseId(this.courseId).then((value) =>
     {this.schedule = Array(value)});
  }


  get sortedCourseSchedule() {
    if (this.schedule[0].lessons === undefined)
    {
      return new Map<number, LessonModel>();
    }
    function parseDate(date: string): Date {
    date = date.split(', ')[1].replace(' г.', '');
    const months_ru = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа',
      'сентября', 'октября', 'ноября', 'декабря']
    const months_en = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
      'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for (let i = 0; i < months_ru.length; i++) {
      if (date.includes(months_ru[i])) {
        date = date.replace(months_ru[i], months_en[i]);
        break;
      }
    }
    return new Date(date);
  }
    function orderLessons(a: any, b: any) {
      const dateA = parseDate(a.date);
      const dateB = parseDate(b.date);
      return (dateA > dateB) ? 1 : 0;
      }

      const lessons = this.schedule[0].lessons;
      lessons.sort(orderLessons);
      const orderedLessons = new Map<number, LessonModel>();
      for (let i = 0; i < lessons.length; i++)
      {
        orderedLessons.set(i, lessons[i].lesson);
      }
      return orderedLessons;
    }

}

</script>

<style scoped lang="stylus">
</style>
