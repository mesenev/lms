<template>
  <div v-if="loading">
    <cv-loading/>
  </div>
  <div v-else>
    <cv-structured-list class="sent">
      <template v-slot:headings>
        <cv-structured-list-heading class="headings">
          <div class="stats">
            <span>Зачтено: {{ successful.length }}</span>
            <span>Ждут проверки: {{ testing.length }}</span>
            <span>Неправильно: {{ wrong.length }}</span>
          </div>
        </cv-structured-list-heading>
      </template>
      <template v-slot:items>
        <cv-structured-list-item
          v-for="submit in successful.concat(testing).concat(wrong)" :key="submit.id">
          <div class="list-results-container">
            <cv-structured-list-data class="student">
              <user-component :userProp="students[submit.student]"/>
            </cv-structured-list-data>
            <cv-structured-list-data class="submit">
              <submit-status :submit="submit"></submit-status>
            </cv-structured-list-data>
          </div>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
    <cv-structured-list class="unsent">
      <template v-slot:headings>
        <cv-structured-list-heading>
          Не сдали: {{ noSubmitsUsers.length }}
        </cv-structured-list-heading>
      </template>
      <template v-slot:items>
        <cv-structured-list-item
          v-for="user in noSubmitsUsers"
          :key="user.id"
          class="unsent-users">
          <cv-structured-list-data>
            <user-component :userProp="user" class="user"/>
          </cv-structured-list-data>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
</template>

<script lang="ts" setup>
import StatsGraph from '@/components/StatsGraph.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import UserComponent from '@/components/UserComponent.vue';
import type { ProblemModel } from '@/models/ProblemModel';
import type { SubmitModel } from '@/models/SubmitModel';
import type { UserModel } from '@/models/UserModel';
import useCourseStore from '@/stores/modules/course';
import useUserStore from '@/stores/modules/user';
import useSubmitStore from '@/stores/modules/submit';
import { type PropType, type Ref, ref, computed, onMounted } from 'vue';

const props = defineProps({
  problem: { type: Object as PropType<ProblemModel>, required: true }
})

  const userStore =useUserStore();
  const courseStore = useCourseStore();
  const submitStore = useSubmitStore();
  const loading: Ref<boolean> = ref(true);
  const _submits: Ref<SubmitModel[]> = ref([]);
  const usersWithSubmits: Ref<number[]> = ref([]);

  const submits = computed((): SubmitModel[] => {
    return _submits.value.filter(x => students.value[x.student] !== undefined);
  })

onMounted(async () => {
    _submits.value = await submitStore.fetchProblemStats(props.problem.id);
    usersWithSubmits.value = submits.value.map(x => x.student);
    loading.value = false;
  })

  const students = computed((): Dictionary<UserModel> => {
    return userStore.currentCourseStudents;
  })

  const successful = computed(() => {
    return submits.value.filter(x => x.status === "OK");
  })

  const testing = computed(() => {
    return submits.value.filter(x => x.status === 'AW' || x.status === 'NP');
  })

  const wrong = computed(() => {
    return submits.value.filter(x => x.status === 'WA');
  })

  const noSubmitsUsers = computed((): Array<UserModel> => {
    return Object.keys(students.value)
      .filter(x => !(usersWithSubmits.value.includes(Number(x))))
      .map(x => students.value[x]);
  })
</script>

<style lang="stylus" scoped>
.list-results-container
  display flex
  flex-direction row
  justify-content space-between
  align-items center

.submit span:first-child
  margin-right 5px

.sent, .unsent
  margin-bottom 1rem
  padding-left 1rem

  /deep/ .bx--structured-list-tbody
    padding 0 1rem

  .headings
    display flex
    flex-direction row
    justify-content space-between

  .stats
    display flex
    flex-direction row

    > span:not(:last-child)
      margin-right 5px

.sent
  /deep/ .bx--structured-list-tbody
    display flex
    flex-direction column


.unsent
  /deep/ .bx--structured-list-tbody
    display flex
    flex-direction row
    flex-wrap wrap

  .cv-structured-list-item
    border 0
    flex 0 0 25%

  .user
    border 0
</style>
