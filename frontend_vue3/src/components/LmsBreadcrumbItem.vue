<template>
  <cv-breadcrumb-item>
    <transition mode="out-in" name="fade">
      <cv-skeleton-text v-if="loading" class="skeleton" width="75px"/>
      <router-link v-else :to="{ name: pageView, props: model.id }">{{ title }}</router-link>
    </transition>
  </cv-breadcrumb-item>
</template>

<script lang="ts" setup>
import type {BaseModel} from '@/models/BaseModel';
import type {PropType} from "vue";
import {computed} from "vue";

const props = defineProps({
  model: {type: Object as PropType<BaseModel>, required: true},
  pageView: {type: String, required: true}
})

const loading = computed(() => {
  return (!props.model)
})

const title = computed(() => {
  return props.model?.name;
})
</script>

<style lang="stylus" scoped>
.skeleton
  margin-bottom -.5rem

.fade-enter-active, .fade-leave-active
  transition opacity .1s

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */
  opacity 0
</style>
