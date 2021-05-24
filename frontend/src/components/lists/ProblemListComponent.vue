<template xmlns:cv-tag="http://www.w3.org/1999/html">
  <cv-accordion-item class="accordion" :class="{ doNotShowAccordionContent: !isStaff }">
    <template slot="title">
      <div class="problem-list-component--header">
        <cv-link :to="target">
          <Launch/>
        </cv-link>
        {{ problem.name }}
        <div class="tags" v-if="!isStaff">
          <submit-status v-if="!!lastSubmit" :submit="lastSubmit"/>
          <cv-tag v-else kind="red" label="Не сдано"/>
        </div>
        <div v-else>
          <stats-graph v-if="problem.stats" :stats="problem.stats"/>
        </div>
      </div>
    </template>
    <template slot="content">
      <problem-stats v-if="isStaff && open" :problem="problem"/>
    </template>
  </cv-accordion-item>
</template>

<script lang="ts">
import ProblemStats from '@/components/ProblemStats.vue';
import StatsGraph from '@/components/StatsGraph.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import ProblemModel from '@/models/ProblemModel';
import SubmitModel from "@/models/SubmitModel";
import Launch from '@carbon/icons-vue/es/launch/16';

import userStore from '@/store/modules/user';
import courseStore from '@/store/modules/course';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { ProblemStats, SubmitStatus, Launch, StatsGraph } })
export default class ProblemListComponent extends Vue {
  @Prop() problemProp!: ProblemModel;
  @Prop() isOpen!: boolean;

  userStore = userStore;
  courseStore = courseStore;

  get open() {
    return this.isOpen;
  }

  get lastSubmit(): SubmitModel | null {
    return null;
  }

  get target() {
    return { name: 'ProblemView', params: { problemId: this.problem.id.toString() } };
  }

  get problem() {
    return this.problemProp;
  }

  created() {
    this.$on('cv:change', this.eventHandler);
  }

  eventHandler(event: object) {
    this.isOpen = !this.isOpen;
  }

  get isStaff(): boolean {
    const courseId = Number(this.$route.params.courseId);
    return this.userStore.user.staff_for.includes(courseId);
  }
}
</script>
<style scoped lang="stylus">
.aw
  text-align right

.accordion /deep/ .bx--accordion__content
  padding-right 0


</style>
