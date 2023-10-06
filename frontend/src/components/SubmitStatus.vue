<template>
  <div class="submit-status--wrapper">
    <cv-tag class="tag" :label="submit.status"
            :style="`background-color: ${statusColor(submit.status)};`">
    </cv-tag>
  </div>
</template>

<script lang="ts" setup>
import type { SubmitModel } from "@/models/SubmitModel";
import { statusAssociations } from "@/common/colors";
import type { PropType } from "vue";

const props = defineProps({
  submit: { type: Object as PropType<SubmitModel>, required: true },
  statusOnly: { type: Boolean, required: false, default: false }
})

  function statusColor(status: string): string {
    return statusAssociations[status] || statusAssociations['default'];
  }
</script>

<style scoped lang="stylus">
  .tag
    background-color transparent
</style>
