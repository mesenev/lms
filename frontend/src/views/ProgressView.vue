<template>
  <div>
    <Progress></Progress>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Progress from '@/components/Progress.vue';

@Component({
  components: {
    Progress,
  },
})
export default class ProgressView extends Vue {}
</script>

<style lang="stylus"></style>
