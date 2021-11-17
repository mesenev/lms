<template>
  <cv-structured-list-item style="border: none">
    <div class="one-history-point">
       {{message.text}}
    </div>
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


.avatar
  width 2em
  margin-bottom 0.3em

.student
  margin-right 1em

.stuff
  margin-left 1em

.one-history-point
  word-break break-after
  font-size 1em
  padding 5px
  margin 20px
  background white
  border 1px solid rgba(0, 0, 0, 0.3)
  border-radius 5px
  min-height 40px
</style>
