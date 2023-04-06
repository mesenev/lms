<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Материалы
    </cv-button>
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
          <div class="materials-header">
            <cv-text-input label="Название материала"
                           @focus="invalidMessageHidden"
                           v-model.trim="currentMaterial.name">
              <template v-if="invalidMessageVisible && !currentMaterial.name"
                        slot="invalid-message">
                {{ emptyInvalidMessage }}
              </template>
              <template v-if="invalidMessageVisible && areSameMaterialNames(currentMaterial.name)"
                        slot="invalid-message">
                {{ invalidMessage }}
              </template>
            </cv-text-input>
            <cv-dropdown class="material-type-dropdown"
                         placeholder="Выберите тип"
                         label="Тип материала"
                         v-model="currentMaterial.content_type">
              <cv-dropdown-item value="text">Текст</cv-dropdown-item>
              <cv-dropdown-item value="url">Ссылка</cv-dropdown-item>
              <cv-dropdown-item value="video">Видео</cv-dropdown-item>
              <template slot="invalid-message"
                        v-if="invalidMessageVisible && !currentMaterial.content_type">
                {{ emptyInvalidMessage }}
              </template>
            </cv-dropdown>
          </div>
          <br>
          <p class="materials-info"> Добавление содержимого в материал доступно после создания. </p>
          <h5 class="materials-title" v-if="materials.length">Материалы урока:</h5>
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
                                           @modal-hidden="modalHidden"/>
                </cv-structured-list-item>
              </template>
            </cv-structured-list>
          </div>
          <empty-list-component v-else
                                class="empty-list"
                                :text="emptyMaterialsListText"
                                list-of="materials"/>
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
import { Component, Prop } from 'vue-property-decorator';
import materialStore from '@/store/modules/material';
import ConfirmModal from "@/components/ConfirmModal.vue";
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import EmptyListComponent from "@/components/EmptyListComponent.vue";

@Component({
  components: {
    EmptyListComponent,
    AddAlt20,
    SubtractAlt20,
    MaterialListComponent,
    ConfirmModal
  }
})
export default class EditLessonMaterialsModal extends NotificationMixinComponent {
  @Prop({ required: true }) lesson!: LessonModel;
  AddAlt32 = AddAlt20;
  SubtractAlt32 = SubtractAlt20;
  materialStore = materialStore;
  currentMaterial: MaterialModel = { ...this.materialStore.getNewMaterial, lesson: this.lesson.id };
  creationLoader = false;
  material: Array<MaterialModel> = [];
  modalVisible = false;
  searchQueryForAllMaterials = '';
  invalidMessageVisible = false;
  invalidMessage = 'Материал с таким названием уже существует!';
  emptyInvalidMessage = 'Заполните поле!';
  emptyMaterialsListText = 'Добавьте новый материал.';

  showModal() {
    this.modalVisible = true;
    this.currentMaterial = { ...this.materialStore.getNewMaterial, lesson: this.lesson.id };
  }

  modalHidden() {
    this.modalVisible = false;
  }

  invalidMessageHidden() {
    if (this.areSameMaterialNames(this.currentMaterial.name))
      this.invalidMessageVisible = false;
  }

  async addMaterial() {
    if (this.areSameMaterialNames(this.currentMaterial.name)
      || !this.currentMaterial.name
      || !this.currentMaterial.content_type) {
      this.invalidMessageVisible = true;
      return;
    }
    this.creationLoader = true;
    await this.createNewMaterial();
    this.creationLoader = false;
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
      this.materialStore.setMaterials({ [this.lesson.id]: this.lesson.materials });
    });
    request.catch(error => {
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    });
    request.finally(() => {
      this.invalidMessageHidden();
    })
  }

  get isButtonDisabled() {
    return this.creationLoader;
  }

  areSameMaterialNames(materialName: string) {
    return this.materials.filter(material => material.name === materialName).length != 0;
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

  &:hover
    border var(--cds-ui-01) 1px solid

.materials-header
  display flex
  gap 1rem
  justify-content space-between

.cv-text-input
  /deep/ .bx--label
    margin-top 3px

.material-type-dropdown
  max-width 10rem

  /deep/ .bx--dropdown__wrapper.bx--list-box__wrapper
    align-self end

/deep/ .bx--list-box__field
  display flex

.materials-info
  margin-bottom 1rem
  text-decoration-line underline

.materials-title
  margin-bottom 0.5rem

.materials-list-container
  overflow-y auto
  max-height 15rem

.materials-list
  margin-bottom 0

.empty-list
  text-align center

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
