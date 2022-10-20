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
          <template slot="title">Редактирование расписания</template>
          <template slot="content">
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
          <template slot="primary-button">Сохранить изменения</template>
        </cv-modal>
      </div>
    </div>
    <div class="bx--row">
      <div class="items bx--col-lg-10 schedule-list">
        <cv-structured-list selectable @change="actionChange">
          <template slot="headings"></template>
          <template v-if="loading" slot="items">
            <cv-inline-loading/>
          </template>
          <template v-else slot="items">
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
                  <template slot="title">Установка собственного времени</template>
                  <template slot="content">
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

    <div v-if="lessonsWOt.length != 0" class="bx--row header no-schedule--wrapper">
      <div class="items-top bx--col-lg-10">
        <div class="items-top--element" v-if="!loading">
          <span>Уроки без установленного времени</span>
        </div>
        <cv-skeleton-text v-else :heading="true" :width="'35%'" class="main-title"/>
        <cv-structured-list>
          <template slot="headings"></template>
          <template v-if="loading" slot="items">
            <cv-loading/>
          </template>
          <template v-else slot="items">
            <cv-structured-list-item
              v-for="item in lessonsWOt"
              :key="item.id"
              :cur_key="item.id"
              :item="item">
              <template>
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
                    <template slot="title">Установка собственного времени</template>
                    <template slot="content">
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
                    <template slot="secondary-button">Отменить</template>
                    <template slot="primary-button">Сохранить изменения</template>
                  </cv-modal>
                </cv-structured-list-data>
                <cv-structured-list-data>{{ item.name }}</cv-structured-list-data>
              </template>
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

<script lang="ts">
import DateViewComponent from '@/components/common/DateViewComponent.vue';
import NotificationMixinComponent from '@/components/common/NotificationMixinComponent.vue';
import WeekDaysMixin from '@/views/management/CourseCalendarView/WeekDaysMixin.vue';
import DateComponent from '@/components/common/DateViewComponent.vue';
import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import CourseScheduleModel, { ScheduleElement } from '@/models/ScheduleModel';
import courseStore from '@/store/modules/course';
import Edit from '@carbon/icons-vue/es/edit/20';
import Back from '@carbon/icons-vue/es/skip--back/20';
import api from '@/store/services/api'
import _ from 'lodash';
import { mixins } from 'vue-class-component';
import { Component, Prop } from 'vue-property-decorator';
import { dateParse } from '@/utils/utils';

@Component({ components: { DateViewComponent, Edit, Back } })
export default class CourseCalendarView extends mixins(NotificationMixinComponent, WeekDaysMixin) {
  @Prop({ required: true }) courseId!: number;
  courseStore = courseStore;
  course: CourseModel = {} as CourseModel;
  courseSchedule: CourseScheduleModel =
    {
      id: NaN, name: '', course: this.course.id, lessons: [], start_date: '', week_schedule: {},
    } as CourseScheduleModel;
  oldCourseSchedule: CourseScheduleModel = _.cloneDeep(this.courseSchedule);
  iconEdit = Edit;
  iconBack = Back;
  modalVisible = false;
  st_modalVisible = false;
  startDate: string | null = null;
  changedStartDate: string | null = null;
  set_custom_date = "";
  set_custom_time: string | null = null;
  cur_custom_date: string | null = null;
  selected: string | null = null;
  loading = true;
  cur_les_upd_id = "";
  k_keeper: number | null = null;
  courseListId = null;
  updatingInProgress = false;
  newSchedule: Record<string, string | null> = {};
  private schedule: Record<string, string | null> = {
    0: null, 1: null, 2: null, 3: null, 4: null, 5: null, 6: null,
  }

  get calOptions(): object {
    return { dateFormat: 'd/m/Y' };
  }

  get scheduleChangedAndNotEmpty(): boolean {
    return !_.isEqual(this.courseSchedule, this.oldCourseSchedule)
      && !!(this.courseSchedule.lessons.length > 0);
  }


  get isNewSchedule() {
    return !this.courseSchedule.id;
  }

  get currentScheduledDays() {
    let courseSchedule = '';
    Object.keys(this.workingDays).forEach(
      value => courseSchedule += `${this.alias[parseInt(value)]}: ${this.workingDays[value]} `,
    );
    return courseSchedule;
  }

  get isScheduleChanged() {
    return Object.values(this.newSchedule).filter(x => typeof (x) === 'string').length > 0
      && !!this.changedStartDate && (
        !_.isEqual(this.schedule, this.newSchedule)
        || !_.isEqual(this.startDate, this.changedStartDate)
      );
  }

  get isSelfDateChanged() {
    return !(this.set_custom_date == this.cur_custom_date);
  }

  get lessons(): Array<LessonModel> {
    if (this.loading || !this.course.id)
      return [];
    return this.course.lessons;
  }

  get scheduledLessons(): ScheduleElement[] {
    function compare(a: ScheduleElement, b: ScheduleElement) {
      if (a.date > b.date) return 1;
      if (a.date < b.date) return -1;
      return 0;
    }

    return this.courseSchedule.lessons.sort(compare);
  }

  get lessonsWOt(): LessonModel[] {
    if (this.loading || !this.course.id)
      return [];
    const ids = this.scheduledLessons.map(value => Number(value.lesson_id));
    return this.course.lessons.filter(value => ids.indexOf(Number(value.id)) === -1);
  }

  lessonById(id: number): LessonModel {
    return this.lessons.find(x => Number(x.id) === Number(id)) as LessonModel;
  }

  get workingDays(): Record<string, string> {
    if (!this.schedule) return {};
    return Object.keys(this.schedule)
      .filter(key => this.schedule[key] != null)
      .reduce((obj: Record<string, string>, key: string) => {
        obj[key] = this.schedule[key] as string;
        return obj;
      }, {});
  }

  async created() {
    this.course = await this.courseStore.fetchCourseById(this.courseId);
    this.courseSchedule.course = this.course.id;
    this.oldCourseSchedule.course = this.course.id;
    if (!this.course.id || typeof (this.course.schedule) !== 'number') {
      this.loading = false;
      return;
    }
    this.courseSchedule = await this.courseStore.fetchCourseScheduleByCourseId(this.courseId);
    this.oldCourseSchedule = _.cloneDeep(this.courseSchedule);
    this.startDate = this.courseSchedule.start_date;
    this.schedule = this.courseSchedule.week_schedule;
    if (this.courseSchedule.lessons)
      for (let i = 0; i < this.courseSchedule.lessons.length; i++)
        this.courseSchedule.lessons[i].isSelected = false;
    this.loading = false;
  }


  onUpdateTime(n: number) {
    return (value: string) => this.newSchedule = { ...this.newSchedule, [n]: value };
  }


  showModal() {
    this.newSchedule = { ...this.schedule };
    this.changedStartDate = this.startDate;
    this.modalVisible = true;
  }

  async st_showModal(event: PointerEvent) {
    this.st_modalVisible = true;
    const element = (event?.currentTarget as Element);
    this.cur_les_upd_id = element.getAttribute('cur_key') as string;
    this.set_custom_date = "";
    this.cur_custom_date = "";
    if (element.getAttribute('key_k') !== null) {
      this.k_keeper = Number(element.getAttribute('key_k'));
      const currentDate = (this.courseSchedule as CourseScheduleModel).lessons[this.k_keeper].date;
      const date = new Date(currentDate);
      this.set_custom_date = date.toISOString()
      this.cur_custom_date = this.set_custom_date;
    }
    if (this.cur_les_upd_id === null) {
      throw Error();
    }

  }

  actionHidden() {
    this.modalVisible = false;
  }

  st_actionHidden() {
    this.st_modalVisible = false;
  }

  changeSchedule() {
    this.modalVisible = false;
    this.schedule = { ...this.newSchedule };
    this.startDate = this.changedStartDate;
    this.generateSchedule();
  }

  async actionChange(obj: string) {
    const schedule = this.courseSchedule as CourseScheduleModel;
    const n = schedule.lessons.findIndex(x => x.lesson_id === Number(obj));
    if (!this.course?.lessons[n].is_hidden) {
      alert("Изменять время открытого урока невозможно");
      this.selected = "-1";
      schedule.lessons[n].isSelected = false;
      return;
    } else if (!this.selected || this.selected == "-1") {
      this.selected = n.toString();
      schedule.lessons[n].isSelected = true;
      return;
    }
    // TODO: Research why THF I need this async construction for this for drop selection
    this.loading = true;
    await this.updateResult(n);
    this.loading = false;
    return;
  }

  dropSelect(event: Event) {
    const schedule = this.courseSchedule as CourseScheduleModel;
    const n = Number((event?.currentTarget as Element).getAttribute('key_k'));
    if (!this.course?.lessons[n].is_hidden) {
      this.selected = "-1";
      schedule.lessons[n].isSelected = false;
      return;
    }
    if (schedule.lessons[n].isSelected) {
      this.selected = "-1";
      schedule.lessons[n].isSelected = false;
      return;
    }
    return;
  }

  changeLessonDate() {
    const cur_less_id = Number(this.cur_les_upd_id);
    if (this.set_custom_date === "") {
      this.courseSchedule?.lessons.splice((this.k_keeper as number), 1);
      this.st_modalVisible = false;
      return;
    }
    const schedule = _.cloneDeep(this.courseSchedule);
    const parsed = dateParse(this.set_custom_date);
    if (this.lessonsWOt.map(value => value.id).indexOf(cur_less_id) !== -1) {
      schedule.lessons.push({ date: parsed, lesson_id: cur_less_id, isSelected: false })
    } else {
      schedule.lessons[this.k_keeper as number].date = parsed;
    }
    this.courseSchedule = schedule;
    this.st_modalVisible = false;
  }

  private alias = [
    'Понедельник', 'Вторник', "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье",
  ];

  async updateResult(n: number) {
    const schedule = this.courseSchedule as CourseScheduleModel;
    const newArr = [...schedule.lessons];
    const tmp = newArr[Number(this.selected)];

    const date_tmp = newArr[Number(this.selected)].date;

    newArr[Number(this.selected)] = newArr[n];
    newArr[n] = tmp;

    newArr[n].date = newArr[Number(this.selected)].date;
    newArr[Number(this.selected)].date = date_tmp;

    newArr[n].isSelected = false;
    newArr[Number(this.selected)].isSelected = false;
    this.selected = null;
    this.courseSchedule = { ...schedule, lessons: newArr };
  }

  saveOrUpdateSchedule(): void {
    this.updatingInProgress = true;
    const request = (this.isNewSchedule) ?
      api.post('/api/course-schedule/', this.courseSchedule) :
      api.patch(`/api/course-schedule/${this.courseSchedule?.id}/`, this.courseSchedule);
    request.then(answer => {
      this.notificationKind = 'success';
      this.notificationText = (this.isNewSchedule)
        ? 'Расписание успешно создано'
        : 'Расписание успешно изменено';
      this.courseSchedule = answer.data as CourseScheduleModel;
      this.oldCourseSchedule = _.cloneDeep(this.courseSchedule);
    }).catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.notificationKind = 'error';
    }).finally(() => {
      this.showNotification = true;
      this.updatingInProgress = false;
    });

  }

  revertChanges(): void {
    this.courseSchedule = _.cloneDeep(this.oldCourseSchedule);
  }

  generateSchedule(): void {
    if (this.course === undefined)
      return;
    const parsed = (this.startDate || '').split('/').reverse().map((x) => Number(x));
    const date: Date = new Date(parsed[0], parsed[1] - 1, parsed[2]);
    const schedule = _.cloneDeep(this.courseSchedule);
    for (let i = 0; i < this.lessonsWOt.length; i++) {
      while (!Object.keys(this.workingDays).includes(((date.getDay() + 6) % 7).toString())) {
        date.setDate(date.getDate() + 1);
      }
      schedule.lessons.push(
        {
          date: date.getTime(), lesson_id: this.lessonsWOt[i].id, isSelected: false,
        } as ScheduleElement,
      );
      date.setDate(date.getDate() + 1);
    }
    this.selected = "-1";
    this.courseSchedule = _.cloneDeep(schedule);
  }
}


</script>

<style scoped lang="stylus">
.header
  padding-bottom: 1.5rem
  padding-top: 1rem


.structured-list--data-wrapper
  display flex
  align-items center

.items-top
  background-color var(--cds-ui-02)
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
