<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>Редактирование материала</h1>
    </div>
    <cv-loading v-if="loading"/>
    <div v-else class="bx--row content">
      <div class="edit-container-wrapper bx--col-lg-5">
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
                        style="min-height: 200px"
                        v-model="materialEdit.content">
          </cv-text-area>
          <input type="file" id="files_input" ref="files" multiple  v-on:change="uploadFiles($event.target.files)"/>
          <div class="change__btn">
            <cv-button :disabled="canChangeMaterial"
                       @click="ChangeMaterial">
              Изменить
            </cv-button>
          </div>
        </div>
      </div>
       <div class="preview-container edit-container bx--col-lg-5">
        <h4 class="title" v-if="materialEdit.name.length > 0"> {{ materialEdit.name }} </h4>
        <h4 v-else>Введите название материала</h4>
        <vue-markdown :source="materialEdit.content" html="false" class="markdown"/>
      </div>
    </div>
    <cv-list v-for="element in this.currentAttachments" :key="element.id">
      <cv-list-item>
        <attachments-component-list :attachment="element"></attachments-component-list>
      </cv-list-item>
    </cv-list>
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

@Component({ components: { VueMarkdown, AttachmentsComponentList } })
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

  attachmentsEdit: Array<FormData> = [];
  materialEdit: MaterialModel = { ...this.material }
  showNotification = false;
  notificationKind = 'success';
  notificationText = '';
  loading = true;

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

  uploadFiles(fileList: File[]){
    fileList.forEach((element) =>{
      const fd = new FormData();
      fd.append('id', '-1')
      fd.append('name', element.name)
      fd.append('material', this.material.id.toString())
      fd.append('file_url', element)
      this.attachmentsEdit.push(fd);
    });
  }

  get currentMaterial(): MaterialModel {
    return this.material;
  }

  get currentAttachments(): Array<AttachmentModel>{
    return this.materialStore.currentAttachments;
  }

  get isMaterialEmpty(): boolean {
    return this.materialEdit.name.length === 0 || this.materialEdit.content.length === 0;
  }

  get isAttachmentsEqual(): boolean {
    return _.isEqual(this.currentAttachments, this.attachmentsEdit)
  }

  //toDo fix return
  get canChangeMaterial(): boolean {
    return _.isEqual(this.currentMaterial, this.materialEdit) || this.isMaterialEmpty
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

    this.attachmentsEdit.forEach(element=>{
      this.materialStore.createAttachment(element);
    })
    await this.updateAttachments();
    const input = window.document.getElementById('files_input') as HTMLInputElement
    input.value = '';
    this.attachmentsEdit = [];
  }

  async updateAttachments(){
    await this.materialStore.fetchAttachmentsByMaterialId(this.materialId);
  }

  async updateMaterials(oldMaterial: MaterialModel, newMaterial: MaterialModel) {
    let materials = await this.materialStore.fetchMaterialsByLessonId(oldMaterial.lesson);
    materials = materials.filter(x => x.id !== oldMaterial.id);
    materials.push(newMaterial);
    materials.sort((a,b) => a.id - b.id);
    this.materialStore.setMaterials({ [newMaterial.lesson]: materials });
  }
}
</script>

<style scoped lang="stylus">
.bx--col-lg-5
  margin-left 20px

.preview-container
  border 2px black solid

.markdown
  overflow-wrap break-word
  margin-top 10px
  overflow-y auto
  max-height 30rem

.title
  overflow-wrap break-word

.edit-container-wrapper
  margin-top 2rem
  min-height 400px

.edit-container
  padding 1rem
  background-color var(--cds-ui-background)

.text-area >>> .bx--text-area
  min-height 13rem
  resize none
  margin-bottom 10px

.change__btn
  display flex
  justify-content flex-end

.text-area
  font-size: 14px
  font-family: "Monaco", courier, monospace
  margin-top 15px

code {
  color: #f66;
}

</style>
