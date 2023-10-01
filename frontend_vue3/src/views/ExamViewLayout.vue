<template>
  <router-view v-slot="{Component}">
    <transition v-if="exam" mode="out-in" name="fade">
      <component :is="Component"/>
    </transition>
    <div v-else class="loading-container">
      <cv-loading/>
    </div>
  </router-view>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import useExamStore from "@/stores/modules/exam";
import type { ExamModel } from "@/models/ExamModel";
import useSolutionStore from "@/stores/modules/solution";

const props = defineProps({
  examId: { type: String, required: true }
})

const exam = ref<ExamModel | null>(null);
const examStore = useExamStore();
const solutionStore = useSolutionStore();

onMounted(async () => {
  examStore.changeCurrentExam(null);
  exam.value = await examStore.fetchExamById(parseInt(props.examId));
  examStore.changeCurrentExam(exam.value);
  await examStore.fetchExamsByLessonId(exam.value.lesson);
  solutionStore.setSolutions(await solutionStore.fetchSolutionsByExam(parseInt(props.examId)));
})
</script>

<style scoped>

</style>
