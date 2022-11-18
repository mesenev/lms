<script lang="ts">
import UserModel from "@/models/UserModel";
import userStore from '@/store/modules/user';
import courseStore from '@/store/modules/course';
import { Component, Prop, Vue } from 'vue-property-decorator';


@Component({ components: {} })
export default class UserComponent extends Vue {
  @Prop({ required: false }) userProp!: UserModel;
  @Prop({ required: false }) userId!: number;
  loading = true;
  userStore = userStore;
  courseStore = courseStore;
  userModel: UserModel | null = null;

  get name() {
    if (this.userModel && this.userModel.first_name && this.userModel.last_name)
      return `${this.userModel.first_name} ${this.userModel.last_name}`;
    return this.userModel?.username;
  }

  get picUrl() {
    if (this.userModel && this.userModel.avatar_url)
      return this.userModel.thumbnail;
    return "https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png";
  }

  get warning() {
    if (!this.courseStore.currentCourse)
      return false;
    if (this.userId)
      return !(this.userId in this.userStore.currentCourseStudents);
    return !(this.userProp.id in this.userStore.currentCourseStudents);
  }

  async created() {
    if (!this.userProp && !this.userId)
      throw Error();
    if (this.userProp)
      this.userModel = this.userProp;
    if (this.userId)
      this.userModel = this.userStore.currentCourseStudents[this.userId];
    if (typeof this.userModel === 'undefined')
      this.userModel = await this.userStore.fetchUserById(this.userId)
    this.loading = false;
  }
}
</script>

<template>
  <div class="user-component">
    <div class="user-component--wrapper">
      <img alt="" class="user-component--avatar" v-bind:src="picUrl"/>
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
