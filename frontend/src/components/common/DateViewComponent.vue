<template>
  <div>
    <span>{{ date }}</span>
  </div>
</template>

<script lang="ts" setup>

import { computed } from "vue";

const props = defineProps({
  dateAsInteger: { type: Number, required: true },
  showDayWeek: { type: Boolean, default: false }
})

const daysOfWeek: string[] = [
  'воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота',
]

const date = computed(() => {
  const date = new Date(props.dateAsInteger);
  let month = String(date.getMonth() + 1);
  let day = String(date.getDate());
  const year = String(date.getFullYear());
  if (month.length < 2) month = '0' + month;
  if (day.length < 2) day = '0' + day;
  let answer = `${day}/${month}/${year}`;
  if (props.showDayWeek) answer = `${answer}, ${daysOfWeek[date.getDay()]}`;
  return answer;
})
</script>

<style lang="stylus" scoped></style>
