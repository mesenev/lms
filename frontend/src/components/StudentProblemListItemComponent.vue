<template>
  <div v-if="!loading" class="problem-list-item">
    <router-link class="list-element" :to="target()">
      <div class="problem-list-component--header">
        <h5 class="problem--title">{{ problem.name }}</h5>
        <div class="tags">
          <submit-status v-if="!!submit.status" :submit="submit"/>
          <cv-tag v-else kind="red" label="Не сдано"/>
        </div>
      </div>
    </router-link>
  </div>
  <cv-skeleton-text v-else></cv-skeleton-text>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import SubmitStatus from "@/components/SubmitStatus.vue";
import ProblemModel from "@/models/ProblemModel";
import SubmitModel from "@/models/SubmitModel";
import CatsProblemModel from "@/models/CatsProblemModel";
import submitStore from "@/store/modules/submit";
import userStore from "@/store/modules/user";


@Component({ components: { SubmitStatus } })
export default class StudentProblemListItemComponent extends Vue {
  @Prop({ required: true }) problem!: ProblemModel | CatsProblemModel;
  submitStore = submitStore;
  userStore = userStore;
  loading = true;
  submit: SubmitModel | null = null;

  async created() {
    await this.submitStore.fetchLastSubmit({
      user_id: this.userStore.user.id,
      problem_id: this.problem.id
    })
      .then((data: SubmitModel | null) => this.submit = data)
      .catch((error: string) => console.log(error));
    this.loading = false;
  }

  target() {
    if (!!this.submit?.status) {
      return {
        name: 'ProblemViewWithSubmit',
        params: {
          courseId: this.$route.params.courseId,
          lessonId: this.$route.params.lessonId,
          problemId: this.problem.id.toString(),
          submitId: this.submit.id.toString(),
        }
      };
    } else {
      return {
        name: 'ProblemView', params: {
          courseId: this.$route.params.courseId,
          lessonId: this.$route.params.lessonId,
          problemId: this.problem.id.toString(),
        }
      };
    }
  }

}
</script>
