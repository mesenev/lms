<template>
  <div v-if="!loading" class="bx--grid bx--grid--narrow">
    <div class="bx--row header">
      <h1 class="header-title"> {{ user.first_name + ' ' + user.last_name }}</h1>
    </div>
    <div class="bx--row content">
      <div class="avatar-container">
        <Avatar class="image" :avatar_url="user.avatar_url"/>
        <EditAvatarModal class="image-edit-icon" v-if="!guestMode" :user="user"/>
      </div>
      <div class="bx--col">
        <div class="courses-block">
          <h3 v-if="!guestMode">Мои курсы</h3>
          <h3 v-else>Курсы пользователя</h3>
          <cv-structured-list v-if="!loading" selectable>
            <template slot="items">
              <cv-structured-list-item class="item" v-for="course in filterCourses"
                                       :key="course.id">
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
                  <cv-structured-list-data>{{
                      user.email || 'error@mail.ru'
                    }}
                  </cv-structured-list-data>
                </cv-structured-list-item>
                <cv-structured-list-item>
                  <cv-structured-list-data>Аккаунт Cats</cv-structured-list-data>
                  <cv-structured-list-data class="cats_status" >
                    <cv-inline-loading active v-if="cats_loading"/>
                    <span v-else> {{ cats_status }}</span>
                  </cv-structured-list-data>
                </cv-structured-list-item>
              </template>
            </cv-structured-list>
          </div>
          <div class="info-btns">
            <AddCatsModal v-if="!guestMode" class="add-cats"/>
            <ChangePasswordModal v-if="!guestMode" class="change-pass"/>
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
import { Component, Prop, Vue } from 'vue-property-decorator';
import axios from "axios";

@Component({
  components: {
    Avatar, Course, AddCatsModal, UserView,
    Edit32, EditAvatarModal, ChangePasswordModal,
  },
})
export default class ProfileView extends Vue {
  @Prop({ required: true }) userId!: number;
  private store = courseStore;
  loading = true;
  cats_loading = true;
  cats_account = "";
  searchValue = "";
  user = userStore.user;

  guestMode = false;

  async created() {
    await this.store.fetchUserCourses();
    if (this.userId != this.user.id) {
      this.guestMode = true;
      this.user = await userStore.fetchUserById(this.userId);
    }
    this.loading = false;
    await this.fetch_cats_account();
  }

  async fetch_cats_account() {
    await axios.get(`/api/cats_account/?user_id=${this.userId}`)
      .then(response => {
        if (response.data)
          this.cats_account = response.data[0].username;
      })
      .catch(error => {
        debugger;
        console.log(error);
      })
    this.cats_loading = false;
  }

  get filterCourses() {
    return this.courses.filter(c => {
      return c.name.toLowerCase().includes(this.searchValue.toLowerCase())
    })
  }

  get courses() {
    return this.store.courses;
  }

  get cats_status() {
    return (this.cats_account) ? this.cats_account : 'Не привязан ⚠️';
  }
}
</script>

<style scoped lang="stylus">

.avatar-container
  padding-right 3rem

.image
  margin-top 2rem
  border 1px solid rgba(0, 0, 0, 0.3)
  border-radius 150%

.image-edit-icon
  margin-top 0.8rem
  text-align center

.header-title
  margin-left -2rem
  margin-top 2rem

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
  margin-top 0
  display flex
  flex-direction row
  justify-content center

.change-pass
  margin-left 1rem

.info
  margin-bottom 20px

.list
  margin-top 2rem
  padding-bottom 0
  margin-bottom 0

///


</style>
