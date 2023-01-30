<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1 class="main-title">Редактирование материала</h1>
    </div>
    <cv-loading v-if="loading"/>
    <div v-else class="bx--row content">
      <div class="edit-container-wrapper bx--col-lg-5">
        <confirm-modal :modal-trigger="confirmModalTrigger"
                       :text="approvedText"
                       :approve-handler="deleteAttachment"/>
        <div class="edit-container">
          <cv-inline-notification
            v-if="showNotification"
            :kind="notificationKind"
            :sub-title="notificationText"
            @close="hideSuccess"
          />
          <cv-text-input label="Заголовок"
                         type="text"
                         v-model="materialEdit.name"/>
          <cv-text-area label="Содержимое"
                        class="text-area"
                        v-model="materialEdit.content">
          </cv-text-area>
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
          <div class="change__btn">
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
        <vue-markdown :source="materialEdit.content" html="false" class="markdown"/>
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
  deletingAttachmentId: number | null = null;
  attachmentLoading = false;

  hideSuccess() {
    this.showNotification = false;
  }

  async created() {
    const material = await this.materialStore.fetchMaterialById(this.materialId);
    await this.materialStore.fetchAttachmentsByMaterialId(this.materialId);
    if (material) {
      this.materialStore.setCurrentMaterial(material);
      this.material = this.materialStore.currentMaterial;
      this.materialEdit = _.cloneDeep(this.material)
    }
    this.loading = false;
  }

  uploadFiles(fileList: File[]) {
    fileList.forEach((element) => {
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
    return this.material;
  }

  get currentAttachments(): Array<AttachmentModel> {
    return this.materialStore.currentAttachments;
  }

  get isMaterialEmpty(): boolean {
    return this.materialEdit.name.length === 0 || this.materialEdit.content.length === 0;
  }

  get isAttachmentsEqual(): boolean {
    return _.isEqual(this.currentAttachments, this.attachmentsEdit);
  }

  get canChangeMaterial(): boolean {
    return _.isEqual(this.currentMaterial, this.materialEdit) || this.isMaterialEmpty
  }

  showConfirmModal(deletingAttachment: AttachmentModel) {
    this.deletingAttachmentId = deletingAttachment.id;
    this.approvedText = `Удалить вложение: ${deletingAttachment.name}`;
    this.confirmModalTrigger = !this.confirmModalTrigger;
  }

  async ChangeMaterial() {
    await api.patch(`/api/material/${this.materialEdit.id}/`, this.materialEdit)
      .then(() => {
        this.notificationKind = 'success';
        this.notificationText = 'Материалы успешно изменены';
        this.updateMaterials(this.material, this.materialEdit);
        this.material = this.materialEdit;
        this.materialStore.setCurrentMaterial(this.material);
      })
      .catch(error => {
        this.notificationText = `Что-то пошло не так: ${error.message}`;
        this.notificationKind = 'error';
      })
      .finally(() => this.showNotification = true);

    this.attachmentsEdit.forEach(element => {
      this.materialStore.createAttachment(element);
    })
    await this.updateAttachments();
    const input = window.document.getElementById('files_input') as HTMLInputElement
    input.value = '';
    this.attachmentsEdit = [];
  }

  deleteAttachment() {
    if (!this.deletingAttachmentId)
      throw Error;
    this.materialStore.deleteAttachment(this.deletingAttachmentId);
  }

  async updateAttachments() {
    await this.materialStore.fetchAttachmentsByMaterialId(this.materialId);
  }

  async deleteAttachment() {
    if (!this.deletingAttachmentId)
      throw Error;
    await this.materialStore.deleteAttachment(this.deletingAttachmentId)
      .catch(error => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так: ${error.message}`
        this.showNotification = true;
      })
  }

  async updateAttachments() {
    await this.materialStore.fetchAttachmentsByMaterialId(this.materialId);
  }

  async updateMaterials(oldMaterial: MaterialModel, newMaterial: MaterialModel) {
    let materials = await this.materialStore.fetchMaterialsByLessonId(oldMaterial.lesson);
    materials = materials.filter(x => x.id !== oldMaterial.id);
    materials.push(newMaterial);
    materials.sort((a, b) => a.id - b.id);
    this.materialStore.setMaterials({ [newMaterial.lesson]: materials });
  }
}
</script>

<style scoped lang="stylus">
.bx--col-lg-5
  margin-left 20px

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

.edit-container-wrapper
  margin-top 2rem
  margin-bottom 2rem
  min-height 400px

.edit-container
  padding 1rem
  background-color var(--cds-ui-01)

/deep/.bx--text-input
  background-color var(--cds-ui-background)

.text-area >>> .bx--text-area
  background-color var(--cds-ui-background)
  min-height 13rem
  resize none
  margin-bottom 10px

#files_input
  color var(--cds-text-01)

.change__btn
  display flex
  justify-content flex-end

.text-area
  font-size: 14px
  font-family: "Monaco", courier, monospace
  margin-top 15px

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
