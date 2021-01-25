<template>
  <div>
    <span>{{ catsProblem.id }}</span> <br>
    <span>{{ catsProblem.name }}</span> <br>
    <span>{{ catsProblem.text_url }}</span>
  </div>
</template>

<script lang="ts">
import CatsProblemModel from '@/models/CatsProblemModel';
import { Component, Prop, Vue } from 'vue-property-decorator';


@Component({ components: {} })

export default class CatsProblemComponent extends Vue {
  @Prop({ required: true }) catsProblem!: CatsProblemModel;

}
</script>

<style lang="stylus" scoped>
</style>
