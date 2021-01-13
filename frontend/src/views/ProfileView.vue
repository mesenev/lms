<template>
  <div class="bx--grid bx--grid--narrow">
    <div class="bx--row header">
      <h1>{{ Name }}</h1>
    </div>
    <div class="bx--row content">
      <div class="bx--col">
        <Avatar/>
      </div>
      <div class="bx--col">
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
      <div class="bx--col">
        <cv-structured-list>
          <template slot="headings">
            <h3>Информация</h3>
          </template>
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
            <cv-button>Привязать аккаунт cats</cv-button>
          </template>
        </cv-structured-list>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

import { courseStore } from '@/store';
import { Component, Prop, Vue } from 'vue-property-decorator';
import Course from "@/components/Course.vue";
import Avatar from "@/components/Avatar";


@Component({ components: {Avatar, Course } })
export default class ProfileView extends Vue {

  @Prop() courseId!: number;
  private store = courseStore;
  loading = true;
  searchValue = "";
  Name = "Павел Месенев";

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

.cats_status
  font-weight bold;

</style>
