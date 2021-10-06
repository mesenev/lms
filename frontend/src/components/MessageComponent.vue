<template>
  <div v-if="this.userStore.user.id === this.message.sender.id" class="author-message">
    <img v-if="displayAvatar" src="" alt="'avatar'" onerror="this.src = 'https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png'" class="avatar student">
    <a href="#" class="button">{{ this.message.text }}</a>
              <br>
  </div>

  <div v-else class="non-author-message">
    <a href="#" class="button answer">всё фигня, переделывай</a>
    <img v-if="displayAvatar" src="" alt="'avatar'" onerror="this.src = 'https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png'" class="avatar staff">
    <br>
  </div>
</template>

<script lang="ts">
import MessageModel from "@/models/MessageModel";
import userStore from '@/store/modules/user';
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import { Component, Prop } from "vue-property-decorator";


@Component({ components: {} })
export default class MessageComponent extends NotificationMixinComponent {
  @Prop({ required: true }) message?: MessageModel | null;
  userStore = userStore;
  displayAvatar?: boolean;

  get isStaff() {
    return this.message?.sender?.staff_for.includes(this.message?.courseId);
  }

  get senderAvatar() {
    return this.message?.sender?.avatar_url;
  }

  async created() {
    console.log(this.displayAvatar);
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
