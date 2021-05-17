<template>
  <cv-grid>
    <cv-row class="header">
      <cv-column>
        <div class="solution-container--submit-list">
          <cv-structured-list
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
        </div>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<script lang="ts">
import SubmitStatus from '@/components/SubmitStatus.vue';
import { Component, Prop, Vue } from 'vue-property-decorator';
import ProblemModel from "@/models/ProblemModel";
import problemStore from '@/store/modules/problem';
import { Route } from 'vue-router';

@Component({ components: { SubmitStatus } })
export default class UserProblemsListComponent extends Vue {
  @Prop({ required: true }) courseId!: number;

  private problemStore = problemStore;

  problems: Array<ProblemModel> = [];
  loading = true;

  async created() {
    this.problems = await this.problemStore.fetchProblemsForCourse(this.courseId);
    this.loading = false;
  }

  linkRoute(data: ProblemModel): Route {
    const params = {
      courseId: this.$route.params.courseId,
      lessonId: data.lesson,
      problemId: data.id,
    };
    if (!data.last_submit) {
      return {
        name: 'ProblemView', params: { ...params },
      };
    }
    return {
      name: 'ProblemViewWithSubmit', params: {
        ...params, submitId: data.last_submit.id.toString(),
      },
    };
  }
}
</script>

<style lang="stylus" scoped>

.list-header
  font-size 1.1rem
  padding-bottom 1rem

.submit-list
  justify-content center

.table
  width 1rem

.list-item
  border 1px solid rgba(0, 0, 0, .3)

</style>
