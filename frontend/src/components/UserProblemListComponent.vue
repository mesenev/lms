<template>
  <div class="solution-container">
    <div v-if="loading || problems.length > 0" class="submit-list-data">
      <cv-structured-list
        v-if="!loading"
        class="submit-list">
        <template slot="headings">
          <cv-structured-list-heading>Задача</cv-structured-list-heading>
          <cv-structured-list-heading>Статус</cv-structured-list-heading>
        </template>
        <template v-if="problems" slot="items">
          <cv-structured-list-item v-for="problem in problems" :key="problem.id">
            <cv-structured-list-data>
              <cv-link :to="linkRoute(problem)">{{ problem.name }}</cv-link>
            </cv-structured-list-data>
            <cv-structured-list-data>
              <submit-status v-if='problem.last_submit' :submit='problem.last_submit'/>
              <div v-else style="background-color: gray; width: 1em; height: 1em; border-radius: 1em"/>
            </cv-structured-list-data>
          </cv-structured-list-item>
        </template>
        <template v-else>
          <cv-structured-list-item>
            <cv-skeleton-text/>
          </cv-structured-list-item>
        </template>
      </cv-structured-list>

      <cv-data-table-skeleton v-else :columns="2" :rows="1"/>
    </div>
    <div v-else class="submit-list-empty">
      <div class="submit-list-empty--wrapper">
        <task-icon class="submit-list-empty--icon"/>
        <h4>Задач к решению нет</h4>
        <span>Все доступные задачи решены 👍</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import SubmitStatus from '@/components/SubmitStatus.vue';
import ProblemModel from "@/models/ProblemModel";
import problemStore from '@/store/modules/problem';
import TaskIcon from '@carbon/icons-vue/es/task/32';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { TaskIcon, SubmitStatus } })
export default class UserProblemListComponent extends Vue {
  @Prop({ required: true }) courseId!: number;

  private problemStore = problemStore;

  problems: Array<ProblemModel> = [];
  loading = true;

  async created() {
    this.problems = await this.problemStore.fetchProblemsForCourse(this.courseId);
    this.loading = false;
    this.problems = [];
  }

  linkRoute(data: ProblemModel) {
    const params = {
      courseId: this.$route.params.courseId,
      lessonId: Number(data.lesson).toString(),
      problemId: data.id.toString(),
    };
    if (!data.last_submit) {
      return {
        name: 'ProblemView', params: { ...params },
      };
    }
    return {
      name: 'ProblemViewWithSubmit', params: {
        ...params, submitId: Number(data.last_submit.id).toString(),
      },
    };
  }
}
</script>


<style lang="stylus" scoped>

.submit-list-data
  background-color var(--cds-ui-background)
  padding var(--cds-spacing-05)
  width 100%
  min-height 300px

.user-component-container-main
  height 0
  width 200px

.user-component-container
  position absolute

.submit-list-empty
  background-color var(--cds-ui-background)
  padding var(--cds-spacing-05)
  display flex
  height 300px

  &--wrapper
    align-self center
    width: 300px

  &--icon
    width 100px
    height 100px
    opacity 0.8
</style>

