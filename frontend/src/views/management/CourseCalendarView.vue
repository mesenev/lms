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
          <template v-if="!loading && courseSchedule"
                    slot="items">
            <cv-structured-list-item
              v-for="(record, index) in courseSchedule"
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
        <cv-button :disabled="scheduleChanged" kind="primary">
          {{ (isNewSchedule) ? "Создать расписание" : "Сохранить изменения"
        </cv-button>
      </cv-button-set>
    </div>
  </div>
</template>

<script lang="ts">
import NotificationMixinComponent from '@/components/common/NotificationMixinComponent.vue';
import CourseModel from '@/models/CourseModel';
import LessonModel from '@/models/LessonModel';
import courseStore from '@/store/modules/course';
import Edit from '@carbon/icons-vue/es/edit/20';
import Back from '@carbon/icons-vue/es/skip--back/20';
import axios from 'axios';
import _ from 'lodash';
import { mixins } from 'vue-class-component';
import { Component, Prop } from 'vue-property-decorator';

interface ScheduleElement {
  date: string;
  lesson: LessonModel;
  isSelected: boolean;
}

@Component({ components: { Edit, Back } })
export default class CourseCalendarView extends mixins(NotificationMixinComponent) {
  @Prop({ required: true }) courseId!: number;
  courseStore = courseStore;
  courseSchedule: Array<ScheduleElement> = [];
  oldCourseSchedule: Array<ScheduleElement> = [];
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
    //
  }

  get course(): CourseModel {
    return this.courseStore.currentCourse;
  }

  get scheduleCurrent() {
    let courseSchedule = '';
    Object.keys(this.workingDays).forEach(
      value => courseSchedule += `${this.alias[parseInt(value)]}: ${this.workingDays[value]} `,
    );
    return courseSchedule;
  }

  async getSchedule() {
    //
  }

  created() {
    this.course = this.courseStore.currentCourse;
    this.oldCourseSchedule = this.course.schedule;
    this.loading = false;
  }

  async actionChange(obj: string) {
    const n = this.courseSchedule.findIndex(x => x.lesson.id === Number(obj));
    if (!this.selected) {
      this.selected = n.toString();
      this.courseSchedule[n].isSelected = true;
      return;
    }
    this.loading = true;
    // TODO: Research why THF I need async function for this
    await this.updateResult(n);
    this.loading = false;
    return;
  }

  async updateResult(n: number) {
    const newArr = [...this.courseSchedule];
    const tmp = newArr[Number(this.selected)];
    newArr[Number(this.selected)] = newArr[n];
    newArr[n] = tmp;
    newArr[n].isSelected = false;
    newArr[Number(this.selected)].isSelected = false;
    this.courseSchedule = [];
    this.selected = null;
    this.courseSchedule = [...newArr];
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

  saveOrUpdateSchedule(): void {
    const request = (this.isNewSchedule) ?
      axios.post('/api/course-schedule/', this.courseSchedule) :
      axios.patch(`/api/course-schedule/${this.courseSchedule.id}/`, this.courseSchedule);
    request.then(() => {
      this.notificationKind = 'success';
      this.notificationText = (this.isNewSchedule)
        ? 'Расписание успешно создано'
        : 'Расписание успешно изменено';
    }).catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.notificationKind = 'error';
    }).finally(() => this.showNotification = true);
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

  generateSchedule(): void {
    if (Object.keys(this.schedule).length === 0 || this.startDate === null)
      return;
    const lessons = this.course.lessons;
    const date = new Date(Date.parse(this.startDate));
    const schedule: ScheduleElement[] = [];
    for (let i = 0; i < lessons.length; i++) {
      while (!Object.keys(this.workingDays).includes(((date.getDay() + 6) % 7).toString())) {
        date.setDate(date.getDate() + 1);
      }
      schedule.push({
        date: date.toLocaleDateString(
          'ru-RU',
          { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' },
        ),
        lesson: lessons[i],
        isSelected: false,
      })
      date.setDate(date.getDate() + 1);
    }
    this.courseSchedule = schedule;
  }

  get isScheduleChanged() {
    return !_.isEqual(this.schedule, this.newSchedule)
      || !_.isEqual(this.startDate, this.changedStartDate);
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
