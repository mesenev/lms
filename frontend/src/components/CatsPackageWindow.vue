<template>
  <cv-loading v-if="isLoading"/>
  <div
    v-else
    class="cats-package-window">
    <div v-for="message_keys in Object.keys(getCatsData)" v-bind:key="message_keys">
      <div class="head_of_message">
        {{ message_keys }}
      </div>
      <div class="message">
        {{ getCatsData[message_keys] }}
      </div>
    </div>

  </div>
</template>

<script lang="ts">

import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class CatsPackageWindow extends Vue {
  @Prop({ required: false, default: null }) catsSubmitAnswerProp!: object | null;

  get isLoading(): boolean {
    return this.catsSubmitAnswerProp === null;
  }

  get getCatsData() {
    return this.catsSubmitAnswerProp;
  }
}
</script>


<style lang="stylus" scoped>
.head_of_message
  padding 10px
  width 100%
  height min-content
  font-size 1.7em
  font-weight bold

.message
  background rgba(207, 204, 174, 0.3);
  padding-left 5px
  padding-right 5px
  padding-bottom 10px
  padding-top 10px
  margin 10px


.cats-package-window
  height 100%
  background white


</style>

<style lang="stylus" scoped>

</style>
