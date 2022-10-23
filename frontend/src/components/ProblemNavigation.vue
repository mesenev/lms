<template>
  <aside>
    <nav>
      <ul>
        <li class="navigation-title" v-if="classwork.length > 0">
          <span title="Классная работа">CW</span>
          <ul v-if="!loading">
            <problem-navigation-item :problem="problem" v-for="problem in classwork" :key="problem.id"/>
          </ul>
          <ul v-else>
            <cv-tag-skeleton/>
          </ul>
        </li>
        <li class="navigation-title" v-if="homework.length > 0">
          <span title="Домашняя работа">HW</span>
          <ul v-if="!loading">
            <problem-navigation-item :problem="problem" v-for="problem in homework" :key="problem.id"/>
          </ul>
          <ul v-else>
            <cv-tag-skeleton/>
          </ul>
        </li>
        <li class="navigation-title" v-if="extrawork.length > 0">
          <span title="Дополнительные задания" >EX</span>
          <ul v-if="!loading">
            <problem-navigation-item :problem="problem" v-for="problem in extrawork" :key="problem.id"/>
          </ul>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script lang="ts">
import problemStore from '@/store/modules/problem';
import ProblemNavigationItem from '@/components/ProblemNavigationItem.vue';
import { Component, Prop, Vue } from 'vue-property-decorator';
import ProblemModel from "@/models/ProblemModel";


@Component({ components: {ProblemNavigationItem} })
export default class ProblemNavigation extends Vue {
  @Prop({ required: true }) lessonId!: number;
  problemStore = problemStore;
  problems: Array<ProblemModel> = [];
  loading = true;

  target(pid: number) {
    return { name: 'ProblemView', params: { problemId: pid.toString() } };
  }

  get isProblemsEmpty() {
    if (this.problems.length === 0) {
      return true;
    }
  }

  get classwork(): Array<ProblemModel> {
    return this.problems.filter(x => x.type === 'CW');
  }

  get homework(): Array<ProblemModel> {
    return this.problems.filter(x => x.type === 'HW');
  }

  get extrawork(): Array<ProblemModel> {
    return this.problems.filter(x => x.type === 'EX');
  }


  async created() {
    this.problems = await this.problemStore.fetchProblemsByLessonId(this.lessonId);
    this.loading = false;
    console.log(this.problems);
  }
}
</script>


<style lang="stylus" scoped>
aside
  position absolute
  padding-left 1rem
.navigation-title
  margin-top 0.5rem

  span
    border-radius 50px
    text-align center
    width 32px
    height 32px
    line-height 32px
    margin-bottom 1rem

.navigation-title
  height auto

  span
    color white
    background-color #808080
    display block
    cursor default
</style>

<style lang="stylus" scoped>
.bx--structured-list-row--header-row
  background-color #393939
  .pupil-title
    color white
</style>
