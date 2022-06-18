<template>
  <li class="status" :class="{'status-ok': isAccepted,
                 'status-wa': isRejected,
                 'status-np': !(isAccepted || isRejected)}">
    <div class="status-back"></div>
    <a :href="'../../'+problem.id">
      <svg v-if="isAccepted"
        viewBox="0 0 18 15" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 6.86325L7.36816 13.1846L17 1.5" stroke-width="2"></path></svg>
      <svg v-else-if="isRejected"
        viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><path d="M1 1L15 15M15 1L1 15" stroke-width="2"/></svg>
      <div v-else>?</div>
    </a>
  </li>
</template>

<script lang="ts">
import ProblemModel from "@/models/ProblemModel";
import { Component, Prop, Vue } from 'vue-property-decorator';
import {SUBMIT_STATUS} from "@/models/SubmitModel";

@Component({ components: {} })
export default class ProblemNavigationItem extends Vue {
  @Prop({ required: true }) problem!: ProblemModel;


  get getStatus(): string | undefined {
    return this.problem.last_submit?.status;
  }
  get isAccepted() {
    return this.getStatus === SUBMIT_STATUS.OK;
  }
  get isRejected() {
    return this.getStatus === SUBMIT_STATUS.WRONG_ANSWER;
  }


}
</script>

<style lang="stylus" scoped>
li
  border-radius 50px
  text-align center
  width 32px
  height 32px
  line-height 32px
  margin-bottom 1rem

.status
  width 24px
  height 24px
  line-height 24px
  margin 0.5rem 4px 0 4px
  position relative
  box-sizing border-box

  a
    position relative
    z-index 1
    display block
    width 100%
    height 100%

    &:focus
      outline none

  svg
    stroke white

  &-back
    width 28px
    height 28px
    position absolute
    top -2px
    left -2px
    border 1px solid #808080
    border-radius 50px
    display none

  &-ok
    background-color #4EB052
    svg
      width 18px
      height 18px
      margin 3px
  &-wa
    background-color #DA1E28
    svg
      width 16px
      height 16px
      margin 4px
  &-np
    background-color transparent
    border 1px #808080 solid
    a
      color black
      text-decoration none
      &:hover
        text-decoration 1px underline


  &-np &-back
    top -3px
    left -3px
  &:hover &-back
    display unset
</style>
