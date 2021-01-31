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
        <cv-structured-list v-if="!loading" selectable>
          <template slot="items">
            <cv-structured-list-item
              class="item"
              v-for="lesson in filterLessons"
              :key="lesson.id">
              <lesson :lesson-prop='lesson'/>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
        <cv-data-table-skeleton v-else :rows="6" :columns="1"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Lesson from "@/components/lists/LessonListComponent.vue";
import CourseModel from '@/models/CourseModel';
import LessonModel from "@/models/LessonModel";
import courseStore from "@/store/modules/course";
import lessonStore from "@/store/modules/lesson";
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { Lesson } })
export default class CourseView extends Vue {
  @Prop({ required: true }) courseId!: number;

  course: CourseModel | null = null;
  courseStore = courseStore;
  lessonStore = lessonStore;
  loading = true;
  usagesAmount = 0;

  searchValue = "";

  async created() {
    this.course = await this.courseStore.fetchCourseById(this.courseId);
    this.loading = false;
  }

  get lessons(): Array<LessonModel> {
    return (this.course) ? this.course.lessons : [];
  }

  get filterLessons() {
    return this.lessons.filter(l => {
      return l.name?.toLowerCase().includes(this.searchValue.toLowerCase())
    })
  }
}

</script>

<style scoped>
</style>
