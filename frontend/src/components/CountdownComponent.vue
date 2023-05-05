<template>
  <div class="container">
    <ul class="countdown">
      <li v-for="data in timeData" :key="data.label">
        <span>{{ data.current.toString().padStart(2, "0") }}</span>
        <span v-if="data.label !== 'Seconds'">:</span>

      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";

@Component({})
export default class CountdownComponent extends Vue {
  @Prop({ required: true }) end!: string;

  @Watch('now')
  updateTime() {
    this.diff = this.date - this.now
    if (this.diff <= 0)
      this.diff = 0
    else {
      this.updateTimeDataElement(0, this.hours)
      this.updateTimeDataElement(1, this.minutes)
      this.updateTimeDataElement(2, this.seconds)
    }
  }

  now = 0
  diff = 0
  date = 0
  interval = 0
  timeData = [
    {
      current: 0,
      previous: 0,
      label: 'Hours',
      elementId: 'hours'
    },
    {
      current: 0,
      previous: 0,
      label: 'Minutes',
      elementId: 'minutes'
    },
    {
      current: 0,
      previous: 0,
      label: 'Seconds',
      elementId: 'seconds',
    }]

  async created() {
    this.now = Math.trunc((new Date().getTime()) / 1000)
    this.date = Math.trunc(Date.parse(this.end.replace(/-/g, "/")) / 1000)
    setInterval(() => {
      this.now = Math.trunc(new Date().getTime() / 1000);
    }, 1000);
  }


  get seconds() {
    return Math.trunc(this.diff) % 60
  }

  get minutes() {
    return Math.trunc(this.diff / 60) % 60
  }

  get hours() {
    return Math.trunc(this.diff / 3600)
  }

  updateTimeDataElement(id: number, newVal: number) {
    const val = newVal < 0 ? 0:newVal
    if (val !== this.timeData[id].current) {
      this.timeData[id].previous = this.timeData[id].current
      this.timeData[id].current = val
    }
  }
}
</script>


<style scoped lang="stylus">
.countdown
  display flex
  flex-direction row
  font-size 2rem

</style>
