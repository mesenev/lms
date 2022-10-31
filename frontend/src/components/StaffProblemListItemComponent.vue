<template>
  <cv-accordion-item v-if="!loading" class="accordion">
    <template slot="title">
      <div class="problem-list-component--header">
        <div class="problem-container">
          <cv-link :to="target(problem)">
            {{ problem.name }}
          </cv-link>
          <div>
            <stats-graph v-if="problem.stats" :stats="problem.stats"/>
          </div>
        </div>
        <component
          v-if="isEditing"
          :is="TrashCan16"
          class="icon-trash"
          @click.stop.prevent="deleteProblemClick(problem.id)">
        </component>
      </div>
    </template>
    <template slot="content">
      <problem-stats :problem="problem"/>
    </template>
  </cv-accordion-item>
</template>

<script lang="ts">
import { Component, Prop } from "vue-property-decorator";
import ProblemStats from "@/components/ProblemStats.vue";
import SubmitStatus from "@/components/SubmitStatus.vue";
import Launch from "@carbon/icons-vue/es/launch/16";
import StatsGraph from "@/components/StatsGraph.vue";
import ProblemModel from "@/models/ProblemModel";
import SubmitModel from "@/models/SubmitModel"
import userStore from "@/store/modules/user";
import TrashCan16 from '@carbon/icons-vue/es/trash-can/16'
import { Vue } from 'vue-property-decorator'

@Component({ components: { ProblemStats, SubmitStatus, Launch, StatsGraph } })
export default class StaffProblemListItemComponent extends Vue {
  @Prop({ required: true }) problem!: ProblemModel;
  @Prop({ required: false }) isEditing!: false | boolean;
  submit: SubmitModel | null = null;
  userStore = userStore;
  TrashCan16 = TrashCan16;
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
      return { name: 'ProblemView', params: { problemId: problem.id.toString()} };
  }
  deleteProblemClick(problemId: number) {
    this.$emit('delete-problem-click', problemId);
  }
}
</script>
