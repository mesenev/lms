<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>Расписание занятий</h1>
    </div>
    <div class="bx--row header">
      <div class="items bx--col-lg-10">
        <span>
          {{ scheduleCurrent }}
          <cv-icon-button v-on:click="showModal" kind="secondary" tip-position="hidden" :icon="icon" size='small'/>
        </span>

        <cv-modal
          close-aria-label="Закрыть"
          :visible="modalVisible"
          @modal-hidden="actionHidden"
          @modal-hide-request="actionHideRequest"
          @after-modal-hidden="actionAfterHidden"
          :auto-hide-off="false">
          <template slot="title">Редактирование расписания</template>
          <template slot="content">
            <div>
              <cv-checkbox label="Понедельник" :checked="checked" :value=""/>
            </div>
          </template>
          <template v-if="use_primaryButton" :active="isScheduleChanged" slot="primary-button">Сохранить изменения</template>
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

  private schedule: Record<string, string | null> = {
    1: null, 2: null, 3: null, 4: null, 5: null, 6: null, 7: null,
  }
  private newSchedule: Record<string, string | null> = {};

  showModal() {
    this.newSchedule = this.schedule;
    this.modalVisible = true;
  }

  actionHidden() {
    this.modalVisible = false;
  }
  activateDay(day: number) {
    return() => {
      this.newSchedule = {...this.newSchedule, [day]: '00:00'};
    }
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
      value => result += `${this.alias[parseInt(value) - 1]}: ${this.workingDays[value]}`,
    );
    return result;
  }

  get isScheduleChanged(){
    return
  }

}
</script>

<style lang="stylus">
.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.items
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

  .bx--structured-list-thead
    display none

.item
  min-height 85px
</style>
