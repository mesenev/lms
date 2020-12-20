<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>Расписание занятий</h1>
    </div>
    <div class="bx--row header">
      <div class="items bx--col-lg-10">
        <span>
          {{ scheduleCurrent }}
          <cv-icon-button
            v-on:click="showModal" kind="secondary" tip-position="hidden"
            :icon="icon" size='small'
          />
        </span>

        <cv-modal
          close-aria-label="Закрыть"
          :visible="modalVisible"
          @modal-hidden="actionHidden"
          :auto-hide-off="false">
          <template slot="title">Редактирование расписания</template>
          <template slot="content">
            <div class="modal-container">
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
              <div class="daytime-container">
                <cv-checkbox label="Воскресенье" value='123' v-model="sunday"/>
                <cv-time-picker
                  label="" ampm="24" :disabled="!sunday"
                  :time.sync="newSchedule[6]" :form-item="true"/>
              </div>
            </div>
          </template>
          <template :active="isScheduleChanged" slot="primary-button">Сохранить изменения</template>
        </cv-modal>


      </div>
    </div>
    <div class="bx--row">
      <div class="items bx--col-lg-10">
        <cv-tabs selected="0" aria-label="Tabs navigation">
          <cv-tab label="1 Семестр">
            <p class="landing-page__p">
              Carbon is IBM’s open-source design system for digital
              products and experiences. With the IBM Design Language as
              its foundation, the system consists of working code, design
              tools and resources, human interface guidelines, and a
              vibrant community of contributors.
            </p>
          </cv-tab>
          <cv-tab label="2 Семестр">
            <p class="landing-page__p">
              <span class="10">Lorem ipsum dolor sit amet,
                consectetur adipisicing elit.
                Molestias obcaecati
                officiis pariatur quibusdam quo ratione, sapiente vel veniam?
                Consequatur debitis incidunt
                inventore, ipsa iusto maiores temporibus vero voluptates?
                Alias, cupiditate?</span>
            </p>
          </cv-tab>
        </cv-tabs>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Prop, Component, Vue } from 'vue-property-decorator';
import Edit from '@carbon/icons-vue/es/edit/20';
import _ from 'lodash';

@Component({ components: { Edit } })
export default class CourseCalendarView extends Vue {
  @Prop() courseId!: number;
  public icon = Edit;
  public modalVisible = false;

  private monday_ = false;
  private tuesday_ = false;
  private wednesday_ = false;
  private thursday_ = false;
  private friday_ = false;
  private saturday_ = false;
  private sunday_ = false;

  set monday(value: boolean) {
    this.monday_ = value;
    this.newSchedule = { ...this.newSchedule, 0: null };
  }

  get monday() {
    return this.monday_;
  }


  get tuesday() {
    return this.tuesday_;
  }

  set tuesday(value: boolean) {
    this.tuesday_ = value;
    this.newSchedule = { ...this.newSchedule, 1: null };
  }


  get wednesday() {
    return this.wednesday_;
  }

  set wednesday(value: boolean) {
    this.wednesday_ = value;
    this.newSchedule = { ...this.newSchedule, 2: '00:00' };
  }


  get thursday() {
    return this.thursday_;
  }

  set thursday(value: boolean) {
    this.thursday_ = value;
    this.newSchedule = { ...this.newSchedule, 3: '00:00' };
  }


  get friday() {
    return this.friday_;
  }

  set friday(value: boolean) {
    this.friday_ = value;
    this.newSchedule = { ...this.newSchedule, 4: '00:00' };
  }


  get saturday() {
    return this.saturday_;
  }

  set saturday(value: boolean) {
    this.saturday_ = value;
    this.newSchedule = { ...this.newSchedule, 5: '00:00' };
  }

  onUpdateTime(n: number) {
    return (value: string) => this.newSchedule = { ...this.newSchedule, [n]: value };
  }

  get sunday() {
    return this.sunday_;
  }

  set sunday(value: boolean) {
    this.sunday_ = value;
    this.newSchedule = { ...this.newSchedule, 5: '00:00' };
  }

  private schedule: Record<string, string | null> = {
    0: null, 1: null, 2: null, 3: null, 4: null, 5: null, 6: null, 7: null,
  }
  private newSchedule: Record<string, string | null> = {};

  showModal() {
    this.newSchedule = this.schedule;
    this.modalVisible = true;
  }

  actionHidden() {
    this.modalVisible = false;
    this.schedule = this.newSchedule;
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

  get scheduleCurrent() {
    let result = '';
    Object.keys(this.workingDays).forEach(
      value => result += `${this.alias[parseInt(value)]}: ${this.workingDays[value]}`,
    );
    return result;
  }

  get isScheduleChanged() {
    return !_.isEqual(this.schedule, this.newSchedule);
  }

}
</script>

<style scoped lang="stylus">
.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.items
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

  .bx--structured-list-thead
    display none

.modal-container
  display flex
  flex-wrap wrap

.daytime-container
  padding-bottom 5px
  display inline-flex

.item
  min-height 85px
</style>
