<template>
  <div class="solution-container">
    <div v-if="loading || submits.length > 0" class="submit-list-data">
      <cv-structured-list v-if="!loading"
                          class="submit-list">
        <template slot="headings">
          <cv-structured-list-heading>Студент</cv-structured-list-heading>
          <cv-structured-list-heading>Задача</cv-structured-list-heading>
          <cv-structured-list-heading>Статус</cv-structured-list-heading>
        </template>
        <template slot="items">
          <cv-structured-list-item
            v-for="submit in submits"
            :key="submit.id">
            <cv-structured-list-data>
              <div class="user-component-container-main">
                <user-component :user-id="submit.student" class="user-component-container"/>
              </div>
            </cv-structured-list-data>
            <cv-structured-list-data>
              <cv-link :to="linkRoute(submit)">{{ submit.problem.name }}</cv-link>
            </cv-structured-list-data>
            <cv-structured-list-data>
              <submit-status :submit='submit'/>
            </cv-structured-list-data>
          </cv-structured-list-item>
        </template>
      </cv-structured-list>
      <cv-data-table-skeleton v-else :columns="3" :rows="1"/>
    </div>
    <div v-else class="submit-list-empty">
      <div class="submit-list-empty--wrapper">
        <task-icon class="submit-list-empty--icon"/>
        <h4>Ручная проверка не требуется</h4>
        <span>Вы проверили все работы на ручной проверке, или студенты ничего не отправили</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import SubmitStatus from '@/components/SubmitStatus.vue';
import UserComponent from '@/components/UserComponent.vue';
import SubmitModel from "@/models/SubmitModel";
import submitStore from '@/store/modules/submit';

import TaskIcon from '@carbon/icons-vue/es/task/32';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { TaskIcon, UserComponent, SubmitStatus } })
export default class UserSubmitListComponent extends Vue {
  @Prop({ required: true }) courseId!: number;
  submits: Array<SubmitModel> = [];
  loading = true;
  private submitStore = submitStore;

  async created() {
    this.submits = (await this.submitStore.fetchFirstFiveAW(this.courseId));
    this.loading = false;
  }

  linkRoute(data: SubmitModel) {
    const params = {
      courseId: this.$route.params.courseId,
      lessonId: Number(data.lesson).toString(),
      problemId: data.problem.id.toString(),
    };
    return {
      name: 'ProblemViewWithSubmit', params: {
        ...params, submitId: Number(data.id).toString(),
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
  min-height 400px

.user-component-container-main
  height 0
  width 200px

.user-component-container
  position absolute

.submit-list-empty
  color var(--cds-text-01)
  padding var(--cds-spacing-05)
  display flex
  height 400px

  &--wrapper
    align-self center
    width: 300px

  &--icon
    width 100px
    height 100px
    opacity 0.8
</style>
