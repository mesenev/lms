<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>Отправленные решения</h1>
    </div>
    <div class=" bx--row">
      <div class="items bx--col-lg-8">
        <cv-search
          label="label"
          placeholder="search"
        >
        </cv-search>
        <div>
          <span>work in process</span>
        </div>
      </div>
      <div class="bx--col-lg-8">
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class SolutionsListView extends Vue {
  @Prop() courseId!: number;
}
</script>

<style lang="stylus" scoped>
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
