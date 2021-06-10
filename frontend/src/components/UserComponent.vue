<template>
  <div>
    <div class="bx--row user">
      <img class="avatar"
           v-bind:src="pic_url"
           alt=""
           width="30"
           height="30">
      <cv-tooltip v-if="warning" tip="Пользователь не является студентом курса"/>
      <div class="name">
        <cv-loading v-if="loading" :small="true"/>
        <span v-else>{{ name }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import UserModel from "@/models/UserModel";
import userStore from '@/store/modules/user';
import { Component, Prop, Vue } from 'vue-property-decorator';


@Component({ components: {} })
export default class UserComponent extends Vue {
  @Prop({ required: false }) user!: UserModel;
  @Prop({ required: false }) userId!: number;
  loading = true;
  warning = false;
  userStore = userStore;
  _user!: UserModel;

  get name() {
    if (this._user && this._user.first_name && this._user.last_name)
      return `${this._user.first_name} ${this._user.last_name}`;
    return '';
  }

  get pic_url() {
    if (this._user && this._user.avatar_url)
      return this._user.thumbnail;
    return "https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png";
  }

  async created() {
    if (!this.user && !this.userId)
      throw {};
    if (this.user)
      this._user = this.user;
    if (this.userId)
      this._user = this.userStore.currentCourseStudents[this.userId];
    if (typeof this._user === 'undefined') {
      this.warning = true;
      this._user = await this.userStore.fetchUserById(this.userId)
    }
    this.loading = false;
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
  object-fit: cover;
  border-radius: 150%;
  padding: 0;
  margin: 0;
  margin-left 1.5rem

</style>
