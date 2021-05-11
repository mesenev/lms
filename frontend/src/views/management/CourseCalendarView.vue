<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>Расписание занятий</h1>
    </div>
    <div class="bx--row header">
      <div class="items-top bx--col-lg-10">
        <div class="items-top--element"><span>Начало занятий: {{ startDate || ":warning:" }}</span></div>
        <hr>
        <div class="items-top--element"><span> {{ scheduleCurrent }}</span></div>
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
                    :cal-options="dpOptions"
                    date-format="d/m/Y"
                    placeholder="dd/mm/yyyy"
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
      <div class="items bx--col-lg-10">
        <cv-structured-list selectable @change="actionChange">
          <template slot="headings"></template>
          <template v-if="!loading && courseSchedule && courseSchedule.lessons"
                    slot="items">
            <cv-structured-list-item
              v-for="(record, index) in courseSchedule.lessons"
              :key="index" :checked="record.isSelected" :value="record.lesson.id.toString()"
              name="group">
              <cv-structured-list-data>{{ record.date }}</cv-structured-list-data>
              <cv-structured-list-data>{{ record.lesson.name }}</cv-structured-list-data>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
      </div>
    </div>
    <div class="save-button">
      <cv-button-set>
        <cv-button kind="secondary">Отменить</cv-button>
        <cv-button :disabled="!scheduleChanged" kind="primary" v-on:click="saveOrUpdateSchedule">
          {{ (isNewSchedule) ? "Создать расписание" : "Сохранить изменения" }}
        </cv-button>
      </cv-button-set>
    </div>
  </div>
</template>

<script lang="ts">
import NotificationMixinComponent from '@/components/common/NotificationMixinComponent.vue';
import CourseModel from '@/models/CourseModel';
import CourseScheduleModel, { ScheduleElement } from '@/models/ScheduleModel';
import courseStore from '@/store/modules/course';
import Edit from '@carbon/icons-vue/es/edit/20';
import Back from '@carbon/icons-vue/es/skip--back/20';
import axios from 'axios';
import _ from 'lodash';
import { mixins } from 'vue-class-component';
import { Component, Prop } from 'vue-property-decorator';


@Component({ components: { Edit, Back } })
export default class CourseCalendarView extends mixins(NotificationMixinComponent) {
  @Prop({ required: true }) courseId!: number;
  courseStore = courseStore;
  courseSchedule: CourseScheduleModel | null = null;
  oldCourseSchedule: CourseScheduleModel | null = null;
  iconEdit = Edit;
  iconBack = Back;
  modalVisible = false;
  startDate: string | null = null;
  changedStartDate: string | null = null;
  selected: string | null = null;
  loading = true;

  private monday_ = false;
  private tuesday_ = false;
  private wednesday_ = false;
  private thursday_ = false;
  private friday_ = false;
  private saturday_ = false;
  private sunday_ = false;

  get scheduleChanged(): boolean {
    return !_.isEqual(this.courseSchedule, this.oldCourseSchedule);
  }

  get isNewSchedule() {
    return !this.courseSchedule?.id;
  }

  get course(): CourseModel {
    return this.courseStore.currentCourse as CourseModel;
  }

  get scheduleCurrent() {
    let courseSchedule = '';
    Object.keys(this.workingDays).forEach(
      value => courseSchedule += `${this.alias[parseInt(value)]}: ${this.workingDays[value]} `,
    );
    return courseSchedule;
  }

  get isScheduleChanged() {
    return !!this.changedStartDate && (
      !_.isEqual(this.schedule, this.newSchedule)
      || !_.isEqual(this.startDate, this.changedStartDate)
    );
  }

  get dpOptions() {
    return {
      dateFormat: "d/m/Y",
    };
  }

  async created() {
    if (this.course.schedule) {
      this.courseSchedule = await this.courseStore.fetchCourseScheduleByCourseId(this.course.id);
      this.oldCourseSchedule = { ...this.courseSchedule };
      //TODO: Same data in two fields. Ambigous. Normalize it.
      this.startDate = this.courseSchedule.start_date;
      this.schedule = this.courseSchedule.week_schedule;
      //TODO: correct init state for days (modal init state)
    }
    this.loading = false;
  }

  set monday(value: boolean) {
    this.monday_ = value;
    this.newSchedule = { ...this.newSchedule, 0: (value) ? '00:00' : null };
  }

  get monday() {
    return this.monday_;
  }


  get tuesday() {
    return this.tuesday_;
  }

  set tuesday(value: boolean) {
    this.tuesday_ = value;
    this.newSchedule = { ...this.newSchedule, 1: (value) ? '00:00' : null };
  }


  get wednesday() {
    return this.wednesday_;
  }

  set wednesday(value: boolean) {
    this.wednesday_ = value;
    this.newSchedule = { ...this.newSchedule, 2: (value) ? '00:00' : null };
  }


  get thursday() {
    return this.thursday_;
  }

  set thursday(value: boolean) {
    this.thursday_ = value;
    this.newSchedule = { ...this.newSchedule, 3: (value) ? '00:00' : null };
  }


  get friday() {
    return this.friday_;
  }

  set friday(value: boolean) {
    this.friday_ = value;
    this.newSchedule = { ...this.newSchedule, 4: (value) ? '00:00' : null };
  }


  get saturday() {
    return this.saturday_;
  }

  set saturday(value: boolean) {
    this.saturday_ = value;
    this.newSchedule = { ...this.newSchedule, 5: (value) ? '00:00' : null };
  }

  onUpdateTime(n: number) {
    return (value: string) => this.newSchedule = { ...this.newSchedule, [n]: value };
  }

  get sunday() {
    return this.sunday_;
  }

  set sunday(value: boolean) {
    this.sunday_ = value;
    this.newSchedule = { ...this.newSchedule, 6: (value) ? '00:00' : null };
  }

  private schedule: Record<string, string | null> = {
    0: null, 1: null, 2: null, 3: null, 4: null, 5: null, 6: null,
  }
  private newSchedule: Record<string, string | null> = {};

  showModal() {
    this.newSchedule = { ...this.schedule };
    this.changedStartDate = this.startDate;
    this.modalVisible = true;
  }

  actionHidden() {
    this.modalVisible = false;
  }

  changeSchedule() {
    this.modalVisible = false;
    this.schedule = { ...this.newSchedule };
    this.startDate = this.changedStartDate;
    this.generateSchedule();
  }

  async actionChange(obj: string) {
    const schedule = this.courseSchedule as CourseScheduleModel;
    const n = schedule.lessons.findIndex(x => x.lesson.id === Number(obj));
    if (!this.selected) {
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

  get workingDays() {
    return Object.keys(this.schedule)
      .filter(key => this.schedule[key] != null)
      .reduce((obj: Record<string, string>, key: string) => {
        obj[key] = this.schedule[key] as string;
        return obj;
      }, {});
  }

  private alias = [
    'Понедельник', 'Вторник', "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье",
  ];

  async updateResult(n: number) {
    const schedule = this.courseSchedule as CourseScheduleModel;
    const newArr = [...schedule.lessons];
    const tmp = newArr[Number(this.selected)];
    newArr[Number(this.selected)] = newArr[n];
    newArr[n] = tmp;
    newArr[n].isSelected = false;
    newArr[Number(this.selected)].isSelected = false;
    this.selected = null;
    this.courseSchedule = { ...schedule, lessons: newArr };
  }

  saveOrUpdateSchedule(): void {
    const request = (this.isNewSchedule) ?
      axios.post('/api/course-schedule/', this.courseSchedule) :
      axios.patch(`/api/course-schedule/${this.courseSchedule?.id}/`, this.courseSchedule);
    request.then(answer => {
      this.notificationKind = 'success';
      this.notificationText = (this.isNewSchedule)
        ? 'Расписание успешно создано'
        : 'Расписание успешно изменено';
      this.courseSchedule = answer.data as CourseScheduleModel;
      this.oldCourseSchedule = { ...this.courseSchedule };
    }).catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.notificationKind = 'error';
    }).finally(() => this.showNotification = true);
  }

  generateSchedule(): void {
    if (Object.keys(this.schedule).length === 0 || this.startDate === null)
      return;
    const lessons = this.course.lessons;
    const parsed = this.startDate.split('/').reverse().map((x) => Number(x));
    const date: Date = new Date(parsed[0], parsed[1], parsed[2]);
    const schedule: CourseScheduleModel = {
      id: NaN,
      name: '',
      course: this.course.id,
      lessons: [],
      start_date: this.startDate as string,
      week_schedule: this.schedule,
    }
    for (let i = 0; i < lessons.length; i++) {
      while (!Object.keys(this.workingDays).includes(((date.getDay() + 6) % 7).toString())) {
        date.setDate(date.getDate() + 1);
      }
      schedule.lessons.push({
          date: date.toLocaleDateString(
            'ru-RU',
            { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' },
          ),
          lesson: lessons[i],
          isSelected: false,
        } as ScheduleElement,
      )
      date.setDate(date.getDate() + 1);
    }
    this.courseSchedule = schedule;
  }
}


</script>

<style scoped lang="stylus">
.header
  padding-bottom: 1.5rem
  padding-top: 1rem


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
