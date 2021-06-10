<template>
  <cv-breadcrumb-item>
    <transition mode="out-in" name="fade">
      <cv-skeleton-text v-if="loading" class="skeleton" width="75px"/>
      <router-link v-else :to="{ name: PageView, props: model.id }">{{ title }}</router-link>
    </transition>
  </cv-breadcrumb-item>
</template>

<script lang="ts">
import { BaseModel } from '@/models/BaseModel';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class LmsBreadcrumbItem extends Vue {
  @Prop({ required: true }) model!: BaseModel;
  @Prop({ type: String, required: true }) PageView!: string;

  get loading() {
    return (!this.model)
  }

  get title() {
    return this.model?.name;
  }
}

</script>

<style lang="stylus" scoped>
.skeleton
  margin-bottom -.5rem


.fade-enter-active, .fade-leave-active
  transition opacity .1s

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */
  opacity 0
</style>
