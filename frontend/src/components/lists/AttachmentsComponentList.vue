<template>
  <div>
    {{attachment.name}}
    <component class="trash-icon" :is="TrashCan" @click.prevent.stop="deleteAttachment"/>
  </div>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import NotificationMixinComponent from '../common/NotificationMixinComponent.vue';
import AttachmentModel from "@/models/Attachment";
import TrashCan from '@carbon/icons-vue/es/trash-can/20';
import MaterialStore from '@/store/modules/material'
@Component({
  components: {}
})
export default class FileListComponent extends NotificationMixinComponent {
  @Prop( { required: true } ) attachment!: AttachmentModel;
  TrashCan = TrashCan;
  materialStore = MaterialStore

  deleteAttachment(){
    this.materialStore.deleteAttachment(this.attachment.id);
  }
}
</script>
<style lang="stylus">

</style>
