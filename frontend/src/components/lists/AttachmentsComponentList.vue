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

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator';
import NotificationMixinComponent from '../common/NotificationMixinComponent.vue';
import AttachmentModel from "@/models/Attachment";
import TrashCan from '@carbon/icons-vue/es/trash-can/20';
import Copy from '@carbon/icons-vue/es/copy/20'

@Component({
  components: { Copy, }
})
export default class FileListComponent extends NotificationMixinComponent {
  @Prop({ required: true }) attachment!: AttachmentModel;
  TrashCan = TrashCan;
  Copy = Copy;

  insertAttachment() {
    let markdown_file_string = '';

    if (this.attachment.file_format.includes('image/')) {
      markdown_file_string = '<img src="' + this.attachment.file_url + '" alt="' +
        this.attachment.name;
      markdown_file_string += '" width="" height="">';
    } else if (this.attachment.file_format.includes('video/')) {
      markdown_file_string = '<video controls="controls"><source src="' + this.attachment.file_url
        + ' "></video>'
    } else {
      markdown_file_string = '<a href="' + this.attachment.file_url + '">' + this.attachment.name
        + '</a>'
    }
    window.navigator.clipboard.writeText(markdown_file_string);
  }

  deleteAttachment() {
    this.$emit('show-confirm-modal', this.attachment);
  }
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
