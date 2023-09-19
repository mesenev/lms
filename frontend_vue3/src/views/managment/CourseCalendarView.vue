<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>Расписание занятий</h1>
    </div>
    <div class="bx--row header">
      <div class="items-top bx--col-lg-10">
        <div class="items-top--element" v-if="!loading">
          <span v-if="startDate">Начало занятий: {{ startDate }}</span>
          <span v-else>Расписание для курса не составлено</span>
        </div>
        <cv-skeleton-text v-else :heading="true" :width="'35%'" class="main-title"/>
        <hr>
        <div v-if="!loading" class="items-top--element">
          <span> {{ currentScheduledDays }}</span>
        </div>
        <cv-button
          class="items-top--element"
          v-on:click="showModal" kind="secondary" tip-position="hidden"
          :icon="iconEdit">
          Редактировать
        </cv-button>
        <cv-modal
          close-aria-label="Закрыть"
          :visible="modalVisible"
          @modal-hidden="actionHidden"
          :primaryButtonDisabled="!isScheduleChanged"
          @primary-click="changeSchedule"
          :auto-hide-off="false">
          <template v-slot:title>Редактирование расписания</template>
          <template v-slot:content>
            <cv-grid>
              <cv-row v-if="showNotification">
                <cv-inline-notification
                  :kind="notificationKind"
                  :sub-title="notificationText"
                  @close="hideNotification"
                />
              </cv-row>
              <cv-row>
                <cv-column :sm="1">
                  <h4 class="">Начало занятий</h4>
                </cv-column>
                <cv-column :sm="1">
                  <cv-date-picker
                    date-label=""
                    kind="single"
                    placeholder="dd/mm/yyyy"
                    :cal-options="calOptions"
                    v-model="changedStartDate">
                  </cv-date-picker>
                </cv-column>
                <cv-column :sm="5"></cv-column>
              </cv-row>
              <cv-row>
                <cv-column :sm="1">
                  <div class="daytime-container">
                    <cv-checkbox label="Понедельник" value='123' v-model="monday"/>
                    <cv-time-picker
                      label=""
                      ampm="24" :disabled="!monday" :time.sync="newSchedule[0]" :form-item="true"
                    />
                  </div>
                  <div class="daytime-container">
                    <cv-checkbox label="Вторник" value='123' v-model="tuesday"/>
                    <cv-time-picker
                      label="" ampm="24" :disabled="!tuesday"
                      :time.sync="newSchedule[1]" :form-item="true"/>
                  </div>
                  <div class="daytime-container">
                    <cv-checkbox label="Среда" value='123' v-model="wednesday"/>
                    <cv-time-picker
                      label="" ampm="24" :disabled="!wednesday"
                      :time.sync="newSchedule[2]" :form-item="true"/>
                  </div>
                </cv-column>
                <cv-column :sm="1">
                  <div class="daytime-container">
                    <cv-checkbox label="Четверг" value='123' v-model="thursday"/>
                    <cv-time-picker
                      label="" ampm="24" :disabled="!thursday"
                      :time.sync="newSchedule[3]" :form-item="true"/>
                  </div>
                  <div class="daytime-container">
                    <cv-checkbox label="Пятница" value='123' v-model="friday"/>
                    <cv-time-picker
                      label="" ampm="24" :disabled="!friday"
                      :time.sync="newSchedule[4]" :form-item="true"/>
                  </div>
                  <div class="daytime-container">
                    <cv-checkbox label="Суббота" value='123' v-model="saturday"/>
                    <cv-time-picker
                      label="" ampm="24" :disabled="!saturday"
                      :time.sync="newSchedule[5]" :form-item="true"/>
                  </div>
                </cv-column>
                <cv-column :sm="1">
                  <div class="daytime-container">
                    <cv-checkbox label="Воскресенье" value='123' v-model="sunday"/>
                    <cv-time-picker
                      label="" ampm="24" :disabled="!sunday"
                      :time.sync="newSchedule[6]" :form-item="true"/>
                  </div>
                </cv-column>
              </cv-row>
            </cv-grid>
          </template>
          <template v-slot:primary-button>Сохранить изменения</template>
        </cv-modal>
      </div>
    </div>


    <div class="bx--row">
      <div class="items bx--col-lg-10 schedule-list">
        <cv-structured-list selectable @change="actionChange">
          <template v-slot:headings></template>
          <template v-if="loading" v-slot:items>
            <cv-inline-loading/>
          </template>
          <template v-else v-slot:items>
            <cv-structured-list-item
              v-for="(record, index) in scheduledLessons"
              :key="index"
              :checked="record.isSelected"
              :cur_key="scheduledLessons[index].lesson_id"
              :key_k="index"
              :value="record.lesson_id.toString()"
              v-on:click="dropSelect"
              name="group">
              <cv-structured-list-data>
                <div class="structured-list--data-wrapper">
                  <date-view-component :date-as-integer="record.date" :show-day-week="true"/>
                  <cv-icon-button
                    kind="ghost"
                    size="sm"
                    tip-position="hidden"
                    :cur_key="scheduledLessons[index].lesson_id"
                    :icon="iconEdit"
                    :key_k="index"
                    :disabled="!lessons.find(a => a.id === record.lesson_id).is_hidden"
                    v-on:click="st_showModal"/>
                </div>
                <cv-modal
                  close-aria-label="Закрыть"
                  :visible="st_modalVisible"
                  @primary-click="changeLessonDate"
                  :primaryButtonDisabled="!isSelfDateChanged"
                  @modal-hidden="st_actionHidden"
                  :auto-hide-off="false">
                  <template v-slot:title>Установка собственного времени</template>
                  <template v-slot:content>
                    <cv-grid>
                      <cv-row>
                        <cv-column>
                          <cv-date-picker
                            dateLabel="Дата"
                            kind="single"
                            :cal-options="calOptions"
                            placeholder="dd/mm/yyyy"
                            v-model="set_custom_date"
                            @onChange="actionChange">
                          </cv-date-picker>
                          <hr>
                        </cv-column>
                      </cv-row>
                    </cv-grid>
                  </template>
                  <template slot="secondary-button">Отменить</template>
                  <template slot="primary-button">Сохранить изменения</template>
                </cv-modal>
              </cv-structured-list-data>
              <cv-structured-list-data>
                {{ lessonById(record.lesson_id).name }}
              </cv-structured-list-data>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
      </div>
    </div>

    

    <div v-if="lessonsWOt.length !== 0" class="bx--row header no-schedule--wrapper">
      <div class="items-top bx--col-lg-10">
        <div class="items-top--element" v-if="!loading">
          <span>Уроки без установленного времени</span>
        </div>
        <cv-skeleton-text v-else :heading="true" :width="'35%'" class="main-title"/>
        <cv-structured-list>
          <template v-slot:headings></template>
          <template v-if="loading" v-slot:items>
            <cv-loading/>
          </template>
          <template v-else v-slot:items>
            <cv-structured-list-item
              v-for="item in lessonsWOt"
              :key="item.id"
              :cur_key="item.id"
              :item="item">
                <cv-structured-list-data>
                  Установите время для урока
                  <cv-icon-button
                    kind="tertiary"
                    size="xl"
                    label="Установить собственную дату"
                    tip-position="hidden"
                    :icon="iconEdit"
                    :cur_key="item.id"
                    v-on:click="st_showModal"
                  />
                  <cv-modal
                    :cur_key="item.id"
                    close-aria-label="Закрыть"
                    :visible="st_modalVisible"
                    @primary-click="changeLessonDate"
                    :primaryButtonDisabled="!isSelfDateChanged"
                    @modal-hidden="st_actionHidden"
                    :auto-hide-off="false">
                    <template v-slot:title>Установка собственного времени</template>
                    <template v-slot:content>
                      <cv-grid>
                        <cv-row>
                          <cv-column>
                            <cv-date-picker
                              dateLabel="Дата"
                              kind="single"
                              placeholder="dd/mm/yyyy"
                              :cal-options="calOptions"
                              v-model="set_custom_date"
                              @onChange="actionChange">
                            </cv-date-picker>
                            <hr>
                          </cv-column>
                        </cv-row>
                      </cv-grid>
                    </template>
                    <template v-slot:secondary-button>Отменить</template>
                    <template v-slot:primary-button>Сохранить изменения</template>
                  </cv-modal>
                </cv-structured-list-data>
                <cv-structured-list-data>{{ item.name }}</cv-structured-list-data>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
      </div>
    </div>

    <div class="save-button">
      <cv-inline-notification
        v-if="showNotification"
        :kind="notificationKind"
        :sub-title="notificationText"
        @close="hideNotification"
      />
      <cv-button-set>
        <cv-button
          :disabled="!scheduleChangedAndNotEmpty || updatingInProgress"
          kind="secondary"
          v-on:click="revertChanges">Отменить
        </cv-button>
        <cv-button
          :disabled="!scheduleChangedAndNotEmpty || updatingInProgress"
          kind="primary"
          v-on:click="saveOrUpdateSchedule">
          {{ (isNewSchedule) ? "Создать расписание" : "Сохранить изменения" }}
        </cv-button>
      </cv-button-set>
    </div>
  </div>
</template>

<script lang="ts" setup>
import DateViewComponent from '@/components/common/DateViewComponent.vue';
import useNotificationMixinComponent from '@/components/common/NotificationMixinComponent.vue';
import useWeekDaysMixin from '@/components/common/WeekDaysMixin.vue';
import type { CourseModel } from '@/models/CourseModel';
import type { LessonModel } from '@/models/LessonModel';
import type { CourseScheduleModel, ScheduleElement}  from '@/models/ScheduleModel';
import useCourseStore from '@/stores/modules/course';
import Edit from '@carbon/icons-vue/es/edit/20';
import Back from '@carbon/icons-vue/es/skip--back/20';
import api from '@/stores/services/api';
import _ from 'lodash';
import { dateParse } from '@/utils/utils';
import { ref, type Ref, computed, onMounted, watch } from 'vue';

  const props = defineProps({
    courseId: { type: Number, required: true }
  })
  const courseStore = useCourseStore();
  const course: Ref<CourseModel> = ref({} as CourseModel);
  const courseSchedule: Ref<CourseScheduleModel> =
    ref({
      id: NaN, name: '', course: course.value.id, lessons: [], start_date: '', week_schedule: {},
    } as CourseScheduleModel);

  const { monday, tuesday, wednesday, thursday, friday, saturday, sunday } = useWeekDaysMixin();

  const oldCourseSchedule: Ref<CourseScheduleModel> = ref(_.cloneDeep(courseSchedule));
  const iconEdit = Edit;
  const modalVisible: Ref<boolean> = ref(false);
  const st_modalVisible: Ref<boolean> = ref(false);
  const startDate: Ref<string | null> = ref(null);
  const changedStartDate: Ref<string | null> = ref(null);
  const set_custom_date: Ref<string> = ref("");
  const cur_custom_date: Ref<string | null> = ref(null);
  const selected: Ref<string | null> = ref(null);
  const loading: Ref<boolean> = ref(true);
  const cur_les_upd_id: Ref<string> = ref("");
  const k_keeper: Ref<number | null> = ref(null);
  const updatingInProgress: Ref<boolean> = ref(false);
  const newSchedule: Ref<Record<string, string | null>> = ref({});
  const schedule: Ref<Record<string, string | null>> = ref({
    0: null, 1: null, 2: null, 3: null, 4: null, 5: null, 6: null,
  });

  const { notificationKind, notificationText, hideNotification, showNotification } = useNotificationMixinComponent();
  const alias = [
    'Понедельник', 'Вторник', "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье",
  ];

onMounted(async () => {
    course.value = courseStore.currentCourse
      ?? await courseStore.fetchCourseById(props.courseId);
    courseSchedule.value.course = course.value.id;
    oldCourseSchedule.value.course = course.value.id;
    if (!course.value.id || typeof (course.value.schedule) !== 'number') {
      loading.value = false;
      return;
    }
    courseSchedule.value = await courseStore.fetchCourseScheduleByCourseId(props.courseId);
    oldCourseSchedule.value = _.cloneDeep(courseSchedule.value);
    startDate.value = courseSchedule.value.start_date;
    schedule.value = courseSchedule.value.week_schedule;
    if (courseSchedule.value.lessons)
      for (let i = 0; i < courseSchedule.value.lessons.length; i++)
        courseSchedule.value.lessons[i].isSelected = false;
    loading.value = false;
  })

  watch(startDate, (new_val: string) =>{
    courseSchedule.value.start_date = new_val;
  })

  watch(schedule, (new_val: Record<string, string | null>) =>{
    courseSchedule.value.week_schedule = new_val;
  })

  const calOptions = computed((): object => {
    return { dateFormat: 'd/m/Y' };
  })

  const scheduleChangedAndNotEmpty = computed((): boolean => {
    return !_.isEqual(courseSchedule.value, oldCourseSchedule.value)
      && (courseSchedule.value.lessons.length > 0);
  })

  const isNewSchedule = computed(() => {
    return !courseSchedule.value.id;
  })

  const currentScheduledDays = computed(() => {
    let courseSchedule = '';
    Object.keys(workingDays.value).forEach(
      value => courseSchedule += `${alias[parseInt(value)]}: ${workingDays.value[value]} `,
    );
    return courseSchedule;
  })

  const isScheduleChanged = computed(() => {
    return Object.values(newSchedule.value).filter(x => typeof (x) === 'string').length > 0
      && !!changedStartDate.value && (
        !_.isEqual(schedule.value, newSchedule.value)
        || !_.isEqual(startDate.value, changedStartDate.value)
      );
  })

  const isSelfDateChanged = computed(() => {
    return !(set_custom_date.value == cur_custom_date.value);
  })

  const lessons = computed((): Array<LessonModel> => {
    if (loading.value || !course.value.id)
      return [];
    return course.value.lessons;
  })

  const scheduledLessons = computed((): ScheduleElement[] => {
    function compare(a: ScheduleElement, b: ScheduleElement) {
      if (a.date > b.date) return 1;
      if (a.date < b.date) return -1;
      return 0;
    }

    return courseSchedule.value.lessons.sort(compare);
  })

  const lessonsWOt = computed((): LessonModel[] => {
    if (loading.value || !course.value.id)
      return [];
    const ids = scheduledLessons.value.map(value => Number(value.lesson_id));
    return course.value.lessons.filter(value => ids.indexOf(Number(value.id)) === -1);
  })

  function lessonById(id: number): LessonModel {
    return lessons.value.find(x => Number(x.id) === Number(id)) as LessonModel;
  }

  const workingDays = computed((): Record<string, string> => {
    if (!schedule.value) return {};
    return Object.keys(schedule.value)
      .filter(key => schedule.value[key] != null)
      .reduce((obj: Record<string, string>, key: string) => {
        obj[key] = schedule.value[key] as string;
        return obj;
      }, {});
  })


  function onUpdateTime(n: number) {
    return (value: string) => newSchedule.value = { ...newSchedule.value, [n]: value };
  }


  function showModal() {
    newSchedule.value = { ...schedule.value };
    changedStartDate.value = startDate.value;
    modalVisible.value = true;
  }

  async function st_showModal(event: PointerEvent) {
    st_modalVisible.value = true;
    const element = (event?.currentTarget as Element);
    cur_les_upd_id.value = element.getAttribute('cur_key') as string;
    set_custom_date.value = "";
    cur_custom_date.value = "";
    if (element.getAttribute('key_k') !== null) {
      k_keeper.value = Number(element.getAttribute('key_k'));
      const currentDate = (courseSchedule.value as CourseScheduleModel).lessons[k_keeper.value].date;
      const date = new Date(currentDate);
      set_custom_date.value = date.toISOString();
      cur_custom_date.value = set_custom_date.value;
    }
    if (cur_les_upd_id.value === null) {
      throw Error();
    }

  }

  function actionHidden() {
    modalVisible.value = false;
  }

  function st_actionHidden() {
    st_modalVisible.value = false;
  }

  function changeSchedule() {
    modalVisible.value = false;
    schedule.value = { ...newSchedule.value };
    startDate.value = changedStartDate.value;
    generateSchedule();
  }

  async function actionChange(obj: string) {
    const schedule = courseSchedule.value as CourseScheduleModel;
    const n = schedule.lessons.findIndex(x => x.lesson_id === Number(obj));
    if (!course.value?.lessons[n].is_hidden) {
      alert("Изменять время открытого урока невозможно");
      selected.value = "-1";
      schedule.lessons[n].isSelected = false;
      return;
    } else if (!selected.value || selected.value == "-1") {
      selected.value = n.toString();
      schedule.lessons[n].isSelected = true;
      return;
    }
    // TODO: Research why THF I need this async construction for this for drop selection
    loading.value = true;
    await updateResult(n);
    loading.value = false;
    return;
  }

  function dropSelect(event: Event) {
    const schedule = courseSchedule.value as CourseScheduleModel;
    const n = Number((event?.currentTarget as Element).getAttribute('key_k'));
    if (!course.value?.lessons[n].is_hidden) {
      selected.value = "-1";
      schedule.lessons[n].isSelected = false;
      return;
    }
    if (schedule.lessons[n].isSelected) {
      selected.value = "-1";
      schedule.lessons[n].isSelected = false;
      return;
    }
    return;
  }

  function changeLessonDate() {
    const cur_less_id = Number(cur_les_upd_id.value);
    if (set_custom_date.value === "") {
      courseSchedule.value?.lessons.splice((k_keeper.value as number), 1);
      st_modalVisible.value = false;
      return;
    }
    const schedule = _.cloneDeep(courseSchedule.value);
    const parsed = dateParse(set_custom_date.value);
    if (lessonsWOt.value.map(value => value.id).indexOf(cur_less_id) !== -1) {
      schedule.lessons.push({ date: parsed, lesson_id: cur_less_id, isSelected: false });
    } else {
      schedule.lessons[k_keeper.value as number].date = parsed;
    }
    courseSchedule.value = schedule;
    st_modalVisible.value = false;
  }

  async function updateResult(n: number) {
    const schedule = courseSchedule.value as CourseScheduleModel;
    const newArr = [...schedule.lessons];
    const tmp = newArr[Number(selected.value)];

    const date_tmp = newArr[Number(selected.value)].date;

    newArr[Number(selected.value)] = newArr[n];
    newArr[n] = tmp;

    newArr[n].date = newArr[Number(selected.value)].date;
    newArr[Number(selected.value)].date = date_tmp;

    newArr[n].isSelected = false;
    newArr[Number(selected.value)].isSelected = false;
    selected.value = null;
    courseSchedule.value = { ...schedule, lessons: newArr };
  }

  function saveOrUpdateSchedule(): void {
    updatingInProgress.value = true;
    const request = (isNewSchedule.value) ?
      api.post('/api/course-schedule/', courseSchedule.value) :
      api.patch(`/api/course-schedule/${courseSchedule.value?.id}/`, courseSchedule.value);
    request.then(answer => {
      notificationKind.value = 'success';
      notificationText.value = (isNewSchedule.value)
        ? 'Расписание успешно создано'
        : 'Расписание успешно изменено';
      courseSchedule.value = answer.data as CourseScheduleModel;
      oldCourseSchedule.value = _.cloneDeep(courseSchedule.value);
    }).catch(error => {
      notificationText.value = `Что-то пошло не так: ${error.message}`;
      notificationKind.value = 'error';
    }).finally(() => {
      showNotification.value = true;
      updatingInProgress.value = false;
    });

  }

  function revertChanges(): void {
    courseSchedule.value = _.cloneDeep(oldCourseSchedule.value);
  }

  function generateSchedule(): void {
    if (course.value === undefined)
      return;
    const parsed = (startDate.value || '').split('/').reverse().map((x) => Number(x));
    const date: Date = new Date(parsed[0], parsed[1] - 1, parsed[2]);
    const schedule = _.cloneDeep(courseSchedule.value);
    for (let i = 0; i < lessonsWOt.value.length; i++) {
      while (!Object.keys(workingDays.value).includes(((date.getDay() + 6) % 7).toString())) {
        date.setDate(date.getDate() + 1);
      }
      schedule.lessons.push(
        {
          date: date.getTime(), lesson_id: lessonsWOt.value[i].id, isSelected: false,
        } as ScheduleElement,
      );
      date.setDate(date.getDate() + 1);
    }
    selected.value = "-1";
    courseSchedule.value = _.cloneDeep(schedule);
  }


</script>

<style scoped lang="stylus">
.header
  color var(--cds-text-01)
  padding-bottom: 1.5rem
  padding-top: 1rem


.structured-list--data-wrapper
  display flex
  align-items center

.items-top
  background-color var(--cds-ui-01)
  padding var(--cds-spacing-05)

  &--element
    padding-bottom 10px

  .bx--structured-list-thead
    display none

.modal-container
  display flex
  flex-wrap wrap

.item
  min-height 85px


</style>
