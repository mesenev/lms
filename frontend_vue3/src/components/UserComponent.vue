<script lang="ts">
import {UserModel} from "@/models/UserModel";
import useUserStore from '@/store/modules/user';
import useCourseStore from '@/store/modules/course';

</script>

<template>
  <div class="user-component">
    <div class="user-component--wrapper">
      <img alt="" class="user-component--avatar" v-bind:src="picUrl"/>
      <div class="user-component--name">
        <cv-inline-loading v-if="loading" active/>
        <span v-else>{{ name }}</span>
      </div>
      <div v-if="warning" class="user-component--warning">
        <cv-tooltip tip="Пользователь не является студентом курса"/>
      </div>
    </div>
  </div>
</template>

<style scoped lang="stylus">
.user-component
  width 200px
  height 32px

  &--wrapper
    display flex
    flex-flow row
    align-items center

  &--avatar
    height 32px
    width 32px
    border-radius: 150%
    padding 0
    margin 0

  &--name
    padding-left var(--cds-spacing-02)

  &--warning
    padding-left var(--cds-spacing-02)
    display flex
    align-items center

</style>
