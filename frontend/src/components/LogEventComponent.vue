<template>
  <div class="scrollable-solution-list">
    <div class="title-space"></div>
    <div class="title">
      <span>История решений:</span>
    </div>
    <div id="submit-list-wrapper"
         class="wrapper-for_controll-overflow-list"
         @scroll="handleScroll">
      <cv-loading v-if="loading"/>
      <cv-structured-list
        v-else
        class="submit-list">
        <template slot="items">
          <div
            v-for="event in sortedEvents" :key="event.id" class="list--item"
            v-bind:class="{
              'list--item--submit': event.type === logEventTypes.TYPE_SUBMIT,
              'right': event.author === userStore.user.id,
              'clickable': [logEventTypes.TYPE_SUBMIT,
                            logEventTypes.TYPE_STATUS_CHANGE].includes(event.type)}"
            v-on:click="elementClickHandler(event)">

            <img
              v-if="event.data.thumbnail"
              :src="event.data.thumbnail"
              alt='avatar'
              class="student--avatar">
            <span class="event--date">{{ event.created_at | withoutSeconds }}</span>

            <div v-if="logEventTypes.TYPE_SUBMIT === event.type" class="one-history-point">
              <span>ID решения: {{ event.data.message }}</span>
              <div
                class="checkbox--submit"
                v-bind:class="{ 'hidden': event.submit !== selectedSubmit }">
                <component :is="Checkbox"/>
              </div>
            </div>
            <div v-else class="one-history-point">
              <span>{{ event.data.message }}</span>
              <component
                :is="iconTrash"
                v-if="event.author === userStore.user.id && event.type === logEventTypes.TYPE_MESSAGE"
                class="event--delete"
                title="Удалить сообщение"
                @click="deleteEvent(event)"/>
            </div>
            <div ref="eventListBottom" class="space"></div>
          </div>
        </template>
      </cv-structured-list>
    </div>
    <div class="searchbar-out">
      <cv-text-input
        v-model.trim="commentary"
        :disabled="false"
        :label="''"
        :light="false"
        :password-visible="false"
        :placeholder="'Введите сообщение'"
        :type="''"
        :value="''"
        class="searchbar"
        v-on:keydown.enter="createMessageHandler">
      </cv-text-input>
    </div>
    <div class="btn-out">
      <cv-button class="btn-send" kind="tertiary" @click="createMessageHandler">Отправить
      </cv-button>
    </div>
  </div>
</template>

<script lang="ts">
import LogEventModel, * as logEventTypes from "@/models/LogEventModel";
import userStore from '@/store/modules/user';
import TrashCan16 from '@carbon/icons-vue/es/trash-can/16';
import Checkbox16 from '@carbon/icons-vue/es/checkbox--checked--filled/16';
import logEventStore from '@/store/modules/logEvent';
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import { Component, Prop } from "vue-property-decorator";


@Component({
  components: { TrashCan16 },
  filters: {
    withoutSeconds: function (d: string) {
      return new Date(d).toLocaleString([], {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
      });
    }
  }
})
export default class LogEventComponent extends NotificationMixinComponent {
  @Prop({ required: true }) problemId!: number;
  @Prop({ required: true }) studentId!: number;
  @Prop({ required: false }) selectedSubmit?: number;
  userStore = userStore;
  logEventStore = logEventStore;
  logEventTypes = logEventTypes;
  loading = true;
  messageIsSending = false;
  commentary = '';
  iconTrash = TrashCan16;
  Checkbox = Checkbox16;
  events: Array<LogEventModel> = [];
  newEvents: Array<LogEventModel> = [];
  connection!: WebSocket;
  limit = 20;
  offset = 0;
  previousScrollHeightMinusScrollTop = 0;

  get sortedEvents() {
    return this.events.sort((a, b) => a.id - b.id);
  }

  // @Watch('studentId')
  // @Watch('problemId')
  // onPropChanged() {
  //   this.fetchEvents();
  // }

  async created() {
    await this.userStore.fetchUserById(this.studentId);
    await this.fetchEvents();
    this.socketConnectionUpdate();
    await this.scrollDown();
    this.loading = false;
  }

  socketMessageHandler(event: MessageEvent) {
    this.events.push((JSON.parse(event.data) as LogEventModel));
    this.events = [...this.events];
    this.$nextTick(this.scrollDown);
  }

  socketEventHandler(event: Event) {
    console.log(event);
  }

  socketErrorHandler(event: Event) {
    console.log('something bad happened with sockets');
    console.log(event);
  }

  socketConnectionUpdate() {
    const protocol = (window.location.protocol === 'http:') ? 'ws://' : 'wss://';
    this.connection = new WebSocket(
      protocol + window.location.host
      + `/ws/notifications?user_id=${this.studentId}&problem_id=${this.problemId}`
    );
    this.connection.onmessage = this.socketMessageHandler;
    this.connection.onclose = this.socketEventHandler;
    this.connection.onopen = this.socketEventHandler;
    this.connection.onerror = this.socketErrorHandler;
  }

  async fetchEvents() {
    this.newEvents = await this.logEventStore.fetchLogEventsByProblemAndStudentIds(
      {
        problem: this.problemId,
        student: this.studentId,
        limit: this.limit,
        offset: this.offset
      },
    );
    if (this.newEvents.length) {
      this.recordScrollPosition();
      this.events.unshift(...this.newEvents);
      this.loading = false;
      this.offset += this.limit;
      this.restoreScrollPosition();
    }
    await this.thumbnailsUpdate();
  }

  async thumbnailsUpdate() {
    if (!this.events.length)
      return;
    let previous = this.sortedEvents[0];
    await this.fetchThumbnailForEvent(previous);
    for (const event of this.sortedEvents) {
      if (previous.author !== event.author)
        await this.fetchThumbnailForEvent(event);
      previous = event;
    }
    this.events = [...this.events];
  }

  async fetchThumbnailForEvent(event: LogEventModel) {
    if (!event.author)
      return;
    const user = await this.userStore.fetchUserById(event.author);
    event.data.thumbnail = user.thumbnail;
  }

  elementClickHandler(element: LogEventModel): void {
    if (logEventTypes.TYPE_SUBMIT === element.type)
      this.$emit('submit-selected', { id: element.submit });
    if (logEventTypes.TYPE_STATUS_CHANGE === element.type)
      this.$emit('cats-answer', { id: element.submit });
  }

  async deleteEvent(event: LogEventModel) {
    await this.logEventStore.deleteEvent(event.id);
    this.events = this.events.filter(value => value.id !== event.id);
    await this.thumbnailsUpdate();
    if (this.offset > 0) {
      this.offset -= 1;
    }
  }

  async createMessageHandler() {
    if (!this.commentary)
      return;
    this.messageIsSending = true;
    const newMessage: LogEventModel = {
      ...this.logEventStore.getNewLogEventMessage,
      problem: this.problemId, student: this.studentId,
      data: { message: this.commentary },
    };
    await this.logEventStore.createLogEvent(newMessage);
    // if (answer !== undefined) {
    //   await this.fetchThumbnailForEvent(answer);
    // this.events.push(answer);
    // }
    this.commentary = '';
    this.messageIsSending = false;
    this.offset += 1;
  }

  picUrl(url: string): string {
    if (url)
      return url;
    return "https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png";
  }

  recordScrollPosition() {
    const eventList = document.getElementById('submit-list-wrapper')!;
    this.previousScrollHeightMinusScrollTop =
      eventList.scrollHeight - eventList.scrollTop;
  }

  restoreScrollPosition() {
    const eventList = document.getElementById('submit-list-wrapper')!;
    eventList.scrollTop = eventList.scrollHeight - this.previousScrollHeightMinusScrollTop;
  }

  handleScroll() {
    const eventList = document.getElementById('submit-list-wrapper')!;
    if (eventList.scrollTop === 0) {
      this.fetchEvents();
    }
  }

  async scrollDown() {
    const eventList = document.getElementById('submit-list-wrapper')!;
    eventList.scrollTop = eventList.scrollHeight;
  }
}

</script>

<style lang="stylus" scoped>
.title
  font-size 1em
  padding 1em
  background-color #393939
  color white
  border-top-right-radius 5px

  &-space
    height calc(2em + 0.5rem)
    background-color #f4f4f4

.avatar
  width 2em
  margin-bottom 0.3em

.list--item--submit
  span
    font-weight bold

  .one-history-point
    padding-right 30px

.hidden
  display none

.list--item
  border none
  cursor default
  margin-top 0.1em
  padding-top 1em
  padding-bottom 0.1em
  position relative

  &.right
    text-align right

    .student--avatar
      right 0

    .event--date
      right 40px
      left 0

    .one-history-point
      margin-right 35px
      margin-left 5px

  &.clickable
    cursor pointer

  .student--avatar
    margin 0
    float left
    height 32px
    width 32px
    border-radius: 150%
    position absolute
    top 1em

  .event--delete
    display none
    right -5px
    bottom -10px
    background white
    height 20px
    width 20px
    position absolute
    cursor pointer

  &:hover
    .event--date
      display unset

    .event--delete
      display unset

.stuff
  margin-left 1em

.checkbox--submit
  position absolute
  height 16px
  width 16px
  right 3px
  top 50%
  transform translate(-50%, -50%)
  vertical-align center

.one-history-point
  word-break break-word
  font-size 1em
  padding 10px 15px
  margin 0 35px
  background white
  border 0.5px solid rgba(0, 0, 0, 0.3)
  border-radius 5px
  overflow-wrap anywhere
  position relative
  width fit-content
  display inline-block
  margin-right 5px


.bx--tile.submit-list
  border-left 1em
  padding-left 1em
  margin-left 1em

//box-shadow -1em black

.bx--list
  list-style-type none

.submit-list
  margin 0
  padding 0
  bottom 0
  list-style-type none
  border-radius 10px
  border-color black


.wrapper-for_controll-overflow-list
  height calc(400px)
  overflow scroll
  overflow-x hidden
  padding 0 0.5rem
  border 0.5px #8D8D8D solid

span.event--date
  font-weight normal
  color #808080
  position absolute
  left 40px
  font-size 0.7em
  top 0
  display none

.btn
  &-out
    display flex
    flex-direction row
    padding 0.5rem 0 0.5rem 0.5rem
    justify-content flex-end
    background-color #f4f4f4

  &-send
    padding 0 1rem

.space
  height 10px

.searchbar-out
  padding 0.5rem
  border solid #8d8d8d
  border-width 0 0.5px 0.5px 0.5px
  border-bottom-left-radius 5px
</style>

<style lang="stylus">
.wrapper-for_controll-overflow-list
  .bx--structured-list-thead
    display none

.searchbar
  input
    border-bottom 0
    border-radius 5px

  label
    display none
</style>
