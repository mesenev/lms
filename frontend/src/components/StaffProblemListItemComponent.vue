<template>
  <cv-accordion-item v-if="!loading" class="accordion">
    <template slot="title">
      <div class="problem-list-component--header">
        <div class="problem-container">
          <cv-link :to="target(problem)">
            {{ problem.name }}
          </cv-link>
          <div>
            <stats-graph :problem="problem"/>
          </div>
        </div>
        <component
          :is="TrashCan16"
          v-if="isEditing"
          class="icon-trash"
          @click.stop.prevent="showConfirmModal(problem)">
        </component>
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
import StatsGraph from "@/components/StatsGraph.vue";
import ProblemModel from "@/models/ProblemModel";
import SubmitModel from "@/models/SubmitModel"
import userStore from "@/store/modules/user";
import TrashCan16 from '@carbon/icons-vue/es/trash-can/16'

@Component({components: {ProblemStats, SubmitStatus, StatsGraph}})
export default class StaffProblemListItemComponent extends Vue {
  @Prop({required: true}) problem!: ProblemModel;
  @Prop({required: false}) isEditing!: false | boolean;
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
      return {name: 'ProblemView', params: {problemId: problem.id.toString()}};
  }

  showConfirmModal(problem: ProblemModel) {
    this.$emit('show-confirm-modal', problem);
  }
}
</script>
