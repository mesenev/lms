<template>
  <div>
    <img class = "avatar"
         v-bind:src="pic_url"
         alt=""
         width="250"
         height="250" >
  </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';

@Component({ components: { } })

export default class Avatar extends Vue {
  @Prop({ required: true }) avatar_url!: string
  src = "https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png";

  get pic_url() {
    if (!this.avatar_url)
      return this.src;
    return this.avatar_url;
  }
}
</script>

<style scoped lang="stylus">
  .avatar
    object-fit:cover;
    border-radius: 150%;
</style>
