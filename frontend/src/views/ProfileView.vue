<template>
  <div class="bx--grid bx--grid--narrow">
    <div class="bx--row header">
      <h1> {{Role}} {{ Name }}</h1>
    </div>
    <div class="bx--row content">
      <div class="bx--col, avatarblock">
        <div class="avatar-block">
          <Avatar/>
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
          <cv-data-table-skeleton v-else :columns="1" :rows="3" />
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
                  <cv-structured-list-data >Б8119-01.03.02</cv-structured-list-data>
                </cv-structured-list-item>
                <cv-structured-list-item>
                  <cv-structured-list-data>Почта</cv-structured-list-data>
                  <cv-structured-list-data>mail@mesenev.ru</cv-structured-list-data>
                </cv-structured-list-item>
                <cv-structured-list-item>
                  <cv-structured-list-data>Аккаунт Cats</cv-structured-list-data>
                  <cv-structured-list-data class = "cats_status">Не привязан</cv-structured-list-data>
                </cv-structured-list-item>
                <div class="info-btns">
                  <cv-button class="cats-btn" kind="primary">Привязать аккаунт cats</cv-button>
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

import { courseStore } from '@/store';
import { Component, Prop, Vue } from 'vue-property-decorator';
import Course from "@/components/Course.vue";
import Avatar from "@/components/Avatar.vue";

@Component({ components: {Avatar, Course } })
export default class ProfileView extends Vue {

  @Prop() courseId!: number;
  private store = courseStore;
  loading = true;
  searchValue = "";
  Name = "Гринёв Максим";
  Role = "Студент";


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
  display flex
  flex-direction row

.cats-btn
  margin-top 20px
  margin-left 20px

.pass-btn
  margin-top 20px
  margin-left 20px

.info
  margin-bottom 20px

.list
  margin-top 70px
</style>
