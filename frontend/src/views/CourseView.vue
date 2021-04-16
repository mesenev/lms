<template>
  <div class="bx--grid">
    <div v-if="!loading" class="bx--row header">
      <h1 class="course-title">Курс: {{ (course) ? course.name : "" }}</h1>
    </div>
    <div v-else class="bx--row header">
      <cv-skeleton-text :width="'65%'" :heading="true"/>
    </div>
    <div class="description--container">
        <span v-if="!loading">
          {{ course.description }}
        </span>
      <cv-skeleton-text v-else width="'35%'"/>
    </div>
    <div class=" bx--row">
      <div class="items bx--col-lg-8">
        <cv-search label="label" placeholder="search" v-model.trim="searchValue"/>
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
    </div>
  </div>

</template>


<script lang="ts">
import LessonListComponent from "@/components/lists/LessonListComponent.vue";
import CourseModel from '@/models/CourseModel';
import LessonModel from "@/models/LessonModel";
import courseStore from "@/store/modules/course";
import lessonStore from "@/store/modules/lesson";
import {Component, Prop, Vue} from 'vue-property-decorator';

@Component({components: {LessonListComponent}})
export default class CourseView extends Vue {
  @Prop({required: true}) courseId!: number;
  courseStore = courseStore;
  lessonStore = lessonStore;
  searchValue = "";
  loading = true;

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
.description--container
  margin-left 2.5rem
  padding-bottom 2rem

.course-title
  margin-left 3rem

</style>
