<template>
  <div v-if="!isStaff"> <!--Разные отображения списка задач, для стафа и студентов-->
    <cv-structured-list>
      <template slot="items">
        <cv-structured-list-item
          v-for="problem in taskList"
          :key="problem.id">
          <div class="problem-list-item">
            <router-link class="list-element" :to="target(problem)">
              <div class="problem-list-component--header">
                <h5 class="problem--title">{{ problem.name }}</h5>
                <div class="tags">
                  <submit-status v-if="!!lastSubmit" :submit="lastSubmit"/>
                  <cv-tag v-else kind="red" label="Не сдано"/>
                </div>
              </div>
            </router-link>
          </div>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
  <div v-else>
    <cv-accordion
      v-for="problem in taskList"
      :key="problem.id"
      align="end">
      <cv-accordion-item class="accordion" :class="{ doNotShowAccordionContent: !isStaff }">
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
          <problem-stats v-if="isStaff && open" :problem="problem"/>
        </template>
      </cv-accordion-item>
    </cv-accordion>
  </div>
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
  @Prop({required: true}) taskList!: Array<ProblemModel>;
  public open = true; /*false?*/
  userStore = userStore;
  courseStore = courseStore;

  target(problem: ProblemModel) {
    return { name: 'ProblemView', params: { problemId: problem.id.toString() } };
  }


  created() {
    this.$on('cv:change', this.eventHandler);
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  eventHandler(_event: object) {
    this.open = true;
  }

  get lastSubmit(): SubmitModel | null {
    return null;
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
