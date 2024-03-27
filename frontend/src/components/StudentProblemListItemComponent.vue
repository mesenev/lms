<template>
  <div v-if="!loading" class="problem-list-item">
    <router-link class="list-element" :to="target()">
      <div class="problem-list-component--header">
        <h5 class="problem--title">{{ problem.name }}</h5>
        <div class="tags">
          <submit-status v-if="submit && !!submit.status" :submit="submit"/>
          <cv-tag v-else kind="red" label="Не сдано"/>
        </div>
      </div>
    </router-link>
  </div>
  <cv-skeleton-text v-else></cv-skeleton-text>
</template>

<script lang="ts" setup>
import SubmitStatus from "@/components/SubmitStatus.vue";
import type {ProblemModel} from "@/models/ProblemModel";
import type {SubmitModel} from "@/models/SubmitModel";
import type {CatsProblemModel} from "@/models/CatsProblemModel";
import useSubmitStore from "@/stores/modules/submit";
import useUserStore from "@/stores/modules/user";
import { type Ref, ref, onMounted, type PropType } from "vue";
import { useRoute } from "vue-router";

  const props = defineProps({
    problem: { type: Object as PropType<ProblemModel | CatsProblemModel>, required: true }
  })
  const submitStore = useSubmitStore();
  const userStore = useUserStore();
  const loading: Ref<boolean> = ref(true);
  const submit: Ref<SubmitModel | null> = ref(null);
  const route = useRoute();

onMounted(async () => {
    await submitStore.fetchLastSubmit({
      user_id: userStore.user.id,
      problem_id: props.problem.id
    })
      .then((data: SubmitModel | null) => submit.value = data)
      .catch((error: string) => console.log(error));
    loading.value = false;
  })

  function target() {
    if (submit.value?.status) {
      return {
        name: 'ProblemViewWithSubmit',
        params: {
          courseId: route.params.courseId,
          lessonId: route.params.lessonId,
          problemId: props.problem.id.toString(),
          submitId: submit.value.id.toString(),
        }
      };
    } else {
      return {
        name: 'ProblemView', params: {
          courseId: route.params.courseId,
          lessonId: route.params.lessonId,
          problemId: props.problem.id.toString(),
        }
      };
    }
  }

</script>
