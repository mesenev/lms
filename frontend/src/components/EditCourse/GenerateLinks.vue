<template>
  <div>
    <cv-button kind="secondary" @click="showModal">Создать ссылку-приглашение</cv-button>
    <cv-modal :visible="modalVisible"
              class="generate-link-modal"
              size="small"
              @modal-hidden="modalHidden">
      <template slot="title">Создание ссылки-приглашения</template>
      <template slot="content">
        <div class="link-content">
          <div class="input-link-container">
            <cv-number-input
              :light="false"
              :label="'Выберите количество учеников курса'"
              :min="1"
              :step="1"
              v-model="counter"
              class="create-link-input">
            </cv-number-input>
            <cv-icon-button
              kind="secondary"
              :icon="AddAlt24"
              label="Создать ссылку"
              tip-position="top"
              size="field"
              @click="createNewLink"
              class="generate-btn"/>
          </div>
          <div class="headings">
            <p class="heading">Доступные ссылки</p>
            <p class="heading">Количество использований</p>
          </div>
          <div class="links-list-container">
            <cv-structured-list class="links-list">
              <template slot="items">
                <cv-structured-list-item v-if="loading">
                </cv-structured-list-item>
                <cv-structured-list-item checked v-for="k in Links" :key="k.link" v-else>
                  <cv-structured-list-data>
                    <cv-link class="link" @click="copyLink(k.link)" title="Скопировать ссылку">
                      {{ k.link }}
                    </cv-link>
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
        </div>
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import LinkModel from "@/models/LinkModel";
import CopyLink16 from '@carbon/icons-vue/lib/copy--link/16';
import TrashCan16 from '@carbon/icons-vue/lib/trash-can/16';
import AddAlt24 from '@carbon/icons-vue/lib/add--alt/24';
import api from '@/store/services/api';
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({})
export default class LinksManagerComponent extends Vue {
  @Prop({required: true}) courseId!: number;
  loading = true;
  Links: Array<LinkModel> = [];
  counter = 1;
  AddAlt24 = AddAlt24
  TrashCan16 = TrashCan16
  CopyLink16 = CopyLink16
  modalVisible = false;

  async created() {
    await api.get(
      '/api/courselink/', { params: { course: this.courseId } },
    ).then(response => {
        this.Links = response.data.filter((x: LinkModel) => x.usages > 0);
      },
    ).catch(error => {
      console.log(error);
    })
    this.loading = false;
  }

  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
  }

  async createNewLink() {
    api.post('/api/courselink/',
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
    api.delete(`/api/delete-link/${link}/`);
  }

  copyLink(link: string) {
    this.$copyText(window.location.origin + '/course-registration/' + link);
  }

}
</script>

<style scoped lang="stylus">
.generate-link-modal >>> .bx--modal-content
  display flex
  justify-content center

.link-content
  max-width 25rem

.headings
  margin-top 1rem
  display flex
  flex-direction row
  justify-content space-evenly

.heading
  max-width 8rem

.links-list-container
  max-height 15rem
  overflow-y auto
  margin-top 1rem

.links-list
  margin-bottom 0

.link
  cursor pointer

.input-link-container
  display flex
  flex-direction row

.generate-btn
  margin-left 1rem
  height 2rem
  align-self flex-end

.cross {
  cursor: pointer;
}
</style>
