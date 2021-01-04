<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>{{ this.store.getCourse.name }}</h1>
      <!-- TODO: take the name of open course -->
    </div>
    <div class=" bx--row">
      <div class="items bx--col-lg-8">
        <cv-search
          label="label"
          placeholder="search"
          v-model.trim="searchValue"
        >
        </cv-search>
        <cv-structured-list selectable>
          <template slot="items">
            <cv-structured-list-item class="item" v-for="less in filterLessons" :key="less.id">
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
import Lesson from "@/components/Lesson.vue";
import CourseModel from '@/models/CourseModel';
import LessonModel from "@/models/LessonModel";
import { modBStore } from "@/store";
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({
  components: { Lesson },
})
export default class CourseView extends Vue {
  private store = modBStore;
  @Prop() courseId!: number;

  @Prop() courseProp!: CourseModel;

  searchValue = "";

  get lessons(): Array<LessonModel> {
    return this.store.getLessons;
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
