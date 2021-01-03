<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>Список курсов</h1>
    </div>
    <div class=" bx--row">
      <div class="items bx--col-lg-8">
        <cv-search
          label="label"
          placeholder="search"
          v-model.trim="searchValue"
        >
        </cv-search>
        <cv-structured-list selectable>
          <template slot="items">
            <cv-structured-list-item class="item" v-for="course in filterCourses" :key="course.id">
              <Course :courseProp='course'/>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
      </div>
      <div class="bx--col-lg-8">
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Course from '@/components/Course.vue';
import { mainStore } from '@/store';
import axios from 'axios';
import Vue from 'vue';
import Component from 'vue-class-component';

@Component({ components: { Course } })
export default class HomeView extends Vue {
  private store = mainStore;
  searchValue = "";
  private loading = true;
  private errored = false;

  async created() {

    axios.get('http://localhost:8000/api/course/')
      .then(response => {
        this.store.setCourses(response.data);
      })
      .catch(error => {
        console.log(error);
        this.errored = true;
      })
      .finally(() => (this.loading = false));
  }

  get courses() {
    return this.store.getCourses;
  }

  get filterCourses() {
    return this.courses.filter(c => {
      return c.name.toLowerCase().includes(this.searchValue.toLowerCase())
    })
  }
}
</script>

<style lang="stylus">
.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.items
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

  .bx--structured-list-thead
    display none

.item
  min-height 85px
</style>
