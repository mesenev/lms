<template>
  <div class="submit-status--wrapper">

    <cv-tag class="tag" :label="submit.status"
            :style="`background-color: ${statusColor(submit.status)};`">
    </cv-tag>
  </div>
</template>

<script lang="ts">
import SubmitModel from "@/models/SubmitModel";
import { Component, Prop, Vue } from 'vue-property-decorator';
import { statusAssociations } from "@/common/colors";

@Component({ components: {} })
export default class SubmitStatus extends Vue {
  @Prop({ required: true }) submit!: SubmitModel;
  @Prop({ required: false, default: false }) statusOnly!: boolean;

  statusColor(status: string): string {
    return statusAssociations[status] || statusAssociations['default'];
  }
}
</script>

<style scoped lang="stylus">
  .tag
    background-color transparent
</style>
