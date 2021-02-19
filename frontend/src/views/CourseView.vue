<template>
  <div class="bx--grid">
    <div v-if="!loading" class="bx--row header">
      <h1>{{ (course) ? course.name : "" }}</h1>
    </div>
    <div v-else class="bx--row header">
      <cv-skeleton-text :width="'65%'" :heading="true"/>
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
import { Component, Vue } from 'vue-property-decorator';

@Component({ components: { LessonListComponent } })
export default class CourseView extends Vue {
  @Prop({ required: true }) courseId: number;
  courseStore = courseStore;
  lessonStore = lessonStore;
  searchValue = "";

  get loading(): boolean {
    return !Boolean(this.lessons);
  }

  get lessons(): Array<LessonModel> {
    if (!(this.courseId in Object.keys(this.lessonStore.lessonsByCourse)))
      return [];
    return this.lessonStore.lessonsByCourse[courseId];
  }

  get course(): CourseModel | null {
    return this.courseStore.currentCourse;
  }

  async created() {
    await this.lessonStore.fetchLessonsByCourseId(courseId);
  }

  get filterLessons() {
    return this.lessons.filter((l: LessonModel) => {
      return l.name.toLowerCase().includes(this.searchValue.toLowerCase());
    });
  }
}

</script>

<style scoped>
</style>
