<template>
  <div class="bx--grid bx--grid--narrow">
    <div class="bx--row header">
      <h1> {{ user.first_name + ' ' + user.last_name }}</h1>
    </div>
    <div class="bx--row content">
      <div class="bx--col, avatarblock">
        <div class="container">
          <Avatar class="image"/>
          <EditAvatarModal class="overlay"/>
        </div>
      </div>
      <div class="bx--col">
        <div class="courses-block">
          <h3>Мои курсы</h3>
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
                  <AddCatsModal class="add-cats"/>
                  <cv-button class="pass-btn" kind="ghost">Сменить пароль</cv-button>
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

import {courseStore, userStore} from '@/store';
import {Component, Prop, Vue} from 'vue-property-decorator';
import Course from "@/components/Course.vue";
import Avatar from "@/components/Avatar.vue";
import AddCatsModal from "@/components/AddCatsModal.vue";
import UserView from "@/views/UserView.vue";
import Edit32 from '@carbon/icons-vue/es/edit/32';
import EditAvatarModal from "@/views/EditAvatarModal.vue";

@Component({components: {Avatar, Course, AddCatsModal, UserView, Edit32, EditAvatarModal}})
export default class ProfileView extends Vue {

  @Prop() courseId!: number;
  private store = courseStore;
  loading = true;
  searchValue = "";

  user = userStore.user;

  async created() {
    await this.store.fetchCourses();
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
.edit-avatar-btn
  margin-left 35px
  margin-top 30px

.avatar-block
  margin 50px

.courses-block
  margin 50px

.info-block
  margin 50px

.cats_status
  font-weight bold

.avatarblock
  background-color var(cds-ui-0)

.bx--col
  margin 1%
  background-color var(--cds-ui-background);

.info-btns
  padding-top 20px;
  float left;
  cursor: pointer;
  clear: both;
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


.container {
  position: relative;
  width: 50%;
  max-width: 300px;
}

.image {
  display: block;
  width: 100%;
  height: auto;
}

.overlay {
  position: absolute;
  bottom: 0;
  transition: .5s ease;
  opacity: 0;
  font-size: 20px;
  text-align: center;
  margin-left: 110px;
  margin-top: 35px;
  padding: 0 auto;
}


.container:hover .overlay {
  opacity: 1;
}


</style>
