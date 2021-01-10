<template>
  <div>
    <cv-button class="change-btn"
               @click="addLessonMaterials">
      Добавить материалы
    </cv-button>
  </div>
</template>

<script lang="ts">
import LessonModel from "@/models/LessonModel";
import { Component, Prop, Vue } from 'vue-property-decorator';


@Component({})
export default class EditLessonMaterials extends Vue {
  @Prop({ required: true }) lesson!: LessonModel;

  addLessonMaterials() {
    //
  }
}
</script>

<style lang="stylus">
.change-btn
  color var($--cds-ui-0)
</style>
