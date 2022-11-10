<template>
  <div class="empty-list">
    <div class="empty-list-wrapper">
      <component v-if="listOf === 'lessons' || listOf === 'problems' || listOf === 'courses'"
                 class="empty-list-icon" :is="ListChecked"/>
      <component v-else class="empty-list-icon" :is="Box"/>
      <h4 class="empty-title">Список пуст!</h4>
      <p class="empty-text">{{ text }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import ListChecked32 from '@carbon/icons-vue/es/list--checked/32';
import Box32 from '@carbon/icons-vue/es/box/32';


@Component({})
export default class EmptyListComponent extends Vue {
  @Prop({ required: true }) text!: string;
  @Prop({ required: true }) listOf!: string;

  ListChecked = ListChecked32;
  Box = Box32;
}
</script>

<style scoped lang="stylus">
.empty-list-icon
  width 100px
  height 100px
  opacity 0.8
</style>
