<template>
  <router-view v-slot="{Component}" :key="route.params.problemId" :submitId="route.params.submitId">
    <transition v-if="problem" mode="out-in" name="fade">
      <component :is="Component"/>
    </transition>
    <div v-else class="loading-container">
      <cv-loading class="loading-out"/>
    </div>
  </router-view>
</template>

<script lang="ts" setup>
import type { ProblemModel } from '@/models/ProblemModel';
import useProblemStore from '@/stores/modules/problem';
import useSubmitStore from '@/stores/modules/submit';
import type { SubmitModel } from "@/models/SubmitModel";
import { ref, onMounted } from 'vue';
import { useRoute } from "vue-router";

const props = defineProps({ problemId: {type: String, required: true} })
const problemStore = useProblemStore();
const submitStore = useSubmitStore();
const route = useRoute()
const problem = ref<ProblemModel | null>(null);

onMounted( async () => {
    problemStore.changeCurrentProblem(null);
    problem.value = await problemStore.fetchProblemById(parseInt(props.problemId));
    problemStore.changeCurrentProblem(problem.value);
    submitStore.setSubmits(problemStore.currentProblem?.submits as SubmitModel[]);
  })
</script>

<style lang="stylus" scoped>
.loading-out
  display flex
  width 100%;
  height 100%;
  align-items center;
  justify-content center;

</style>
