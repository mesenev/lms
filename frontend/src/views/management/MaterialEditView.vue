<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <h1 class="main-title">Редактирование материала</h1>
      <div class="material-hide-button-container">
        <cv-button-skeleton v-if="changingVisibility || loading" kind="ghost"/>
        <cv-button v-else
                   class="material-hide-button"
                   :icon="hiddenIcon"
                   kind="ghost"
                   @click="changeMaterialVisibility">
          {{
            (currentMaterial.is_teacher_only) ?
              "Открыть материал для студентов" : "Скрыть материал от студентов"
          }}
        </cv-button>
      </div>
    </div>
    <cv-loading v-if="loading"/>
    <div v-else class="bx--row content">
      <div class="edit-container-wrapper bx--col-lg-5">
        <confirm-modal :modal-trigger="confirmModalTrigger"
                       :text="approvedText"
                       :approve-handler="deleteHandler"/>
        <div class="edit-container">
          <cv-inline-notification
            v-if="showNotification"
            :kind="notificationKind"
            :sub-title="notificationText"
            @close="hideSuccess"
          />
          <div class="edit-container-header">
            <cv-text-input label="Заголовок"
                           type="text"
                           v-model="materialEdit.name"/>
            <cv-dropdown class="material-type-dropdown"
                         @change="changeMaterialContent"
                         placeholder="Выберите тип"
                         label="Тип материала"
                         v-model="materialEdit.content_type">
              <cv-dropdown-item value="text">Текст</cv-dropdown-item>
              <cv-dropdown-item value="url">Ссылка</cv-dropdown-item>
              <cv-dropdown-item value="video">Видео</cv-dropdown-item>
            </cv-dropdown>
          </div>
          <cv-text-area v-if="isTextType"
                        label="Содержимое"
                        class="text-area"
                        v-model="materialEdit.content"/>
          <cv-text-input v-if="isUrlType"
                         placeholder="Вставьте ссылку"
                         label="Ссылка"
                         v-model="materialEdit.content"/>
          <cv-text-input v-if="isVideoType"
                         placeholder="Вставьте ссылку на видео или добавьте вложение"
                         label="Видео"
                         v-model="materialEdit.content"/>
          <p class="attachments-list-label">Вложения</p>
          <div class="attachments-list-container">
            <cv-structured-list class="attachments-list">
              <template slot="items">
                <cv-structured-list-item class="attachments-list-item"
                                         v-for="element in this.currentAttachments"
                                         :key="element.id">
                  <attachments-component-list :attachment="element"
                                              @show-confirm-modal="showConfirmModal">
                  </attachments-component-list>
                </cv-structured-list-item>
              </template>
            </cv-structured-list>
          </div>
          <input type="file"
                 id="files_input"
                 ref="files"
                 multiple
                 :disabled="attachmentLoading"
                 @change="uploadFiles($event.target.files)"/>
          <div class="action-btns">
            <cv-button kind="danger" @click="showConfirmModal(material)">
              Удалить
            </cv-button>
            <cv-button :disabled="canChangeMaterial"
                       @click="ChangeMaterial">
              Изменить
            </cv-button>
          </div>
        </div>
      </div>
      <div class="preview-container bx--col-lg-6">
        <h4 class="title" v-if="materialEdit.name.length > 0"> {{ materialEdit.name }} </h4>
        <h4 v-else>Введите название материала</h4>
        <youtube v-if="isVideoType && isYoutubeFormat" :video-id="youtubeUrl"
                 ref="youtube"
                 player-width="100%"/>
        <vue-markdown v-else :source="materialEdit.content" :html="true" class="markdown"/>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
import MaterialModel from '@/models/MaterialModel';
import materialStore from '@/store/modules/material';
import _ from 'lodash';
import VueMarkdown from 'vue-markdown'
import Vue from 'vue';
import { Component, Prop } from 'vue-property-decorator';
import api from '@/store/services/api';
import AttachmentModel from "@/models/Attachment";
import AttachmentsComponentList from '@/components/lists/AttachmentsComponentList.vue';
import ConfirmModal from "@/components/ConfirmModal.vue";
import router from "@/router";
import viewOff from '@carbon/icons-vue/es/view--off/32';
import view from '@carbon/icons-vue/es/view/32';
import VueYouTubeEmbed from "vue-youtube-embed";
import { getIdFromURL } from "vue-youtube-embed";

Vue.use(VueYouTubeEmbed);

@Component({ components: { VueMarkdown, AttachmentsComponentList, ConfirmModal } })
export default class MaterialEditView extends Vue {
  @Prop() materialId!: number;
  private materialStore = materialStore;
  material: MaterialModel = {
    id: NaN,
    lesson: NaN,
    name: '',
    content_type: '',
    content: '',
    is_teacher_only: false,
  }

  materialEdit: MaterialModel = { ...this.material }
  showNotification = false;
  notificationKind = 'success';
  notificationText = '';
  loading = true;
  confirmModalTrigger = false;
  approvedText = '';
  deletingValueId: number | null = null;
  attachmentLoading = false;
  changingVisibility = false;

  hideSuccess() {
    this.showNotification = false;
  }

  async created() {
    const material = await this.materialStore.fetchMaterialById(this.materialId);
    await this.materialStore.fetchAttachmentsByMaterialId(this.materialId);
    if (material) {
      this.materialStore.setCurrentMaterial(material);
      await this.materialStore.fetchMaterialsByLessonId(material.lesson);
      this.material = this.materialStore.currentMaterial;
      this.materialEdit = _.cloneDeep(this.material)
    }
    this.loading = false;
  }

  async uploadFiles(fileList: File[]) {
    this.attachmentLoading = true;
    for (const element of fileList) {
      const fd = new FormData();
      fd.append('id', '-1')
      fd.append('name', element.name)
      fd.append('material', this.material.id.toString())
      fd.append('file_url', element)
      fd.append('file_format', element.type)
      await this.materialStore.createAttachment(fd).catch(error => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так: ${error.message}`;
        this.showNotification = true;
      })
    }
    await this.updateAttachments();
    const input = window.document.getElementById('files_input') as HTMLInputElement
    input.value = '';
    this.attachmentLoading = false;
  }

  get currentMaterial(): MaterialModel {
    return this.materialStore.currentMaterial;
  }

  get currentAttachments(): Array<AttachmentModel> {
    return this.materialStore.currentAttachments;
  }

  get isMaterialEmpty(): boolean {
    return this.materialEdit.name.length === 0 || this.materialEdit.content.length === 0;
  }

  get isTextType() {
    return this.materialEdit.content_type === 'text';
  }

  get isUrlType() {
    return this.materialEdit.content_type === 'url';
  }

  get isVideoType() {
    return this.materialEdit.content_type === 'video';
  }

  get isYoutubeFormat() {
    return this.materialEdit.content.includes('https://www.youtube.com/');
  }

  get youtubeUrl() {
    return getIdFromURL(this.materialEdit.content);
  }

  get canChangeMaterial(): boolean {
    return _.isEqual(this.currentMaterial, this.materialEdit) || this.isMaterialEmpty
  }

  get hiddenIcon() {
    return (this.currentMaterial.is_teacher_only) ? viewOff : view;
  }

  determineIsAttachmentOrMaterial(model: AttachmentModel | MaterialModel): model is AttachmentModel {
    return (model as AttachmentModel).file_url !== undefined;
  }

  showConfirmModal(deletingValue: AttachmentModel | MaterialModel) {
    let deletingText = 'Удалить материал: ';
    if (this.determineIsAttachmentOrMaterial(deletingValue)) {
      deletingText = 'Удалить вложение: ';
    }
    this.deletingValueId = deletingValue.id;
    this.approvedText = `${deletingText}${deletingValue.name}`;
    this.confirmModalTrigger = !this.confirmModalTrigger;
  }

  changeMaterialContent() {
    if (this.isTextType) {
      this.materialEdit.content = '### материал';
    } else {
      this.materialEdit.content = '';
    }
  }

  async changeMaterialVisibility() {
    this.changingVisibility = true;
    await this.materialStore.patchMaterialVisibility({
      is_teacher_only: !this.currentMaterial.is_teacher_only,
      id: this.currentMaterial.id
    }).then(() => {
      this.updateAfterChangeMaterials(this.currentMaterial, this.currentMaterial);
      this.materialEdit.is_teacher_only = this.currentMaterial.is_teacher_only;
    })
    this.changingVisibility = false;
  }

  async ChangeMaterial() {
    await api.patch(`/api/material/${this.materialEdit.id}/`, this.materialEdit)
      .then(response => {
        this.notificationKind = 'success';
        this.notificationText = 'Материалы успешно изменены';
        this.updateAfterChangeMaterials(this.material, this.materialEdit);
        this.material = response.data;
        this.materialStore.setCurrentMaterial(this.material);
      })
      .catch(error => {
        this.notificationText = `Что-то пошло не так: ${error.message}`;
        this.notificationKind = 'error';
      })
      .finally(() => this.showNotification = true);
  }

  async deleteHandler() {
    if (this.approvedText.includes('материал')) {
      await this.deleteMaterial();
    } else {
      await this.deleteAttachment();
    }
  }

  async deleteAttachment() {
    if (!this.deletingValueId)
      throw Error;
    await this.materialStore.deleteAttachment(this.deletingValueId)
      .catch(error => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так: ${error.message}`
        this.showNotification = true;
      })
  }

  async deleteMaterial() {
    if (!this.deletingValueId)
      throw Error;
    await api.delete(`/api/material/${this.deletingValueId}/`)
      .then(async () => {
        await this.updateAfterDeleteMaterials();
        await router.push({
          name: 'LessonView',
          params: { lessonId: this.material.lesson.toString() }
        })
      })
      .catch(error => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так: ${error.message}`;
        this.showNotification = true;
      })
  }

  async updateAttachments() {
    await this.materialStore.fetchAttachmentsByMaterialId(this.materialId);
  }

  async updateAfterDeleteMaterials() {
    const materials = await this.materialStore.fetchMaterialsByLessonId(this.currentMaterial.lesson);
    this.materialStore.setMaterials({
      [this.currentMaterial.lesson]: materials.filter(
        x => x.id !== this.currentMaterial.id
      )
    });
  }

  async updateAfterChangeMaterials(oldMaterial: MaterialModel, newMaterial: MaterialModel) {
    let materials = await this.materialStore.fetchMaterialsByLessonId(oldMaterial.lesson);
    materials = materials.filter(x => x.id !== oldMaterial.id);
    materials.push(newMaterial);
    materials.sort((a, b) => a.id - b.id);
    this.materialStore.setMaterials({ [newMaterial.lesson]: materials });
  }
}
</script>

<style scoped lang="stylus">
.material-hide-button-container
  margin-left 1rem

.preview-container
  padding 1rem
  color var(--cds-text-01)
  background-color var(--cds-ui-01)
  border 2px black solid

.markdown
  overflow-wrap break-word
  margin-top 10px
  overflow-y auto
  max-height 40rem

.title
  overflow-wrap break-word

.content
  margin-top 1rem

.edit-container
  padding 1rem
  background-color var(--cds-ui-01)

.edit-container-header
  display flex
  gap 1rem
  justify-content space-between

.cv-text-input
  /deep/ .bx--label
    margin-top 2px

.material-type-dropdown
  max-width 10rem

  /deep/ .bx--dropdown
    background-color var(--cds-ui-background)

  /deep/ .bx--dropdown__wrapper.bx--list-box__wrapper
    align-self end

/deep/ .bx--list-box__field
  display flex

/deep/ .bx--text-input
  margin-bottom 1rem
  background-color var(--cds-ui-background)

.text-area >>> .bx--text-area
  background-color var(--cds-ui-background)
  min-height 13rem
  resize none
  margin-bottom 1rem

#files_input
  color var(--cds-text-01)

.action-btns
  display flex
  justify-content space-between
  margin-top 1rem

.attachments-list-label
  font-size var(--cds-label-01-font-size, 0.75rem)
  font-weight var(--cds-label-01-font-weight, 400)
  line-height var(--cds-label-01-line-height, 1.34)
  letter-spacing var(--cds-label-01-letter-spacing, 0.32px)
  display: inline-block
  margin-bottom 0.5rem
  color: var(--cds-text-02, #525252)
  vertical-align baseline

.attachments-list-container
  overflow auto
  max-height 200px
  margin-bottom 0.5rem
  color var(--cds-text-01)

.attachments-list
  margin-top 1px
  margin-bottom 0

.attachments-list-item
  border-right 1px solid var(--cds-ui-03)
  border-left 1px solid var(--cds-ui-03)

code {
  color: #f66;
}

</style>
