<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>{{ (course) ? course.name : "" }}</h1>
    </div>
    <div class=" bx--row">
      <div class="items bx--col-lg-8">
        <cv-search label="label" placeholder="search" v-model.trim="searchValue"/>
        <cv-structured-list selectable>
          <template slot="items">
            <cv-structured-list-item
              class="item"
              v-for="lesson in filterLessons"
              :key="lesson.id">
              <lesson :lesson-prop='lesson'/>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
      </div>
      <div class="bx--col-lg-8">
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

@Component({
  components: { Lesson },
})
export default class CourseView extends Vue {
  @Prop({required: true}) courseId!: number;

  @Prop({required: false, default: null}) courseProp!: CourseModel | null;
  course: CourseModel| null = null;
  courseStore = courseStore;
  lessonStore = lessonStore;
  loading = true;

  searchValue = "";
  async created() {
    if(this.courseProp === null){
      this.course = await this.courseStore.fetchCourseById(this.courseId);
    }
    this.loading = false;
  }
  get lessons(): Array<LessonModel> {
    return(this.course) ?  this.course.lessons : [];
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
