<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>Расписание занятий</h1>
    </div>
    <div class="bx--row header">
      <div class="items bx--col-lg-10">
        <span>
          Понедельник: 15:30-16:00, Вторник: 8:30-10:00
          <cv-icon-button v-on:click="showModal" kind="secondary" tip-position="hidden" :icon="icon" size='small'/>
        </span>

        <cv-modal
          close-aria-label="Закрыть"
          :visible="modalVisible"
          @modal-hidden="actionHidden"
          @modal-hide-request="actionHideRequest"
          @after-modal-hidden="actionAfterHidden"
          :auto-hide-off="false">
          <template slot="title">Выберите дни и время</template>
          <template slot="content"><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, seed
            do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
            exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p></template>
          <template v-if="use_primaryButton" slot="primary-button">primary</template>
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

@Component({ components: { Edit } })
export default class CourseCalendarView extends Vue {
  @Prop() courseId!: number;
  public icon = Edit;
  public modalVisible = false;

  showModal() {
    this.modalVisible = true;
  }
  actionHidden() {
    this.modalVisible = false;
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
