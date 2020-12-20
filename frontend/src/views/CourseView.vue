<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>{{this.store.getCourse.name}}</h1>
      <!-- TODO: take the name of open course -->
    </div>
    <div class=" bx--row">
      <div class="items bx--col-lg-8">
        <cv-search
          label="label"
          placeholder="search"
        >
        </cv-search>
        <cv-structured-list selectable>
          <template slot="items">
            <cv-structured-list-item class="item" v-for="less in lessons" :key="less.id">
              <Lesson :lesson-prop='less'/>
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
import { Component, Vue, Prop } from 'vue-property-decorator';
import CourseModel from '@/models/CourseModel';
import LessonModel from "@/models/LessonModel";
import {mainStore} from "@/store";
import Lesson from "@/components/Lesson.vue";
@Component({
  components: {Lesson}
})
export default class CourseView extends Vue {
  private store = mainStore;
  @Prop() courseId!: number;

  @Prop() courseProp!: CourseModel;

  get lessons(): Array<LessonModel> {
    return this.store.getLessons;
  }
}

</script>

<style scoped>
</style>
