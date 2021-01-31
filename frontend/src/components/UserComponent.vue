<template>
  <div>
    <div class="bx--row">
      <img class="avatar"
           v-bind:src="src"
           alt=""
           width="30"
           height="30">
      <h4 class="name">{{ user.first_name + ' ' + user.last_name }}</h4>
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
}
</script>

<style scoped lang="stylus">
.name {
  padding-left: 10px;
}

</style>
