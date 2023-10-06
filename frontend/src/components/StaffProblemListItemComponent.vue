<template>
  <cv-accordion-item v-if="!loading" class="accordion">
    <template v-slot:title>
      <div class="problem-list-component--header">
        <div class="problem-container">
          <cv-link @click.stop.prevent :to="target(problem)">
            {{ problem.name }}
          </cv-link>
          <div>
            <stats-graph :problem="problem"/>
          </div>
        </div>
        <component
          :is="TrashCan16"
          v-if="isEditing"
          class="icon-trash"
          @click.stop.prevent="showConfirmModal(problem)">
        </component>
      </div>
    </template>
    <template v-slot:content>
      <problem-stats :problem="problem"/>
    </template>
  </cv-accordion-item>
</template>

<script lang="ts" setup>
import ProblemStats from "@/components/ProblemStats.vue";
import SubmitStatus from "@/components/SubmitStatus.vue";
import StatsGraph from "@/components/StatsGraph.vue";
import type { ProblemModel } from "@/models/ProblemModel";
import type { SubmitModel } from "@/models/SubmitModel"
import useUserStore from "@/stores/modules/user";
import TrashCan16 from '@carbon/icons-vue/es/trash-can/16'
import { type PropType, type Ref, ref } from "vue";
import { useRoute } from "vue-router";
import type { CatsProblemModel } from "@/models/CatsProblemModel";

const props = defineProps({
  problem: { type: Object as PropType<ProblemModel>, required: true },
  isEditing: { type: Boolean, required: false }
})

const submit: Ref<SubmitModel | null> = ref(null);
const userStore = useUserStore();
const loading: Ref<boolean> = ref(false);
const route = useRoute();
const emit = defineEmits<{
  (e: 'show-confirm-modal', problem_param: ProblemModel): void
}>()

function target(problem: ProblemModel) {
  if (!!problem.last_submit) {
    return {
      name: 'ProblemViewWithSubmit',
      params: {
        courseId: route.params.courseId,
        lessonId: route.params.lessonId,
        problemId: problem.id.toString(),
        submitId: problem.last_submit.id.toString(),
      },
    };
  } else
    return { name: 'ProblemView', params: { problemId: problem.id.toString() } };
}

function showConfirmModal(problem: ProblemModel) {
  emit('show-confirm-modal', problem);
}
</script>
