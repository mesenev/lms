<template>
  <div class="empty-list">
    <div class="empty-list-wrapper">
      <component v-if="props.listOf === 'lessons' || props.listOf === 'problems' || props.listOf === 'courses'"
                 class="empty-list-icon" :is="ListChecked"/>
      <component v-else class="empty-list-icon" :is="Box"/>
      <h4 class="empty-title">Список пуст!</h4>
      <p class="empty-text">{{ props.text }}</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import ListChecked from '@carbon/icons-vue/es/list--checked/32';
import Box from '@carbon/icons-vue/es/box/32'

const props = defineProps({
  text: { type: String, required: true },
  listOf: { type: String, required: true }
})
</script>

<style scoped lang="stylus">
.empty-list-icon
  width 100px
  height 100px
  opacity 0.8

.empty
  &-title
    color var(--cds-text-01)

  &-list-icon
    color var(--cds-text-01)

  &-text
    color var(--cds-text-01)

</style>
