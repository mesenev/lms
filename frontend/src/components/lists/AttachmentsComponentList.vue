<template>
  <div v-html="this.file"></div>
</template>

<script lang="ts">
import marked from 'marked';
import {Component, Prop} from 'vue-property-decorator';
import NotificationMixinComponent from '../common/NotificationMixinComponent.vue';
import MaterialFileModel from "@/models/Attachment";
@Component({
  components: {

  }
})
export default class FileListComponent extends NotificationMixinComponent {
  @Prop( { required: true } ) file!: MaterialFileModel;

}
</script>
<style lang="stylus">

</style>
