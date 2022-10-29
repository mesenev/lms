<template>
  <cv-accordion-item v-if="!loading" class="accordion">
    <template slot="title">
      <div class="problem-list-component--header">
        <cv-link :to="target(problem)">
          <Launch/>
        </cv-link>
        {{ problem.name }}
        <div>
          <stats-graph v-if="problem.stats" :stats="problem.stats"/>
        </div>
      </div>
    </template>
    <template slot="content">
      <problem-stats :problem="problem"/>
    </template>
  </cv-accordion-item>
</template>

<script lang="ts">
import {Component, Prop, Vue} from "vue-property-decorator";
import ProblemStats from "@/components/ProblemStats.vue";
import SubmitStatus from "@/components/SubmitStatus.vue";
import Launch from "@carbon/icons-vue/es/launch/16";
import StatsGraph from "@/components/StatsGraph.vue";
import ProblemModel from "@/models/ProblemModel";
import SubmitModel from "@/models/SubmitModel"
import userStore from "@/store/modules/user";

@Component({components: { ProblemStats, SubmitStatus, Launch, StatsGraph } })
export default class StaffProblemListItemComponent extends Vue {
  @Prop({ required: true }) problem!: ProblemModel;
  submit: SubmitModel | null = null;
  userStore = userStore;
  loading = false;


  target(problem: ProblemModel) {
    if (!!problem.last_submit) {
      return {
        name: 'ProblemViewWithSubmit',
        params: {
          courseId: this.$route.params.courseId,
          lessonId: this.$route.params.lessonId,
          problemId: problem.id.toString(),
          submitId: problem.last_submit.id.toString(),
        },
      };
    } else
      return {name: 'ProblemView', params: {problemId: problem.id.toString()}};
  }
}
</script>
