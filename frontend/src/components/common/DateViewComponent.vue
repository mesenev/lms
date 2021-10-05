<template>
  <div>
    <span>{{ date }}</span>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class DateViewComponent extends Vue {
  @Prop({ required: true }) dateAsInteger!: number;
  @Prop({ default: false }) showDayWeek!: boolean;
  src = "https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png";
  daysOfWeek: string[] = [
    'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье',
  ]

  get date(): string {
    const date = new Date(this.dateAsInteger);
    let month = String(date.getMonth() + 1);
    let day = String(date.getDate());
    const year = String(date.getFullYear());
    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;
    let answer = `${day}/${month}/${year}`;
    if (this.showDayWeek) answer = `${this.daysOfWeek[date.getDay()]}, ` + answer;
    return answer;
  }
}
</script>

<style lang="stylus" scoped></style>
