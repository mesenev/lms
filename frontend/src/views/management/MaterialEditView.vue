<template>
  <div class="bx--grid">
    <div class="bx--row header">
      <h1>Редактирование материала</h1>
    </div>
    <div class="bx--row content">
      <div class="edit-container bx--col-lg-5">
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
        <div class="change__btn">
          <cv-button :disabled="canChangeMaterial"
                     @click="ChangeMaterial">
            Изменить
          </cv-button>
        </div>
      </div>
      <div class="preview-container edit-container bx--col-lg-5">
        <h4 class="title" v-if="materialEdit.name.length > 0"> {{ materialEdit.name }} </h4>
        <h4 v-else>Введите название материала</h4>
        <vue-markdown :source="materialEdit.content" class="markdown"/>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
import MaterialModel from '@/models/MaterialModel';
import materialStore from '@/store/modules/material';
import _ from 'lodash';
import VueMarkdown from 'vue-markdown-render';
import Vue, { VueConstructor } from 'vue';
import { Component, Prop } from 'vue-property-decorator';
import api from '@/store/services/api';

@Component({ components: { VueMarkdown } })
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

  hideSuccess() {
    this.showNotification = false;
  }

  async created() {
    const material = await this.materialStore.fetchMaterialById(this.materialId);
    if (material) {
      this.materialStore.setCurrentMaterial(material);
      this.material = this.materialStore.currentMaterial;
      this.materialEdit = { ...this.material }
    }
  }

  get materials(): MaterialModel {
    return this.material;
  }

  get canChangeMaterialName() {
    return this.materials.name === this.materialEdit.name;
  }

  get isMaterialEmpty(): boolean {
    console.log(this.materialEdit.name.length === 0 || this.materialEdit.content.length === 0);
    return this.materialEdit.name.length === 0 || this.materialEdit.content.length === 0;
  }

  get canChangeMaterial(): boolean {
    return _.isEqual(this.materials, this.materialEdit) || this.isMaterialEmpty;
  }

  ChangeMaterial() {
    const request = api.patch(`/api/material/${this.materialEdit.id}/`, this.materialEdit);
    request.then(() => {
      this.notificationKind = 'success';
      this.notificationText = 'Материалы успешно изменены';
      this.material = this.materialEdit;
    });
    request.catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.notificationKind = 'error';
    })
    request.finally(() => this.showNotification = true);
  }

}
</script>

<style scoped lang="stylus">
.bx--col-lg-5
  margin-left 20px
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.preview-container
  border 2px black solid

.markdown
  overflow-wrap break-word
  margin-top 10px
  overflow-y auto
  height 80%

.title
  overflow-wrap break-word

.edit-container
  margin-top 2rem
  min-height 400px

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
