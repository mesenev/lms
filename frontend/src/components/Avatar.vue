<template>
  <div>
    <img class = "avatar"
         v-bind:src="src"
         alt=""
         width="250"
         height="250" >
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator';

@Component({ components: { } })

export default class Avatar extends Vue {
  src = "https://image.flaticon.com/icons/png/512/147/147144.png";
}
</script>

<style scoped lang="stylus">
  .avatar
    border-radius: 150%;
    padding: 0;
    margin: 0;
</style>
