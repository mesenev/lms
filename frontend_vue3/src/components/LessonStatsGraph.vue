<template>
  <div>
    <cv-inline-loading v-if="loading" state="loading"></cv-inline-loading>
    <div v-else-if="problems.length">
      <span>Решено задач: {{ solvedProblems }} из {{ problems.length }}</span>
      <div class="stats-graph">
        <span class="stat" v-for="problem in problems"
              :key="problem.id" :style="problemStatStyle(problem.id)"></span>
      </div>
    </div>
    <span v-else>Задачи отсутствуют</span>
  </div>
</template>

<script lang="ts" setup>

import type { PropType, Ref } from "vue";
import type { LessonModel } from "@/models/LessonModel";
import type { UserModel } from "@/models/UserModel";
import useSubmitStore from "@/stores/modules/submit";
import useProblemStore from "@/stores/modules/problem";
import { computed, onMounted, ref } from "vue";
import type { SubmitModel } from "@/models/SubmitModel";
import type { ProblemModel } from "@/models/ProblemModel";

interface StatsGraphStyle {
  backgroundColor: string;
  width: string;
}

const props = defineProps({
  lesson: { type: Object as PropType<LessonModel>, required: true },
  user: { type: Object as PropType<UserModel> }
})

const submitStore = useSubmitStore();
const problemStore = useProblemStore();
const problemsSubmits = ref<Dictionary<SubmitModel[]>>({});
const _problems = ref<ProblemModel[]>([]);
const loading = ref(true);

const problems = computed(() => {
  return _problems.value;
})

const problemsCount = computed((): number => {
  return props.lesson.problems.length;
})

const lessonStats = computed((): Dictionary<string> => {
  const stats: Dictionary<string> = {};
  for (const problem of problems.value) {
    if (problemsSubmits.value[problem.id].filter(x => x.status === 'OK' && x.student === props.user?.id).length)
      stats[problem.id] = 'OK';
    else if (problemsSubmits.value[problem.id].filter(x => (x.status === 'AW' || x.status === 'NP') && x.student === props.user?.id).length)
      stats[problem.id] = 'NP';
    else if (problemsSubmits.value[problem.id].filter(x => x.status === 'WA' && x.student === props.user?.id).length)
      stats[problem.id] = 'WA'
    else
      stats[problem.id] = '';
  }
  return stats;
})

const solvedProblems = computed(() => {
  return Object.values(lessonStats.value).filter(x => x === 'OK').length;
})

const wrongStyle: StatsGraphStyle = {
  backgroundColor: '#fc4848',
  width: `${1 / problemsCount.value * 100}%`,
};
const successfulStyle: StatsGraphStyle = {
  backgroundColor: '#2ff306',
  width: `${1 / problemsCount.value * 100}%`,
};
const testingStyle: StatsGraphStyle = {
  backgroundColor: '#fff300',
  width: `${1 / problemsCount.value * 100}%`,
};
const withoutSolutionStyle: StatsGraphStyle = {
  backgroundColor: 'var(--cds-ui-01)',
  width: `${1 / problemsCount.value * 100}%`,
};

onMounted(async () => {
  _problems.value = await problemStore.fetchProblemsByLessonId(props.lesson.id);
  for (const problem of problems.value) {
    problemsSubmits.value[problem.id] = await submitStore.fetchProblemStats(problem.id);
  }
  loading.value = false;
})

function problemStatStyle(problemId: number) {
  if (lessonStats.value[problemId.toString()] === '')
    return withoutSolutionStyle;
  else if (lessonStats.value[problemId.toString()] === 'OK')
    return successfulStyle;
  else if (lessonStats.value[problemId.toString()] === 'NP')
    return testingStyle;
  else
    return wrongStyle;
}
</script>

<style scoped lang="stylus">
.stats-graph
  margin-right 5px
  width 130px
  height 5px
  display flex
  background-color var(--cds-ui-01)

.stat
  border 0.3px solid var(--cds-ui-05)
</style>
