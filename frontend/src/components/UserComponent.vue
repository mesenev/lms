<script lang="ts">
import UserModel from "@/models/UserModel";
import userStore from '@/store/modules/user';
import courseStore from '@/store/modules/course';
import { Component, Prop, Vue } from 'vue-property-decorator';


@Component({ components: {} })
export default class UserComponent extends Vue {
  @Prop({ required: false }) user!: UserModel;
  @Prop({ required: false }) userId!: number;
  loading = true;
  userStore = userStore;
  courseStore = courseStore;
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

  get warning() {
    if (!this.courseStore.currentCourse)
      return false;
    return !(this.userId in this.userStore.currentCourseStudents);
  }

  async created() {
    if (!this.user && !this.userId)
      throw Error();
    if (this.user)
      this._user = this.user;
    if (this.userId)
      this._user = this.userStore.currentCourseStudents[this.userId];
    if (typeof this._user === 'undefined')
      this._user = await this.userStore.fetchUserById(this.userId)
    this.loading = false;
  }
}
</script>

<template>
  <div class="user-component">
    <div class="user-component--wrapper">
      <img alt="" class="user-component--avatar" v-bind:src="pic_url"/>
      <div class="user-component--name">
        <cv-inline-loading v-if="loading" active/>
        <span v-else>{{ name }}</span>
      </div>
      <div v-if="warning" class="user-component--warning">
        <cv-tooltip tip="Пользователь не является студентом курса"/>
      </div>
    </div>
  </div>
</template>

<style scoped lang="stylus">
.user-component
  width 200px
  height 32px

  &--wrapper
    display flex
    flex-flow row
    align-items center

  &--avatar
    height 32px
    width 32px
    border-radius: 150%
    padding 0
    margin 0

  &--name
    padding-left var(--cds-spacing-02)

  &--warning
    padding-left var(--cds-spacing-02)
    display flex
    align-items center

</style>
