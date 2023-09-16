<template>
  <div>
    <cv-inline-loading v-if="loading" state="loading"></cv-inline-loading>
    <div v-else>
      <div class="stats-graph">
        <span class="stat" v-for="student in students"
              :key="student.id" :style="submitStatusStyle(student)"></span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type {ProblemModel} from '@/models/ProblemModel';
import useCourseStore from '@/stores/modules/course';
import useUserStore from '@/stores/modules/user';
import useSubmitStore from '@/stores/modules/submit';
import type {SubmitModel} from "@/models/SubmitModel";
import type {UserModel} from "@/models/UserModel";
import { type PropType, ref, type Ref, computed, onMounted } from 'vue';

interface StatsGraphStyle {
  backgroundColor: string;
  width: string;
}

const props = defineProps({ problem: { type: Object as PropType<ProblemModel>, required: true } })

  const userStore = useUserStore();
  const submitStore = useSubmitStore();
  const courseStore = useCourseStore();
  const _submits: Ref<SubmitModel[]> = ref([]);
  const usersWithSubmits: Ref<number[]> = ref([]);
  const loading: Ref<boolean> = ref(true);

  const studentsCount = computed((): number => {
    return Object.keys(students.value).length;
  })

  const wrongStyle: Ref<StatsGraphStyle> = ref({
    backgroundColor: '#fc4848',
    width: `${1 / studentsCount.value * 100}%`,
  });
  const successfulStyle: Ref<StatsGraphStyle> = ref({
    backgroundColor: '#2ff306',
    width: `${1 / studentsCount.value * 100}%`,
  });
  const testingStyle: Ref<StatsGraphStyle> = ref({
    backgroundColor: '#fff300',
    width: `${1 / studentsCount.value * 100}%`,
  });
  const withoutSolutionStyle: Ref<StatsGraphStyle> = ref({
    backgroundColor: 'var(--cds-ui-01)',
    width: `${1 / studentsCount.value * 100}%`,
  });

onMounted(async () => {
    _submits.value = await submitStore.fetchProblemStats(props.problem.id);
    usersWithSubmits.value = submits.value.map(x => x.student);
    loading.value = false;
  })

const students = computed((): Dictionary<UserModel> => {
    return userStore.currentCourseStudents;
  })


const submits = computed((): SubmitModel[] => {
    return _submits.value.filter(x => students.value[x.student] !== undefined);
  })

const noSubmitsUsers = computed((): Array<UserModel> => {
    return Object.keys(students.value)
      .filter(x => !(usersWithSubmits.value.includes(Number(x))))
      .map(x => students.value[x]);
  })

function isSuccessfulStatus(studentId: number) {
    return submits.value.filter(x => x.status === "OK" && x.student === studentId).length > 0;
  }

function isTestingStatus(studentId: number) {
    return submits.value.filter(
      x => (x.status === 'AW' || x.status === 'NP') && x.student === studentId
    ).length > 0;
  }

function submitStatusStyle(student: UserModel) {
    if (isWithoutSolution(student))
      return withoutSolutionStyle.value;
    else if (isSuccessfulStatus(student.id))
      return successfulStyle.value;
    else if (isTestingStatus(student.id))
      return testingStyle.value;
    return wrongStyle.value;
  }

function isWithoutSolution(student: UserModel) {
    return noSubmitsUsers.value.includes(student);
  }
</script>

<style lang="stylus" scoped>
.stats-graph
  margin-right 5px
  width 130px
  height 5px
  display flex
  background-color var(--cds-ui-01)

.stat
  border 0.3px solid var(--cds-ui-05)
</style>
