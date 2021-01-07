<script lang="ts">
import LessonContent from '@/models/LessonContent';
import router from '@/router';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Material extends Vue {
  @Prop() materialProp!: LessonContent;

  openMaterial(): void {
    router.push({ name: 'MaterialView', params: { materialId: this.material.id.toString() } });
  }

  get material(): LessonContent {
    return this.materialProp;
  }
}
</script>

<template>
  <div v-on:click="openMaterial">
      <h5>{{material.name }}</h5>
  </div>
</template>

<style scoped lang="stylus">

</style>
