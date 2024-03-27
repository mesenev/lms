<template>
  <div class="solution-container">
    <div v-if="loading || problems.length > 0" class="submit-list-data">
      <cv-structured-list
          v-if="!loading"
          class="submit-list">
        <template v-slot:headings>
          <cv-structured-list-heading>Задача</cv-structured-list-heading>
          <cv-structured-list-heading>Статус</cv-structured-list-heading>
        </template>
        <template v-if="problems" v-slot:items>
          <cv-structured-list-item v-for="problem in problems" :key="problem.id">
            <cv-structured-list-data>
              <cv-link :to="linkRoute(problem)">{{ problem.name }}</cv-link>
            </cv-structured-list-data>
            <cv-structured-list-data>
              <submit-status v-if='problem.last_submit' :submit='problem.last_submit'/>
              <div class="else--bordered" v-else/>
            </cv-structured-list-data>
          </cv-structured-list-item>
        </template>
        <template v-if="!problems">
          <cv-structured-list-item>
            <cv-skeleton-text/>
          </cv-structured-list-item>
        </template>
      </cv-structured-list>
      <cv-data-table-skeleton v-else :columns="2" :rows="1"/>
    </div>
    <div v-else class="submit-list-empty">
      <div class="submit-list-empty--wrapper">
        <task-icon class="submit-list-empty--icon"/>
        <h4>Задач к решению нет</h4>
        <span>Все доступные задачи решены 👍</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import SubmitStatus from '@/components/SubmitStatus.vue';
import type { ProblemModel } from "@/models/ProblemModel";
import useProblemStore from '@/stores/modules/problem';
import TaskIcon from '@carbon/icons-vue/es/task/32';
import { type Ref, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps({
  courseId: { type: Number, required: true }
})

const problemStore = useProblemStore();
const route = useRoute();

const problems: Ref<Array<ProblemModel>> = ref([]);
const loading: Ref<boolean> = ref(true);

onMounted(async () => {
  problems.value = await problemStore.fetchProblemsForCourse(props.courseId);
  loading.value = false;
})

function linkRoute(data: ProblemModel) {
  const params = {
    courseId: route.params.courseId,
    lessonId: Number(data.lesson).toString(),
    problemId: data.id.toString(),
  };
  if (!data.last_submit) {
    return {
      name: 'ProblemView', params: { ...params },
    };
  }
  return {
    name: 'ProblemViewWithSubmit', params: {
      ...params, submitId: Number(data.last_submit.id).toString(),
    },
  };
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
  background-color var(--cds-ui-background)
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

.else--bordered
  background-color gray
  width 1em
  height 1em
  border-radius 1em
</style>

