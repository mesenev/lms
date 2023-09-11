<template>
  <transition mode="out-in" name="fade">
    <router-view v-if="problem" :key="route.params.problemId"/>
    <div v-else class="loading-out">
      <cv-loading />
    </div>
  </transition>
</template>

<script lang="ts" setup>
import ProblemModel from '@/models/ProblemModel';
import useProblemStore from '@/stores/modules/problem';
import useSubmitStore from '@/stores/modules/submit';
import SubmitModel from "@/models/SubmitModel";
import { Ref, ref, onMounted } from 'vue';
import { useRoute } from "vue-router";

const props = defineProps({ problemId: {type: Number, required: true} })
const problemStore = useProblemStore();
const submitStore = useSubmitStore();
const route = useRoute()
const problem: Ref<ProblemModel> | Ref<null> = ref(null);

onMounted( async () => {
    problemStore.changeCurrentProblem(null);
    problem.value = await problemStore.fetchProblemById(props.problemId);
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
