<template>
  <aside>
    <nav>
      <ul>
        <li class="navigation-title" v-if="classwork.length > 0">
          <span title="Классная работа">CW</span>
          <ul v-if="!loading">
            <problem-navigation-item :problem="problem" v-for="problem in classwork"
                                     :key="problem.id"/>
          </ul>
          <ul v-else>
            <cv-tag-skeleton/>
          </ul>
        </li>
        <li class="navigation-title" v-if="homework.length > 0">
          <span title="Домашняя работа">HW</span>
          <ul v-if="!loading">
            <problem-navigation-item :problem="problem" v-for="problem in homework"
                                     :key="problem.id"/>
          </ul>
          <ul v-else>
            <cv-tag-skeleton/>
          </ul>
        </li>
        <li class="navigation-title" v-if="extrawork.length > 0">
          <span title="Дополнительные задания">EX</span>
          <ul v-if="!loading">
            <problem-navigation-item :problem="problem" v-for="problem in extrawork"
                                     :key="problem.id"/>
          </ul>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script lang="ts" setup>
import useProblemStore from '@/stores/modules/problem';
import ProblemNavigationItem from '@/components/ProblemNavigationItem.vue';
import ProblemModel from "@/models/ProblemModel";
import { computed, onMounted, ref, Ref } from "vue";

const props = defineProps({lessonId:{required: true, type: Number}})

const  problemStore = useProblemStore();
const  problems: Ref<Array<ProblemModel>> = ref([]);
const  loading = ref(true);

function target(pid: number) {
    return { name: 'ProblemView', params: { problemId: pid.toString() } };
  }

const isProblemsEmpty = computed(() => {
    if (problems.value.length === 0) {
      return true;
    }
  })

const classwork = computed((): Array<ProblemModel> => {
    return problems.value.filter(x => x.type === 'CW');
  })

const homework = computed((): Array<ProblemModel> => {
    return problems.value.filter(x => x.type === 'HW');
  })

const extrawork = computed((): Array<ProblemModel> => {
    return problems.value.filter(x => x.type === 'EX');
  })


onMounted(async () => {
    problems.value = await problemStore.fetchProblemsByLessonId(this.lessonId);
    loading.value = false;
  })

</script>


<style lang="stylus" scoped>
aside
  position absolute
  padding-left 1rem

.navigation-title
  color var(--cds-text-01)
  margin-top 0.5rem

  span
    border-radius 50px
    text-align center
    width 32px
    height 32px
    line-height 32px
    margin-bottom 1rem

.navigation-title
  height auto

  span
    color white
    background-color #808080
    display block
    cursor default
</style>

<style lang="stylus" scoped>
.bx--structured-list-row--header-row
  background-color #393939

  .pupil-title
    color white
</style>
