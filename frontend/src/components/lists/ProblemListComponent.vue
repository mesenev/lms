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
                  <submit-status v-if="!!problem.last_submit" :submit="problem.last_submit"/>
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

  target(problem: ProblemModel) {
    if (!!problem.last_submit)
      return {
        name: 'ProblemViewWithSubmit', params: {
          courseId: this.$route.params.courseId,
          lessonId: this.$route.params.lessonId,
          problemId: problem.id.toString(),
          submitId: problem.last_submit.id.toString(),
        }
      };
    else
      return { name: 'ProblemView', params: { problemId: problem.id.toString() } };
  }

  created() {
    this.$on('cv:change', this.eventHandler);
  }

  deleteProblem(problemId: number) {
    api.delete(`/api/problem/${problemId}/`).then(response => {
      this.$emit('update-problem-delete', problemId);
    }).catch(error => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    })
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  eventHandler(_event: object) {
    this.open = true;
  }

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
