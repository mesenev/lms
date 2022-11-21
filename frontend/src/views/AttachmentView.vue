<template>
  <div>
    {{this.attachment.id}}
    <p>
    {{this.attachment.name}}
    <p>
    {{this.attachment.material}}
    <p>
    {{this.attachment.file_url}}
  </div>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import AttachmentModel from "@/models/Attachment";
import Vue from 'vue';
@Component({
  components: {}
})
export default class AttachmentView extends Vue {
  @Prop( { required: true } ) attachment!: AttachmentModel;
}
</script>
<style lang="stylus">

</style>
