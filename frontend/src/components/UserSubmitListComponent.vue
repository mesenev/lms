<template>
  <cv-grid>
    <cv-row class="header">
      <cv-column>
        <div class="solution-container--submit-list">
          <cv-structured-list
            class="submit-list">
            <template slot="headings">
              <cv-structured-list-heading>Студент</cv-structured-list-heading>
              <cv-structured-list-heading>Задача</cv-structured-list-heading>
              <cv-structured-list-heading>Статус</cv-structured-list-heading>
            </template>
            <template slot="items">
              <cv-structured-list-item v-if="loading">
                <cv-skeleton-text/>
              </cv-structured-list-item>
              <cv-structured-list-item v-for="submit in submits"
                                       v-else-if="submits.length > 0" :key="submit.id">
                <cv-structured-list-data>
                  <user-component :user-id="submit.student"/>
                </cv-structured-list-data>
                <cv-structured-list-data>
                  <cv-link :to="linkRoute(submit)">{{ submit.problem.name }}</cv-link>
                </cv-structured-list-data>
                <cv-structured-list-data>
                  <submit-status :submit='submit'/>
                </cv-structured-list-data>
              </cv-structured-list-item>
              <div v-else>
                <span>Отправки отсутствуют</span>
              </div>
            </template>
          </cv-structured-list>
        </div>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<script lang="ts">
import SubmitStatus from '@/components/SubmitStatus.vue';
import UserComponent from '@/components/UserComponent.vue';
import SubmitModel from "@/models/SubmitModel";
import submitStore from '@/store/modules/submit';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { UserComponent, SubmitStatus } })
export default class UserSubmitListComponent extends Vue {
  @Prop({ required: true }) courseId!: number;
  submits: Array<SubmitModel> = [];
  loading = true;
  private submitStore = submitStore;

  async created() {
    this.submits = (await this.submitStore.fetchSubmitsByCourse({
      course_id: this.courseId,
      page: 1,
      page_size: 5,
      status: 'AW',
    })).results;
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
