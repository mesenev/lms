<template>
  <div>
    <div class="bx--row user">
      <img class="avatar"
           v-bind:src="pic_url"
           alt=""
           width="30"
           height="30">
      <span class="name">{{ name }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import UserModel from "@/models/UserModel";
import { Component, Prop, Vue } from 'vue-property-decorator';


@Component({ components: {} })
export default class UserComponent extends Vue {
  @Prop({ required: true }) user!: UserModel;
  src = "https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png";

  get name() {
    if (this.user && this.user.first_name && this.user.last_name)
      return `${this.user.first_name} ${this.user.last_name}`;
    return this.user.username;
  }

  get pic_url() {
    if (!this.user.avatar_url)
      return this.src;
    return this.user.thumbnail;
  }
}
</script>

<style scoped lang="stylus">
.name
  padding-left 10px

.user
  display flex
  flex-direction row
  align-items center

.avatar
  object-fit:cover;
  border-radius: 150%;
  padding: 0;
  margin: 0;
  margin-left 1.5rem

</style>
