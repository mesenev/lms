<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Материалы
    </cv-button>
    <confirm-modal :modal-trigger="confirmModalTrigger"
                   :text="approvedText"
                   :approve-handler="deleteMaterial"
                   @show-modal="showModal"/>
    <cv-modal size="default"
              class="add_lesson_modal"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              :primary-button-disabled="isButtonDisabled"
              @primary-click="addMaterial"
              @secondary-click="() => {}">
      <template slot="label">{{ lesson.name }}</template>
      <template slot="title">
        Добавить материалы
      </template>
      <template slot="content">
        <section class="modal--content">
          <cv-text-input label="Название"
                         @focus="invalidMessageHidden"
                         v-model.trim="currentMaterial.name">
            <template v-if="invalidMessageVisible" slot="invalid-message">
              {{ invalidMessage }}
            </template>
          </cv-text-input>
          <h5>Выберите тип материала:</h5>
          <cv-radio-group :vertical=false>
            <cv-radio-button v-model="currentMaterial.content_type" label="Текст" value="text"/>
            <cv-radio-button v-model="currentMaterial.content_type" label="Ссылка" value="url"/>
            <cv-radio-button v-model="currentMaterial.content_type" label="Видео" value="video"/>
          </cv-radio-group>
          <br>
          <h5 class="materials-title">Материалы урока:</h5>
          <cv-inline-notification
            v-if="showNotification"
            @close="() => showNotification=false"
            kind="error"
            :sub-title="notificationText"
          />
          <div class="materials-list-container" v-if="materials.length">
            <cv-structured-list class="materials-list">
              <template slot="items">
                <cv-structured-list-item
                  v-for="material in materials"
                  :key="material.id"
                >
                  <material-list-component :material-prop="material"
                                           :is-editing="true"
                                           @show-confirm-modal="showConfirmModal($event)"/>
                </cv-structured-list-item>
              </template>
            </cv-structured-list>
          </div>
          <p v-else class="empty-materials-list-title">
            Список материалов пуст
          </p>
        </section>
      </template>
      <template slot="primary-button">
        Добавить материал
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import MaterialListComponent from '@/components/lists/MaterialListComponent.vue';
import LessonModel from '@/models/LessonModel';
import MaterialModel from '@/models/MaterialModel';
import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';
import api from '@/store/services/api'
import {Component, Prop, Vue} from 'vue-property-decorator';
import materialStore from '@/store/modules/material';
import ConfirmModal from "@/components/ConfirmModal.vue";
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";

@Component({components: {AddAlt20, SubtractAlt20, MaterialListComponent, ConfirmModal}})
export default class EditLessonMaterialsModal extends NotificationMixinComponent {
  @Prop({required: true}) lesson!: LessonModel;
  AddAlt32 = AddAlt20;
  SubtractAlt32 = SubtractAlt20;
  materialStore = materialStore;
  currentMaterial: MaterialModel = {...this.materialStore.getNewMaterial, lesson: this.lesson.id};
  creationLoader = false;
  material: Array<MaterialModel> = [];
  modalVisible = false;
  searchQueryForAllMaterials = '';
  invalidMessageVisible = false;
  invalidMessage = '';
  deletingMaterialId: number | null = null;
  approvedText = '';
  confirmModalTrigger = false;

  showModal() {
    this.modalVisible = true;
    this.currentMaterial = {...this.materialStore.getNewMaterial, lesson: this.lesson.id};
  }

  modalHidden() {
    this.modalVisible = false;
  }

  invalidMessageHidden() {
    this.invalidMessageVisible = false;
  }

  showConfirmModal(deletingMaterial: MaterialModel) {
    this.deletingMaterialId = deletingMaterial.id;
    this.approvedText = `Удалить материал: ${deletingMaterial.name}`;
    this.modalHidden();
    this.confirmModalTrigger = !this.confirmModalTrigger;
  }

  async addMaterial() {
    if (this.areSameMaterialNames(this.currentMaterial.name)) {
      this.creationLoader = true;
      await this.createNewMaterial();
      this.creationLoader = false;
    } else {
      this.invalidMessage = 'Материал с таким названием уже существует!';
      this.invalidMessageVisible = true;
    }
    if (this.materials.every((l) => l.name)) {
      // this.lessons.forEach((lesson) => this.lessonStore.addLessonToCourse(lesson));
      // this.lessons = [];
    }
  }

  async createNewMaterial() {
    this.currentMaterial.content = "### материал"
    const request = api.post('/api/material/', this.currentMaterial);
    request.then(response => {
      this.lesson.materials.push(response.data as MaterialModel);
      this.materialStore.setMaterials({[this.lesson.id]: this.lesson.materials});
    });
    request.catch(error => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    });
  }

  async deleteMaterial() {
    if (!this.deletingMaterialId)
      throw Error;
    await api.delete(`/api/material/${this.deletingMaterialId}/`)
      .then(() => {
        this.lesson.materials = this.lesson.materials.filter(x => x.id != this.deletingMaterialId);
        this.materialStore.setMaterials({[this.lesson.id]: this.lesson.materials});
      })
      .catch(error => {
        this.notificationKind = 'error';
        this.notificationText = `Что-то пошло не так: ${error.message}`;
        this.showNotification = true;
      }).finally(() => {
        this.showModal();
        this.$emit('update-material-delete');
      })
  }

  get isButtonDisabled() {
    return this.creationLoader || !this.currentMaterial.name
  }

  areSameMaterialNames(materialName: string) {
    return this.materials.filter(material => material.name === materialName).length === 0;
  }

  get materials(): Array<MaterialModel> {
    if (this.lesson)
      return this.materialStore._materials[this.lesson.id].sort(
        (a, b) => {
          return (a.is_teacher_only === b.is_teacher_only ? 0 : b.is_teacher_only ? -1 : 1) || a.id - b.id;
        }
      );
    return [];
  }
}
</script>

<style scoped lang="stylus">

.bx--modal-content:focus
  outline none

.change-btn
  background-color var(--cds-interactive-02)
  margin-left 25px

.materials-title
  margin-bottom 0.5rem

.materials-list-container
  overflow-y auto
  max-height 15rem

.materials-list
  margin-bottom 0

.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)

.add_lesson_modal .bx--modal-container
  height 75vh

.add_lesson_modal .bx--modal-footer
  height 3.5rem

.add_lesson_modal .bx--btn
  height 3rem
  border none

.add_lesson_modal .bx--btn--secondary
  background-color var(--cds-hover-secondary)

  &:hover, &:active, &:focus
    outline none
    box-shadow none
    border none

.add_lesson_modal .bx--btn--primary[disabled = disabled],
.add_lesson_modal .bx--btn--primary
  background-color var(--cds-ui-05)

.modal--content
  height 400px
</style>
