<template>
  <div class="bx--grid">
    <div v-if="!loading">
      <div class="main-title">
        <h2>Успеваемость урока: {{ currentLesson.name }}</h2>
      </div>
      <div class="table-actions" v-if="progress.length">
        <cv-toggle v-model="dontSolved"
                   value="value">
          <template v-slot:text-left>Отображать только студентов без решений</template>
          <template v-slot:text-right>Отображать только студентов без решений</template>
        </cv-toggle>
        <div class="problem-type-dropdown">
          <cv-dropdown v-model="problemsType">
            <cv-dropdown-item value="CW" selected>Классная работа</cv-dropdown-item>
            <cv-dropdown-item value="HW">Домашняя работа</cv-dropdown-item>
            <cv-dropdown-item value="EW">Доп. задачи</cv-dropdown-item>
          </cv-dropdown>
        </div>
      </div>
      <div class="table-wrapper" v-if="progress.length">
        <cv-data-table @sort="Sort">
          <template v-slot:headings>
            <cv-data-table-heading class="fixed-col thead-element"
                                   v-for="(column, id) in columns" :key="id"
                                   :sortable="true">
              <h5 v-if="(column.id === 0)">Результаты</h5>
              <h5 v-else-if="(column.id === -2)">{{ column.name }}</h5>
              <div v-else @click="openSubmitOrProblem(column.id)">
                <cv-definition-tooltip :definition="definition(column.id)"
                                       :term="column.name"
                                       direction="bottom"/>
              </div>
            </cv-data-table-heading>
          </template>
          <template v-slot:data>
            <cv-data-table-row v-for="user in progress" :key="user.id">
              <cv-data-table-cell class="fixed-col">
                <router-link :to="{ name: 'profile-page', params: { userId: user.user } }"
                             class="course--title" tag="p">
                  <UserComponent :userId="user.user"/>
                </router-link>
              </cv-data-table-cell>
              <cv-data-table-cell v-for="problem in problems"
                                  :key="problem.id"
                                  class="mark tbody-element">
                <div
                  @click="openSubmitOrProblem(problem.id, user.solved[problem.type][problem.id][1])">
                  <submit-status v-if="userMarks(user,problem.type,problem.id)"
                                 :submit="create_submit(user.solved[problem.type][problem.id],problem.id,user.user)"/>
                </div>
              </cv-data-table-cell>
              <cv-data-table-cell>
                {{ average(user).toString() + '%' }}
              </cv-data-table-cell>
            </cv-data-table-row>
          </template>
          >
        </cv-data-table>
      </div>
      <empty-list-component v-else :text="emptyText" list-of="students"/>
    </div>
    <cv-data-table-skeleton v-else :columns="2" :rows="6"/>
  </div>
</template>


<script lang="ts" setup>
import SubmitStatus from "@/components/SubmitStatus.vue";
import UserComponent from "@/components/UserComponent.vue";
import type { LessonModel } from '@/models/LessonModel';
import type { ProblemModel } from "@/models/ProblemModel";
import type { UserModel } from "@/models/UserModel";
import type { UserProgress } from '@/models/UserProgress';
import useLessonStore from "@/stores/modules/lesson";
import useProblemStore from "@/stores/modules/problem";
import useProgressStore from "@/stores/modules/progress";
import useUserStore from '@/stores/modules/user';
import useSubmitStore from '@/stores/modules/submit';
import type { SubmitModel } from "@/models/SubmitModel";
import EmptyListComponent from "@/components/lists/EmptyListComponent.vue";
import { ref, type Ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

  const props = defineProps({lessonId: {type: Number, required: true}})


  const students: Ref<Array<UserProgress>> = ref([]);
  const users:Ref<Dictionary<UserModel>> = ref({});
  const _problems: Ref<Array<ProblemModel>> = ref([]);
  const submits: Ref<Dictionary<SubmitModel[]>> = ref({});
  const lesson: Ref<LessonModel> = ref({
    id: NaN,
    course: NaN,
    description: '',
    name: '',
    problems: [],
    exams: [],
    materials: [],
    deadline: '',
    lessonContent: '',
    is_hidden: true,
    progress: [],
    scores: {},
  });

  const userStore = useUserStore();
  const lessonStore = useLessonStore();
  const progressStore = useProgressStore();
  const problemStore = useProblemStore();
  const submitStore = useSubmitStore();

  const route = useRoute();
  const router = useRouter();

  const loading: Ref<boolean> = ref(true);
  const dontSolved: Ref<boolean> = ref(false);
  const problemsType: Ref<string> = ref('');
  const emptyText: Ref<string> = ref('');

  const columns = computed(() => {
    const a = problems.value.map(l => (
      {
        id: l.id,
        name: l.name,
      }
    ))
    a.unshift({ id: -2, name: "Ученики" })
    a.push({ id: 0, name: "Рейтинг" })
    return a
  })

  const problems = computed(() => {
    return _problems.value.filter(x => x.type === problemsType.value);
  })

  const progress = computed(() => {
    if (dontSolved.value) {
      return students.value.filter(x => Object.keys(x.solved[problemsType.value]).length === 0)
    }
    return students.value;
  })

  const currentLesson = computed(() => {
    return lesson.value;
  })

onMounted(async () => {
    lesson.value = await lessonStore.fetchLessonById(props.lessonId);
    users.value = await userStore.fetchStudentsByCourseId(lesson.value.course);
    _problems.value = await problemStore.fetchProblemsByLessonId(props.lessonId);
    for (const problem of _problems.value) {
      submits.value[problem.id] = await submitStore.fetchProblemStats(problem.id);
    }
    students.value = (await progressStore.fetchLessonProgressByLessonId(props.lessonId));
    emptyText.value = 'Ни один студент не записан на курс';
    loading.value = false;
  })

  function openSubmitOrProblem(problem: number, submit?: number) {
    if (submit)
      router.push(`/course/${route.params['courseId']}/lesson/${route.params['lessonId']}/problem/${problem}/submit/${submit}`);
    else
      router.push(`/course/${route.params['courseId']}/lesson/${route.params['lessonId']}/problem/${problem}`);
  }

  function definition(column: number) {
    if (!loading.value && column != -2 && column != 0) {
      const columnProblem = problems.value.filter((problem) => problem.id === column)[0]
      column = (columnProblem) ? (columnProblem.stats ? columnProblem.stats.green : 0) : 0;
    }
    return `Успешно решило ${column} из ${progress.value.length} студентов`
  }

  function create_submit(status_id: never, problemId: number, userid: number) {
    return {
      id: Object.values(status_id)[1],
      problem: problemId,
      student: Number(userid),
      status: Object.values(status_id)[0]
    }
  };

  function userMarks(userId: UserProgress, problemType: string, problemId: number) {
    return userId.solved[problemType][problemId];
  }

  function average(user: UserProgress): number {
    const problemIds = problems.value.filter(x => x.type === problemsType.value).map(x => x.id);
    let solvedCount = 0;

    for (const submits_ptr of Object.values(submits.value)) {
      solvedCount += submits_ptr.filter(
        x => x.student === user.user && x.status === 'OK' && problemIds.includes(x.problem.id)
      ).length ? 1 : 0;
    }
    const averageResult = (solvedCount / problemIds.length) * 100;

    return problemIds.length ? Math.trunc(averageResult) : 0;
  }

  function Sort(sortBy: { index: string; order: string }) {
    let order = -1;
    if (sortBy.order == "none") {
      return students.value.sort((a, b) => {
        return a.id - b.id
      })
    }
    if (sortBy.order == "ascending") {
      order *= -1;
    }
    if (sortBy.index == "0") {
      return students.value.sort((a, b) => {
        return (users.value[a.user].last_name > users.value[b.user].last_name) ? order : -1 * order;
      })
    } else if (sortBy.index == (columns.value.length - 1).toString()) {
      return students.value.sort((a, b) => {
        return (average(a) > average(b) ? order : -1 * order);
      })
    } else {
      const solved = students.value.filter(x => x.solved[problemsType.value][sortBy.index]).sort((a, b) => {
        const aSolutions = a.solved[problemsType.value][sortBy.index];
        const bSolutions = b.solved[problemsType.value][sortBy.index];
        const A = aSolutions[0] === 'OK' ? 1 : (aSolutions[0] === 'NP' ? 0 : -1);
        const B = bSolutions[0] === 'OK' ? 1 : (bSolutions[0] === 'NP' ? 0 : -1);
        return (A > B) ? order : -1 * order;
      })
      return students.value = solved.concat(students.value.filter(x => !x.solved[problemsType.value][sortBy.index]));
    }
  }
</script>

<style lang="stylus" scoped>
.main-title
  margin-left 0
  margin-bottom 0

.table-actions
  display flex
  flex-direction row

.problem-type-dropdown
  width fit-content

/deep/ .bx--list-box__field
  display flex

.table-wrapper
  margin-top 1rem
  border 0.5px solid var(--cds-ui-05)
  border-collapse separate
  overflow-x auto
  width 100%

/deep/ table
  text-align-last center
  border-collapse separate

/deep/ th
  padding-top 0.5rem
  padding-bottom 0.5rem

.tbody-element, .fixed-col
  border-right 0.5px solid var(--cds-ui-05)
  z-index 0

.fixed-col:first-child
  text-align-last left
  z-index 2
  position sticky
  left 0

.fixed-col:last-child
  border-right none

/deep/ .bx--data-table-container
  padding-top 0

.mark
  user-select none

/deep/ .tag
  cursor pointer

.user-component
  cursor pointer

/deep/ .empty-list-wrapper
  margin-top 5rem
  text-align center

  h4
    font-size var(--cds-productive-heading-04-font-size)

  p
    font-size var(--cds-productive-heading-03-font-size)

.attendance
  display inline

  label
    display inline

</style>
