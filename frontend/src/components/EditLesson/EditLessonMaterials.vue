<template>
  <div>
    <cv-button class="change-btn"
               @click="addLessonMaterials">
      Добавить материалы
    </cv-button>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import LessonModel from "@/models/LessonModel";


@Component({})
export default class EditLessonMaterials extends Vue {
  @Prop({ required: true }) lesson!: LessonModel;

}
</script>

<style lang="stylus">
  .change-btn
    color var($--cds-ui-0)
</style>
