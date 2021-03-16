<template>
  <div>
    <cv-button kind="secondary" size="field" @click="createNewLink">
      Сгенерировать ссылку-приглашения
    </cv-button>
    <cv-structured-list :condensed="false">
      <template slot="headings">
        <cv-structured-list-heading>
          Доступные ссылки
        </cv-structured-list-heading>
        <cv-structured-list-heading>Количество использований</cv-structured-list-heading>
      </template>
      <template slot="items">
        <cv-structured-list-item v-if="loading">
        </cv-structured-list-item>
        <cv-structured-list-item checked v-for="k in Links" :key="k.link" v-else>
          <cv-structured-list-data>
            {{ k.link }}
            <component :is="CopyLink16"
                       class="icon cross"
                       @click="copyLink(k.link)">
            </component>
          </cv-structured-list-data>
          <cv-structured-list-data>{{ k.usages }}
            <component :is="TrashCan16"
                       class="icon cross"
                       @click="deleteLink(k.link)">
            </component>
          </cv-structured-list-data>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
</template>

<script lang="ts">
import LinkModel from "@/models/LinkModel";
import CopyLink16 from '@carbon/icons-vue/lib/copy--link/16';
import TrashCan16 from '@carbon/icons-vue/lib/trash-can/16'
import axios from 'axios';
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({})
export default class LinksManagerComponent extends Vue {
  @Prop({required: true}) counter!: number;
  @Prop({required: true}) courseId!: number;
  loading = true;
  Links: Array<LinkModel> = [];
  TrashCan16 = TrashCan16
  CopyLink16 = CopyLink16

  async created() {
    await axios.get(
      '/api/courselink/', { params: { course: this.courseId } },
    ).then(response => {
        this.Links = response.data.filter((x: LinkModel) => x.usages > 0);
      },
    ).catch(error => {
      console.log(error);
    })
    this.loading = false;
  }

  async createNewLink() {
    axios.post('/api/courselink/',
      { course: this.courseId, usages: this.counter })
      .then(response => {
        this.Links.push(response.data);
        this.Links = [...this.Links];
      })
      .catch(error => {
        console.log(error);
      });
  }

  deleteLink(link: string) {
    this.Links = this.Links.filter((x: LinkModel) => x.link != link);
    axios.delete(`/api/delete-link/${link}/`);
  }

  copyLink(link: string) {
    this.$clipboard(axios.defaults.baseURL + '/course-registration/' + link);
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  $clipboard(arg0: string) {
    throw new Error("Method not implemented.");
  }

}
</script>

<style scoped>
.cross {
  cursor: pointer;
}
</style>
