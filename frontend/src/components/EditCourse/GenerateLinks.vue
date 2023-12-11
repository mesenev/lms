<template>
  <div>
    <cv-button kind="secondary" @click="showModal">Создать ссылку-приглашение</cv-button>
    <cv-modal :visible="modalVisible"
              size="sm"
              class="generate-link-modal"
              @modal-hidden="modalHidden">
      <template v-slot:title>Создание ссылки-приглашения</template>
      <template v-slot:content>
        <div class="link-content">
          <cv-inline-notification
            v-if="showNotification"
            :kind="notificationKind"
            :sub-title="notificationText"
            @close="hideNotification"
          />
          <div class="input-link-container">
            <cv-number-input
              :light="false"
              :label="'Выберите количество учеников'"
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
              <template v-slot:items>
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

<script lang="ts" setup>
import CopyLink16 from '@carbon/icons-vue/lib/copy--link/16';
import TrashCan16 from '@carbon/icons-vue/lib/trash-can/16';
import AddAlt24 from '@carbon/icons-vue/lib/add--alt/24';
import { onMounted, ref } from "vue";
import type { LinkModel } from "@/models/LinkModel";
import api from "@/stores/services/api";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";

const props = defineProps({
  groupId: { type: Number, required: true }
})

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const loading = ref(true);
const Links = ref<Array<LinkModel>>([]);
const counter = ref(1);
const modalVisible = ref(false);

onMounted(async () => {
  await api.get(
    '/api/courselink/', { params: { group: props.groupId } },
  ).then(response => {
      Links.value = response.data.filter((x: LinkModel) => x.usages > 0);
    },
  ).catch(error => {
    console.log(error);
  })
  loading.value = false;
})

function showModal() {
  modalVisible.value = true;
}

function modalHidden() {
  modalVisible.value = false;
}

async function createNewLink() {
  api.post('/api/courselink/',
    { group: props.groupId, usages: counter.value })
    .then(response => {
      Links.value.push(response.data);
      Links.value = [...Links.value];
    })
    .catch(error => {
      notificationKind.value = 'error';
      notificationText.value = `Что-то пошло не так: ${error.message}`;
      showNotification.value = true;
    });
}

function deleteLink(link: string) {
  api.delete(`/api/delete-link/${link}/`)
    .then(() => {
      Links.value = Links.value.filter((x: LinkModel) => x.link != link);
    })
    .catch(error => {
      notificationKind.value = 'error';
      notificationText.value = `Что-то пошло не так: ${error.message}`;
      showNotification.value = true;
    });
}

function copyLink(link: string) {
  navigator.clipboard.writeText(window.location.origin + '/course-registration/' + link);
}

</script>

<style scoped lang="stylus">
:deep() .bx--modal-content:focus
  outline none

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
