<template>
  <div v-if="!isStaff">
    <cv-structured-list>
      <template slot="items">
        <cv-structured-list-item
          v-for="problem in taskList"
          :key="problem.id">
          <student-problem-list-item-component
            :problem="problem"></student-problem-list-item-component>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
  <div v-else>
    <cv-inline-notification
      v-if="showNotification"
      @close="() => showNotification=false"
      kind="error"
      :sub-title="notificationText"/>
    <cv-accordion
      v-for="problem in taskList"
      :key="problem.id"
      align="end">
      <cv-accordion-item class="accordion" :class="{ doNotShowAccordionContent: !isStaff }">
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
              @click.stop.prevent="deleteProblem(problem.id)">
            </component>
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
import Launch from '@carbon/icons-vue/es/launch/16';

import TrashCan16 from '@carbon/icons-vue/es/trash-can/16'
import userStore from '@/store/modules/user';
import courseStore from '@/store/modules/course';
import { Component, Prop, Vue } from 'vue-property-decorator';
import CatsProblemModel from "@/models/CatsProblemModel";
import StudentProblemListItemComponent from "@/components/StudentProblemListItemComponent.vue";
import StaffProblemListItemComponent from "@/components/StaffProblemListItemComponent.vue";
import api from "@/store/services/api";
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";

@Component({ components: { ProblemStats, SubmitStatus, Launch, StatsGraph } })
export default class ProblemListComponent extends NotificationMixinComponent {
  @Prop({required: true}) taskList!: Array<ProblemModel | CatsProblemModel>;
  @Prop({required: false}) isEditing!: false | boolean;
  public open = true; /*false?*/
  userStore = userStore;
  courseStore = courseStore;
  TrashCan16 = TrashCan16;


  get isStaff(): boolean {
    const courseId = Number(this.$route.params.courseId);
    return this.userStore.user.staff_for.includes(courseId);
  }
}
</script>
<style scoped lang="stylus">
.problem-list-component--header
  display flex
  align-items center
  justify-content space-between

.icon-trash
  margin-right 2rem

.aw
  text-align right

.accordion /deep/ .bx--accordion__content
  padding-right 0
</style>
