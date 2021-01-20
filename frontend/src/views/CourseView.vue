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
      <div class="bx--col-lg-8 link">
        <cv-number-input
          :light="light"
          :label="'Выберите количество учеников курса'"
          :value="value"
          :min="1"
          :step="1">
        </cv-number-input>
        <br>
        <GenerateLinks>
            Сгенерировать ссылку-приглашение
        </GenerateLinks>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Lesson from "@/components/Lesson.vue";
import CourseModel from '@/models/CourseModel';
import LessonModel from "@/models/LessonModel";
import { courseStore, lessonStore } from '@/store';
import { Component, Prop, Vue } from 'vue-property-decorator';
import GenerateLinks from "@/components/EditCourse/GenerateLinks.vue";

@Component({
  components: {GenerateLinks, Lesson },
})
export default class CourseView extends Vue {
  @Prop({ required: true }) courseId!: number;

  course: CourseModel | null = null;
  courseStore = courseStore;
  lessonStore = lessonStore;
  loading = true;

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
      return l.name.toLowerCase().includes(this.searchValue.toLowerCase())
    })
  }
}

</script>

<style scoped>
</style>
