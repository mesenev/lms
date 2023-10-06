<template>
  <div class="bx--grid">
    <div v-if="!loading">
      <div class="main-header">
        <div class="main-title">
          <h2>Успеваемость курса: {{ course.name }}</h2>
        </div>
        <cv-button :disabled="change" v-on:click="mark" v-if="progress.length">
          Отметить посещаемость
        </cv-button>
      </div>
      <div class="table-wrapper" v-if="progress.length">
        <cv-data-table @sort="Sort">
          <template v-slot:headings>
            <cv-data-table-heading class="fixed-col thead-element"
                                   v-for="(column, id) in columns" :key="id"
                                   :sortable=true>
              <h5 v-if="(column.id === 0)">Результаты</h5>
              <h5 v-else-if="(column.id === -2)">{{ column.name }}</h5>
              <div v-else @click="openSubmitOrProblem(column.id)">
                <h5>{{ column.name }}</h5>
              </div>
            </cv-data-table-heading>
          </template>
          <template v-slot:data>
            <cv-data-table-row v-for="row in progress" :key="row.user">
              <cv-data-table-cell class="fixed-col">
                <router-link
                  :to="{ name: 'profile-page', params: { userId: row.user} }"
                  class="course--title" tag="p">
                  <UserComponent :userProp="users[row.user]"/>
                </router-link>
              </cv-data-table-cell>
              <cv-data-table-cell v-for="les in lessons"
                                  :key="les.id"
                                  class="tbody-element">
                <div class="tbody-data">
                  <div class="marks">
                    <cv-tooltip tip="Результирующий балл">
                      <cv-tag class="result-mark" :label="sum(row.progress[les.id]).toString()"/>
                    </cv-tooltip>
                    <div v-for="(value, name) in row.progress[les.id]" :key="value+name"
                         class="mark">
                      <cv-tooltip :tip="`Балл за: ${name}`">
                        <cv-tag :label="Math.trunc(value).toString()" :kind="color(name)"/>
                      </cv-tooltip>
                    </div>
                  </div>
                  <div class="mark-checkbox">
                    <cv-checkbox
                      :checked="student_attendance[`${row.user}-${les.id}`].attendance"
                      :value="`${row.user}-${les.id}`"
                      @change="attendanceChange(row.user, les.id)"/>
                  </div>
                </div>
              </cv-data-table-cell>
              <cv-data-table-cell>
                {{ average(row.progress).toString() }}
              </cv-data-table-cell>
            </cv-data-table-row>
          </template>
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
import _ from 'lodash';
import type { UserModel } from "@/models/UserModel";
import type { Attendance } from "@/models/Attendance";
import type { UserProgress } from '@/models/UserProgress';
import useCourseStore from '@/stores/modules/course'
import useProblemStore from "@/stores/modules/problem"
import useProgressStore from "@/stores/modules/progress"
import useUserStore from '@/stores/modules/user';
import useLessonStore from '@/stores/modules/lesson'
import UserAvatar20 from '@carbon/icons-vue/es/user--avatar/20';
import type { CourseModel } from "@/models/CourseModel";
import type { LessonModel } from "@/models/LessonModel";
import api from "@/stores/services/api";
import EmptyListComponent from "@/components/lists/EmptyListComponent.vue";
import { ref, type Ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

const props = defineProps({ courseId: { type: Number, required: true } })
const userStore = useUserStore();
const courseStore = useCourseStore();
const progressStore = useProgressStore();
const problemStore = useProblemStore();
const lessonStore = useLessonStore();
const router = useRouter();
const route = useRoute();

const students_progress: Ref<Array<UserProgress>> = ref([]);
const s: Ref<Dictionary<Array<Attendance>>> = ref({});
const users: Ref<Dictionary<UserModel>> = ref({});
const student_attendance: Ref<Dictionary<Attendance>> = ref({});
const student_attendance_copy: Ref<Dictionary<any>> = ref({});
const lessons: Ref<Array<LessonModel>> = ref([]);
const course: Ref<CourseModel> = ref({ ...courseStore.newCourse });
const emptyText: Ref<string> = ref('');

const loading: Ref<boolean> = ref(true);
const sortable: Ref<boolean> = ref(true);
const dontSolved: Ref<boolean> = ref(false);

const columns = computed(() => {
  const a = lessons.value.map(l => (
    {
      id: l.id,
      name: l.name,
    }
  ))
  a.unshift({ id: -2, name: "Ученики" })
  a.push({ id: 0, name: "Рейтинг" })
  return a
})

const attendance = computed(() => {
  return student_attendance.value;
})

const progress = computed(() => {
  // if (this.dontSolved) {
  //   return this.students_progress.filter(x => Object.keys(x.solved["HW"]).length === 0)
  // }
  return students_progress.value;
})

const change = computed(() => {
  return _.isEqual(student_attendance.value, student_attendance_copy.value)
})

function attendanceChange(userId: number, lessonId: number) {
  const key = `${userId}-${lessonId}`;
  student_attendance_copy.value[key].attendance = !student_attendance_copy.value[key].attendance;
}

onMounted(async () => {
  course.value = await courseStore.fetchCourseById(props.courseId);
  students_progress.value = await progressStore.fetchCourseProgressById(props.courseId);
  users.value = await userStore.fetchStudentsByCourseId(props.courseId);
  lessons.value = await lessonStore.fetchLessonsByCourseId(props.courseId);
  s.value = await progressStore.fetchAttendance(props.courseId);
  emptyText.value = 'Ни один студент не записан на данный курс'

  for (const [key, val] of Object.entries(s.value))
    for (const at of val)
      student_attendance.value[`${key}-${at.lesson}`] = at;

  student_attendance_copy.value = _.cloneDeep(student_attendance.value);
  loading.value = false;
})

function color(type: string) {
  if (type === 'CW') {
    return 'blue'
  }
  if (type === 'HW') {
    return 'green'
  }
  if (type === 'EX') {
    return 'purple'
  }
}

function sum(type: any) {
  return Math.trunc(type['CW'] + type['HW'] + type['EX']);
}

function average(progress: Dictionary<string>) {
  let sum = 0 as any;
  for (const submits of Object.values(progress)) {
    sum += submits['CW' as any];
    sum += submits['HW' as any];
    sum += submits['EX' as any];
  }
  return Math.trunc(sum);
}

//TODO: change it with classical link
function openSubmitOrProblem(problem: number, submit?: number) {
  if (submit)
    router.push(`/course/${route.params['courseId']}/lesson/${route.params['lessonId']}/problem/${problem}/submit/${submit}`);
  else
    router.push(`/course/${route.params['courseId']}/lesson/${route.params['lessonId']}/problem/${problem}`);
}

async function mark(): Promise<void> {
  let success = true;
  //TODO: remove unchanged instances
  for (const val of Object.values(student_attendance_copy)) {
    const request = api.patch(`/api/lessonprogress/${val.id}/`, val);
    request.then((response) => {
      //
    });
    request.catch((error) => {
      success = false;
    })
  }
  student_attendance.value = _.cloneDeep(student_attendance_copy.value);
}

function Sort(sortBy: { index: string; order: string }) {
  let order = -1;
  if (sortBy.order == "none") {
    return students_progress.value.sort((a, b) => {
      return a.user - b.user
    })
  }
  if (sortBy.order == "ascending") {
    order *= -1;
  }
  if (sortBy.index == "0") {
    return students_progress.value.sort((a, b) => {
      return (users.value[a.user].last_name > users.value[b.user].last_name) ? order : -1 * order;
    })
  } else if (sortBy.index == (columns.value.length - 1).toString()) {
    return students_progress.value.sort((a, b) => {
      const A = a.progress ? average(a.progress) : 0;
      const B = b.progress ? average(b.progress) : 0;
      return A > B ? order : -1 * order;
    })
  } else {
    return students_progress.value.sort((a, b) => {
      const A = a.progress ? sum(a.progress[sortBy.index]) : 0;
      const B = b.progress ? sum(b.progress[sortBy.index]) : 0;
      return A > B ? order : -1 * order;
    })
  }
}
</script>

<style scoped lang="stylus">
.main-header
  display flex
  flex-direction row
  justify-content space-between
  margin-bottom 1rem

.main-title
  margin-left 0
  margin-bottom 0

.table-wrapper
  margin-top 1rem
  border 0.5px solid var(--cds-ui-05)
  border-collapse separate
  overflow-x auto
  width 100%

.tbody-element, .fixed-col
  min-width 16rem
  border-right 0.5px solid var(--cds-ui-05)
  z-index 0

.tbody-data
  display flex
  flex-direction row
  justify-content space-around

.fixed-col:first-child
  text-align-last left
  z-index 2
  position sticky
  left 0

.fixed-col:last-child
  border-right none

:deep() table
  text-align-last center
  border-collapse separate

:deep() th
  padding-top 0.5rem
  padding-bottom 0.5rem

:deep() .bx--data-table-container
  padding-top 0

.marks
  min-width 180px

.result-mark
  color var(--cds-ui-05)
  background-color var(--cds-ui-background)
  border var(--cds-ui-05) 0.5px solid

.mark
  display: inline-flex

.mark-checkbox
  display flex
  align-items center

.user-component
  cursor pointer

:deep() .empty-list-wrapper
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

.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.items
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.item
  min-height 85px
</style>
