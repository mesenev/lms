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
    return this.lessons.filter((l: LessonModel) => {
      return l.name.toLowerCase().includes(this.searchValue.toLowerCase());
    });
  }
}

</script>
