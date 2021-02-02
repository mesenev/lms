<template>
  <div>
    <div class="bx--row">
      <cv-tag :label="submit.status"
              :kind="kind(submit)">
      </cv-tag>
    </div>
  </div>
</template>

<script lang="ts">
import SubmitModel from "@/models/SubmitModel";
import { Component, Prop, Vue } from 'vue-property-decorator';
import {Dictionary} from "vue-router/types/router";


@Component({ components: {} })
export default class SubmitStatus extends Vue {
  @Prop({ required: true }) submit!: SubmitModel;

  colors: Dictionary<string> = {
    OK: 'green',
    WA: 'red',
    TL: 'blue',
    ML: 'purple',
    NP: 'cool-gray'
  }

  kind(submit: SubmitModel) {
    const mark = submit.status;
    return (mark) ? this.colors[mark]: 'high-contrast';
  }
}
</script>

<style scoped lang="stylus">

</style>
