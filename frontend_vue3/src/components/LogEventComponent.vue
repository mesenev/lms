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
        <template v-slot:items>
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
            <span class="event--date">{{ withoutSeconds(event.created_at) }}</span>

            <div v-if="logEventTypes.TYPE_SUBMIT === event.type" class="one-history-point">
              <span>ID решения: {{ event.data.message }}</span>
              <div
                  class="checkbox--submit"
                  v-bind:class="{ 'hidden': event.submit !== selectedSubmit }">
                <component :is="Checkbox16"/>
              </div>
            </div>
            <div v-else class="one-history-point">
              <span>{{ event.data.message }}</span>
              <component
                  :is="TrashCan16"
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
      <cv-button class="btn-send" @click="createMessageHandler">Отправить</cv-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type LogEventModel from "@/models/LogEventModel";
import * as allLogEventTypes from "@/models/LogEventModel";
import useUserStore from '@/stores/modules/user';
import TrashCan16 from '@carbon/icons-vue/es/trash-can/16';
import Checkbox16 from '@carbon/icons-vue/es/checkbox--checked--filled/16';
import useLogEventStore from '@/stores/modules/logEvent';
import { ref, computed, onMounted, nextTick } from "vue";

const props = defineProps({
  problemId: { type: Number, required: true },
  studentId: { type: Number, required: true },
  selectedSubmit: { type: Number, required: false, default: NaN }
})

const emit = defineEmits<{
  (e: 'submit-selected', id: number): void,
  (e: 'cats-answer', id: number): void
}>();

const userStore = useUserStore();
const logEventStore = useLogEventStore();
const logEventTypes = allLogEventTypes;
const loading = ref<boolean>(true);
const messageIsSending = ref<boolean>(false);
const commentary = ref<string>('');
const events = ref<Array<LogEventModel>>([]);
const newEvents = ref<Array<LogEventModel>>([]);
let connection!: WebSocket;
const limit = 20;
const offset = ref(0);
const previousScrollHeightMinusScrollTop = ref(0);

const sortedEvents = computed(() => {
  return [...events.value].sort((a, b) => a.id - b.id);
})

// @Watch('studentId')
// @Watch('problemId')
// onPropChanged() {
//   this.fetchEvents();
// }

onMounted(async () => {
  await userStore.fetchUserById(props.studentId);
  await fetchEvents();
  socketConnectionUpdate();
  await scrollDown();
  loading.value = false;
})

function withoutSeconds(d: string | undefined) {
  if (typeof d === 'undefined') return '';
  return new Date(d).toLocaleString([], {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit"
  });
}

function socketMessageHandler(event: MessageEvent) {
  events.value.push((JSON.parse(event.data) as LogEventModel));
  events.value = [...events.value];
  nextTick(scrollDown);
}

function socketEventHandler(event: Event) {
  console.log(event);
}

function socketErrorHandler(event: Event) {
  console.log('something bad happened with sockets');
  console.log(event);
}

function socketConnectionUpdate() {
  const protocol = (window.location.protocol === 'http:') ? 'ws://' : 'wss://';
  connection = new WebSocket(
      protocol + window.location.host
      + `/ws/notifications?user_id=${props.studentId}&problem_id=${props.problemId}`
  );
  connection.onmessage = socketMessageHandler;
  connection.onclose = socketEventHandler;
  connection.onopen = socketEventHandler;
  connection.onerror = socketErrorHandler;
}

async function fetchEvents() {
  newEvents.value = await logEventStore.fetchLogEventsByProblemAndStudentIds(
      {
        problem: props.problemId,
        student: props.studentId,
        limit: limit,
        offset: offset.value
      },
  );
  if (newEvents.value.length) {
    recordScrollPosition();
    events.value.unshift(...newEvents.value);
    loading.value = false;
    offset.value += limit;
    restoreScrollPosition();
  }
  await thumbnailsUpdate();
}

async function thumbnailsUpdate() {
  if (!events.value.length)
    return;
  let previous = sortedEvents.value[0];
  await fetchThumbnailForEvent(previous);
  for (const event of sortedEvents.value) {
    await fetchThumbnailForEvent(event);
    previous = event;
  }
  events.value = [...events.value];
}

async function fetchThumbnailForEvent(event: LogEventModel) {
  if (!event.author)
    return;
  const user = await userStore.fetchUserById(event.author);
  event.data.thumbnail = picUrl(user.thumbnail);
}

function elementClickHandler(element: LogEventModel): void {
  if (typeof element.submit === 'undefined') return;
  if (logEventTypes.TYPE_SUBMIT === element.type)
    emit('submit-selected', element.submit);
  if (logEventTypes.TYPE_STATUS_CHANGE === element.type)
    emit('cats-answer', element.submit);
}

async function deleteEvent(event: LogEventModel) {
  await logEventStore.deleteEvent(event.id);
  events.value = events.value.filter(value => value.id !== event.id);
  await thumbnailsUpdate();
  if (offset.value > 0) {
    offset.value -= 1;
  }
}

async function createMessageHandler() {
  if (!commentary.value)
    return;
  messageIsSending.value = true;
  const newMessage: LogEventModel = {
    ...logEventStore.getNewLogEventMessage,
    problem: props.problemId, student: props.studentId,
    data: { message: commentary.value, thumbnail: picUrl(userStore.user.thumbnail) },
  };
  await logEventStore.createLogEvent(newMessage);
  // if (answer !== undefined) {
  //   await this.fetchThumbnailForEvent(answer);
  // this.events.push(answer);
  // }
  commentary.value = '';
  messageIsSending.value = false;
  offset.value += 1;
}

function picUrl(url: string): string {
  if (url)
    return url;
  return "https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png";
}

function recordScrollPosition() {
  const eventList = document.getElementById('submit-list-wrapper')!;
  previousScrollHeightMinusScrollTop.value =
      eventList.scrollHeight - eventList.scrollTop;
}

function restoreScrollPosition() {
  const eventList = document.getElementById('submit-list-wrapper')!;
  eventList.scrollTop = eventList.scrollHeight - previousScrollHeightMinusScrollTop.value;
}

function handleScroll() {
  const eventList = document.getElementById('submit-list-wrapper')!;
  if (eventList.scrollTop === 0) {
    fetchEvents();
  }
}

async function scrollDown() {
  const eventList = document.getElementById('submit-list-wrapper')!;
  eventList.scrollTop = eventList.scrollHeight;
}

</script>

<style lang="stylus" scoped>
.title
  font-size 1em
  padding 1em
  background-color #393939
  color white
  border-top-right-radius 5px

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
    fill var(--cds-danger-01)
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
  background var(--cds-ui-01)
  color var(--cds-text-01)
  border 0.5px solid var(--cds-ui-05)
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


.scrollable-solution-list
  height 82%

.wrapper-for_controll-overflow-list
  height calc(491px)
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
  &-send
    padding 0 1rem
    max-width calc(100px)

.space
  height 10px

.searchbar-out
  display flex
  gap 10px
  padding 0.5rem
  border solid #8d8d8d
  border-width 0 0.5px 0.5px 0.5px
  border-bottom-right-radius 5px
</style>

<style lang="stylus">
.wrapper-for_controll-overflow-list
  .bx--structured-list-thead
    display none

.searchbar
  flex-direction row
  align-items center

  input
    border-bottom 0
    border-radius 5px

  label
    display none
</style>
