<template>
  <div>
    <cv-button kind="secondary" size="field" @click="createNewLink">
      Сгенерировать ссылку-приглашения
    </cv-button>
    <cv-structured-list :condensed="false">
      <template slot="headings">
        <cv-structured-list-heading>
          Links
        </cv-structured-list-heading>
        <cv-structured-list-heading>Amount of usages</cv-structured-list-heading>
      </template>
      <template slot="items" >
        <cv-structured-list-item v-if="loading">
        </cv-structured-list-item>
        <cv-structured-list-item checked v-for="k in Links" :key="k.link" v-else>
          <cv-structured-list-data >{{ k.link }}
          </cv-structured-list-data>
          <cv-structured-list-data>{{ k.usages }}</cv-structured-list-data>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
</template>

<script lang="ts">
import LinkModel from "@/models/LinkModel";
import axios from 'axios';
import {Component, Prop, Vue} from "vue-property-decorator";
import Save20 from '@carbon/icons-vue/es/save/20'


@Component({components: {
    Save20
  }})
export default class LinksManagerComponent extends Vue {
  @Prop({required: true}) counter!: number;
  @Prop({required: true}) courseId!: number;
  loading = true;
  Links: Array<LinkModel> = [];

  async created() {
    await axios.get('http://localhost:8000/api/courselink/')
      .then(response => {
        this.Links = response.data.filter((x: LinkModel) => x.course == this.courseId);
      })
      .catch(error => {
        console.log(error);
      })
    this.loading = false;
  }

  async createNewLink() {
    const request = axios.post('http://localhost:8000/api/courselink/',
      {course: this.courseId, usages: this.counter})
      .then(response => {
        this.Links.push(response.data);
        this.Links = [...this.Links];
      })
      .catch(error => {
        console.log(error);
      });
  }

}
</script>

<style scoped>

</style>
