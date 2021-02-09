<template>
  <div v-if="!loading" class="bx--grid bx--grid--narrow">
    <div class="bx--row header">
      <h1> {{ user.first_name + ' ' + user.last_name }}</h1>
    </div>
    <div class="bx--row content">
      <div class="container">
        <Avatar class="image" :avatar_url="user.avatar_url"/>
        <EditAvatarModal v-if="!guestMode" :user="user"/>
      </div>
      <div class="bx--col">
        <div class="courses-block">
          <h3 v-if="!guestMode">Мои курсы</h3>
          <h3 v-else>Курсы пользователя</h3>
          <cv-structured-list v-if="!loading" selectable>
            <template slot="items">
              <cv-structured-list-item class="item" v-for="course in filterCourses" :key="course.id">
                <Course :courseProp='course'/>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
          <cv-data-table-skeleton v-else :columns="1" :rows="3"/>
        </div>
      </div>
      <div class="bx--col">
        <div class="info-block">
          <h3 class="info">Информация</h3>
          <div class="list">
            <cv-structured-list>
              <template slot="items">
                <cv-structured-list-item>
                  <cv-structured-list-data>Учебная группа</cv-structured-list-data>
                  <cv-structured-list-data>Б8119-01.03.02</cv-structured-list-data>
                </cv-structured-list-item>
                <cv-structured-list-item>
                  <cv-structured-list-data>Почта</cv-structured-list-data>
                  <cv-structured-list-data>{{ user.email || 'error@mail.ru' }}</cv-structured-list-data>
                </cv-structured-list-item>
                <cv-structured-list-item>
                  <cv-structured-list-data>Аккаунт Cats</cv-structured-list-data>
                  <cv-structured-list-data class="cats_status">Не привязан</cv-structured-list-data>
                </cv-structured-list-item>
                <div class="info-btns">
                  <AddCatsModal v-if="!guestMode" class="add-cats"/>
                  <ChangePasswordModal v-if="!guestMode" class="change-pass"/>
                </div>
              </template>
            </cv-structured-list>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

import AddCatsModal from "@/components/AddCatsModal.vue";
import Avatar from "@/components/Avatar.vue";
import ChangePasswordModal from "@/components/ChangePasswordModal.vue";
import Course from "@/components/lists/CourseListComponent.vue";
import UserView from "@/components/UserComponent.vue";
import courseStore from '@/store/modules/course';
import userStore from '@/store/modules/user';
import EditAvatarModal from "@/views/EditAvatarModal.vue";
import Edit32 from '@carbon/icons-vue/es/edit/32';
import {Component, Prop, Vue} from 'vue-property-decorator';

@Component({
  components: {
    Avatar, Course, AddCatsModal, UserView,
    Edit32, EditAvatarModal, ChangePasswordModal,
  },
})
export default class ProfileView extends Vue {
  @Prop({required: true}) userId!: number;
  private store = courseStore;
  loading = true;
  searchValue = "";
  user = userStore.user;

  guestMode = false;

  async created() {
    await this.store.fetchCourses();
    if (this.userId != this.user.id) {
      this.guestMode = true;
      console.log(this.userId);
      console.log("УРА")
      this.user = await userStore.fetchUserById(this.userId);
      console.log(this.user)
    }
    this.loading = false;
  }

  get filterCourses() {
    return this.courses.filter(c => {
      return c.name.toLowerCase().includes(this.searchValue.toLowerCase())
    })
  }

  get courses() {
    return this.store.courses;
  }

}
</script>

<style scoped lang="stylus">

// avatar edit//////////////////


/////////////////////////


.courses-block
  margin 50px

.info-block
  margin 50px

.cats_status
  font-weight bold

.bx--col
  margin 1%
  background-color var(--cds-ui-background);

.info-btns
  padding-top 20px;
  cursor: pointer;
  display flex;
  flex-direction row;

.info-btns:after
  clear: both;
  display: table;

.info
  margin-bottom 20px

.list
  margin-top 70px

///


</style>
