<template>
<div>
  <cv-button size="field" kind="secondary" @click="createNewLink">
    Сгенерировать ссылку-приглашения
  </cv-button>
  <cv-structured-list :condensed="false">
    <template slot="headings">
      <cv-structured-list-heading>Links</cv-structured-list-heading>
      <cv-structured-list-heading>Amount of usages</cv-structured-list-heading>
      <template slot="items">
        <cv-structured-list-item checked v-for="k in Links" :key="k.course">
          <cv-structured-list-data>{{ k.link }}</cv-structured-list-data>
          <cv-structured-list-data>{{ k.usages }}</cv-structured-list-data>
        </cv-structured-list-item>
      </template>
    </template>
  </cv-structured-list>
</div>
</template>

<!-- TODO: get link from api -->
<script lang="ts">
import {Component, Vue, Prop} from "vue-property-decorator";
import LinkModel from "@/models/LinkModel";
import axios from 'axios';
import CourseModel from "@/models/CourseModel";

@Component({ components: {} })
export default class CourseView extends Vue {
  @Prop({ required: true }) counter!: number;
  @Prop({ required: true }) course!: CourseModel;

  Links: Array<LinkModel> = []

  async createNewLink() {
    const request = axios.post('http://localhost:8000/api/courselink/', {course: this.course.id, usages: this.counter});
    await axios.get('http://localhost:8000/api/courselink/')
      .then(response => {
        this.Links = response.data.filter((x: LinkModel) => x.course == this.course.id)
      })
      .catch(error => {
        console.log(error);
      })
  }

}
</script>

<style scoped>

</style>
