<template>
  <div class="attachment-content">
    <div class="attachment-title">
      {{ attachment.name }}
    </div>
    <div class="attachment-btns">
      <component class="trash-icon icon" :is="TrashCan" @click.prevent.stop="deleteAttachment"/>
      <component class="copy-icon icon" :is="Copy" title="Скопировать" @click="insertAttachment"/>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { PropType } from "vue";
import type { AttachmentModel } from "@/models/Attachment";
import TrashCan from '@carbon/icons-vue/es/trash-can/20';
import Copy from '@carbon/icons-vue/es/copy/20'


const props = defineProps({
  attachment: { type: Object as PropType<AttachmentModel>, required: true }
})

const emits = defineEmits(['show-confirm-modal'])

function insertAttachment() {
  let markdown_file_string = '';

  if (props.attachment.file_format.includes('image/')) {
    markdown_file_string = '<img src="' + props.attachment.file_url + '" alt="' +
      props.attachment.name;
    markdown_file_string += '" width="" height="">';
  } else if (props.attachment.file_format.includes('video/')) {
    markdown_file_string = '<video width="100%" controls="controls">' +
      '<source src="' + props.attachment.file_url + ' "></video>';
  } else {
    markdown_file_string = '<a href="' + props.attachment.file_url + '">' + props.attachment.name
      + '</a>'
  }
  window.navigator.clipboard.writeText(markdown_file_string);
}

function deleteAttachment() {
  emits('show-confirm-modal', props.attachment);
}
</script>
<style lang="stylus">
.attachment-content
  display flex
  flex-direction row
  justify-content space-between
  margin 0.5rem

.attachment-title
  display flex
  align-items center

.trash-icon
  margin-right 0.5rem

.icon
  transition ease-in-out 0.1s

.icon:active
  transform scale(0.9)

</style>
