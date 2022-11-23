<template>
  <div>
    {{attachment.name}}
    <component class="trash-icon" :is="TrashCan" @click.prevent.stop="deleteAttachment"/>
    <Insert @click="insertAttachment" />
  </div>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import NotificationMixinComponent from '../common/NotificationMixinComponent.vue';
import AttachmentModel from "@/models/Attachment";
import TrashCan from '@carbon/icons-vue/es/trash-can/20';
import Insert from '@carbon/icons-vue/es/insert/20'
import MaterialStore from '@/store/modules/material'
import marked from 'marked';
@Component({
  components: {Insert}
})
export default class FileListComponent extends NotificationMixinComponent {
  @Prop( { required: true } ) attachment!: AttachmentModel;
  TrashCan = TrashCan;
  materialStore = MaterialStore

  deleteAttachment(){
    this.materialStore.deleteAttachment(this.attachment.id);
  }
  insertAttachment(){
    let markdown_file_string = '';

    if (this.attachment.file_format.includes('image/')){
      markdown_file_string = '<img src="' +  this.attachment.file_url + '" alt="' +
      this.attachment.name;
      markdown_file_string += '" width="500" height="600">';
    }
    else if(this.attachment.file_format.includes('video/')){
      markdown_file_string = '<video><source src="' + this.attachment.file_url
      + ' " controls></video>'
    }
    else {
      markdown_file_string = '<a href="' + this.atta
    }

    window.navigator.clipboard.writeText(markdown_file_string)
  }
}
</script>
<style lang="stylus">

</style>
