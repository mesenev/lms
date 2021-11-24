<template>
  <div class="scrollable-solution-list">
    <cv-structured-list
      class="submit-list"
      condensed @change="changeCurrentSubmit">
      <template slot="headings"></template>
      <template slot="items">
        <cv-structured-list-item
          v-for="message in messages" :key="message.id" class="list--item" style="border: none;"
        >
          <img
            alt='1'
            class="avatar student"
            src="https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png"
            style="float: left">
          <div class="one-history-point"> {{ message.text }}</div>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
    <cv-text-input v-model.trim="commentary"
                   :disabled="false"
                   :label="''"
                   :light="false"
                   :password-visible="false"
                   :placeholder="'Введите сообщение'"
                   :type="''"
                   :value="''"
                   class="searchbar"
                   v-on:keydown.enter="messageForButton">
    </cv-text-input>
  </div>
</template>

<script lang="ts">
import LogEventModel from "@/models/LogEventModel";
import UserModel from '@/models/UserModel';
import userStore from '@/store/modules/user';
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import { Component, Prop } from "vue-property-decorator";


@Component({ components: {} })
export default class LogEventComponent extends NotificationMixinComponent {
  @Prop({ required: true }) studentId!: number;
  @Prop({ required: true }) problemId!: number;
  userStore = userStore;
  commentary = '';
  messages: Array<LogEventModel> = [
    {
      "type": "message", "text": "Решение отправлено на проверку", "sender": this.user,
      "id": 0, "name": "sdfdsfsf",
    },
    {
      "type": "message", "text": "Вердикт: ОК", "sender": this.user,
      "id": 1, "name": "sdfdsfsf",
    },
    {
      "type": "message", "text": "Статус изменен: Зачтено", "sender": this.user,
      "id": 2, "name": "sdfdsfsf",
    },
    {
      "type": "message", "text": "Выставлен балл: 33.0", "sender": this.user,
      "id": 3, "name": "sdfdsfsf",
    },
  ];

  get user(): UserModel {
    return this.userStore.user;
  }

  changeCurrentSubmit() {
    //
  }

  async mounted() {
    const submits = [...document.getElementsByClassName("submit-list")];
    submits.forEach(element => element.scrollTop = element.scrollHeight);
    const userMessages = [...document.getElementsByTagName("img")];
    userMessages.forEach(
      element => element.classList.contains("avatar") ? element.src = this.avatarUrl : 0,
    );

  }

  messageForButton() {
    const newMessage: LogEventModel = {
      "name": "logEvent", "type": "message", "text": this.commentary,
      sender: this.user, id: this.messages.length + 2,
    };
    this.messages.push(newMessage);
    this.commentary = '';
  }
}

</script>

<style scoped lang="stylus">

.scrollable-solution-list
  height 100%
  overflow scroll

.avatar
  width 2em
  margin-bottom 0.3em

.list--item
  cursor: pointer

  &:hover
    background-color: #e5e5e5;

.stuff
  margin-left 1em

.avatar
  margin 0

.student
  margin 0
  margin-right 1em

.searchbar
  position relative
  height 2em
  left 0
  width 100%
  margin-left auto
  margin-right auto
  text-align center

.one-history-point
  word-break break-after
  font-size 1em
  padding 5px
  margin 20px
  background white
  border 1px solid rgba(0, 0, 0, 0.3)
  border-radius 5px
  min-height 40px

.bx--tile.submit-list
  border-left 1em
  padding-left 1em
  margin-left 1em
  box-shadow -1em black

.bx--list
  list-style-type none

.submit-list
  margin 0
  padding 0
  height 24.55em
  overflow-y scroll
  bottom 0
  list-style-type none
  border-radius 10px
  border-color black
</style>
