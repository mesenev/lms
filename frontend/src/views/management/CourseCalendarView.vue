<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>Расписание занятий</h1>
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
              <span class="10">Lorem ipsum dolor sit amet, consectetur adipisicing elit.
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

@Component({ components: {} })
export default class CourseCalendarView extends Vue {
  @Prop() courseId!: number;

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
