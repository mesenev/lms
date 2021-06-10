<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1 v-if="!loading" class="course-title">Курс: {{ (course) ? course.name : "" }}</h1>
      <cv-skeleton-text v-else :heading="true" :width="'65%'"/>
    </div>
    <div class="description--container">
      <span v-if="!loading"> {{ (course) ? course.description : "" }} </span>
      <cv-skeleton-text v-else width="'35%'"/>
    </div>
    <div class=" bx--row">
      <div class="courses bx--col-lg-6">
        <h4 class="lessons-title">Уроки</h4>
        <cv-search
          v-model.trim="searchValue"
          class="search"
          label="label"
          placeholder="search"
          size="size"/>
        <cv-data-table-skeleton v-if="loading" :columns="1" :rows="6"/>
        <cv-structured-list v-else>
          <template slot="items">
            <cv-structured-list-item
              class="item"
              v-for="lesson in filterLessons"
              :key="lesson.id">
              <lesson-list-component :lesson-prop='lesson'/>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
      </div>
      <div class="submits bx--col-lg-4">
        <user-problems-list-component v-if="!isStaff" :course-id="course.id"/>
        <user-submits-list-component v-else :course-id="course.id"/>
      </div>
    </div>
  </div>

</template>


<script lang="ts">
import LessonListComponent from "@/components/lists/LessonListComponent.vue";
import UserComponent from '@/components/UserComponent.vue';
import UserProblemsListComponent from "@/components/UserProblemsListComponent.vue"
import CourseModel from '@/models/CourseModel';
import LessonModel from "@/models/LessonModel";
import courseStore from "@/store/modules/course";
import lessonStore from "@/store/modules/lesson";
import userStore from '@/store/modules/user';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({
  components: {
    UserProblemsListComponent, LessonListComponent, UserComponent,
  },
})
export default class CourseView extends Vue {
  @Prop({ required: true }) courseId!: number;
  courseStore = courseStore;
  lessonStore = lessonStore;
  searchValue = "";
  loading = true;
  private userStore = userStore;
  private user = this.userStore.user;

  get isStaff(): boolean {
    return this.user.staff_for.includes(Number(this.courseId));
  }

  get lessons(): Array<LessonModel> {
    if (!(this.courseId in this.lessonStore.lessonsByCourse)) {
      return [];
    }

    return this.lessonStore.lessonsByCourse[this.courseId];
  }

  async created() {
    await this.lessonStore.fetchLessonsByCourseId(this.courseId);
    this.loading = false;
  }

  get course(): CourseModel | null {
    return this.courseStore.currentCourse;
  }


  get filterLessons() {
    return this.lessons.filter((l: LessonModel) => {
      return l.name.toLowerCase().includes(this.searchValue.toLowerCase());
    });
  }
}

</script>

<style scoped lang="stylus">

.submits-title
  margin-left 1rem
  margin-top 1rem
  padding 0

.lessons-title
  margin-left 2rem
  margin-top 1rem
  padding 0

.description--container
  margin-left 2.5rem
  padding-bottom 2rem

.submits
  margin-left 1rem
  background-color var(--cds-ui-02)

.courses
  background-color var(--cds-ui-02)

.course-title
  margin-left 3rem

</style>
