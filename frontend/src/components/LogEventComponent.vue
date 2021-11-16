<template>
  <cv-structured-list-item class="author-message">
    <img src="" alt="'avatar'" class="avatar student">
    <a href="#" class="button">{{ this.message.text }}</a>
    <br>
  </cv-structured-list-item>
</template>

<script lang="ts">
import LogEventModel from "@/models/LogEventModel";
import userStore from '@/store/modules/user';
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import { Component, Prop } from "vue-property-decorator";


@Component({ components: {} })
export default class LogEventComponent extends NotificationMixinComponent {
  @Prop({ required: true }) message!: LogEventModel;
  userStore = userStore;

  get isStaff() {
    return this.message.sender.staff_for.includes(this.message?.courseId);
  }

  get senderAvatar() {
    return this.message.sender.avatar_url;
  }
}

</script>

<style scoped lang="stylus">

.button
  display: inline-block
  padding: 0.75em
  margin 0.00002em
  color: #fff
  font-size: 0.8em
  text-decoration none
  position: relative
  overflow: hidden
  z-index: 1

  &:after
    content: ''
    position: absolute
    bottom: 0
    left: 0
    width: 100%
    height: 100%
    background-color: gray
    z-index: -2

  &:hover
    color: #fff

    &:before
      width: 100%


.avatar
  width 2em
  margin-bottom 0.3em

.student
  margin-right 1em

.stuff
  margin-left 1em

</style>
