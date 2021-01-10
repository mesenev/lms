<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить материал
    </cv-button>
    <cv-modal size="default"
              class="add_lesson_modal"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              :primary-button-disabled="!materials.length && !currentMaterial.name"
              @primary-click="addMaterial"
              @secondary-click="() => {}">
      <template slot="label">{{ lesson.name }}</template>
      <cv-inline-notification
        v-if="showNotification"
        @close="() => showNotification=false"
        kind="error"
        :sub-title="notificationText"
      />
      <template slot="title">
        Добавить материалы
        <cv-content-switcher class="switcher" @selected="actionSelected">
          <cv-content-switcher-button content-selector=".content-1" selected>
            Создать новый
          </cv-content-switcher-button>
          <cv-content-switcher-button content-selector=".content-2">
            Выбрать из существующих
          </cv-content-switcher-button>
        </cv-content-switcher>
      </template>
      <template slot="content">
        <section class="modal--content">
          <div class="content-1">
            <cv-text-input label="Название материала" v-model.trim="material.name" disabled/>
            <cv-text-input label="Название" v-model.trim="currentMaterial.name"/>
            <span>Редактирование материалов доступно после создания</span>

          </div>
          <div class="content-2" hidden>
            <div>
              <cv-structured-list>
                <template slot="items">
                  <cv-search v-model="searchQueryForAllMaterials"></cv-search>
                  <cv-structured-list-item
                    class="problem-card"
                    v-for="material in allMaterials"
                    :key="material.id">
                  </cv-structured-list-item>
                </template>
              </cv-structured-list>
            </div>
          </div>
        </section>
      </template>
      <template slot="primary-button">
        Добавить
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import searchByMaterials from '@/common/searchByMaterials';
import LessonModel from '@/models/LessonModel';
import { lessonStore, materialStore } from '@/store';
import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';
import axios from 'axios';
import { Component, Prop, Vue } from 'vue-property-decorator';
import ProblemCard from "@/components/EditLesson/ProblemCard.vue";
import LessonContent from "@/models/LessonContent";


@Component({ components: {ProblemCard, AddAlt20, SubtractAlt20 } })
export default class EditLessonMaterialsModal extends Vue {
  @Prop({ required: true }) lesson!: LessonModel;
  AddAlt32 = AddAlt20;
  SubtractAlt32 = SubtractAlt20;
  materialStore = materialStore;
  currentMaterial: LessonContent = { ...this.materialStore.getNewMaterial, lesson: this.lesson.id};
  fetchingMaterials = true;
  selectedNew = true;
  showNotification = false;
  notificationText = '';
  creationLoader = false;
  materials: LessonContent[] = [];
  modalVisible = false;
  searchQueryForAllMaterials = '';
  get allMaterials(): LessonContent[] {
    return searchByMaterials(this.searchQueryForAllMaterials, this.freeMaterials);
  }
  get freeMaterials(): LessonContent[] {
    return this.materialStore.materials.filter((l) => {
      return !this.lesson.materials.map((lessonMaterial) => lessonMaterial.id).includes(l.id);
    });
  }
  async created() {
    if (this.materialStore.materials.length === 0)
      await this.materialStore.fetchMaterials();
    this.fetchingMaterials = false;
  }
  showModal() {
    this.modalVisible = true;
    this.showNotification = false;
    this.currentMaterial = { ...this.materialStore.getNewMaterial, lesson: this.lesson.id };
  }
  modalHidden() {
    this.modalVisible = false;
  }
  actionSelected() {
    this.selectedNew = !this.selectedNew;
  }
  get getSelected(): string {
    return this.materials.concat(this.currentMaterial)
      .map((l) => l.name)
      .sort((a, b) => a < b ? -1 : 1)
      .join(' ');
  }
  chooseMaterial(material: LessonContent) {
    if (!this.materials.includes(material)) {
      this.materials.push(material);
    } else {
      this.materials = this.materials.filter((l) => materials !== l); //!
    }
  }
  async addMaterial() {
    if (this.selectedNew) {
      this.creationLoader = true;
      await this.createNewMaterial();
      this.creationLoader = false;
    }
    if (this.materials.every((l) => l.name)) {
      // this.lessons.forEach((lesson) => this.lessonStore.addLessonToCourse(lesson));
      // this.lessons = [];
    }
  }
  async createNewMaterial() {
    delete this.currentMaterial.id;
    const request = axios.post('http://localhost:8000/api/material/', this.currentMaterial);
    request.then(response => {
      this.lesson.materials.push(response.data as LessonContent);
      this.modalHidden();
    });
    request.catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.showNotification = true;
    });
  }
}
</script>

<style scoped lang="stylus">
.bx--modal-content:focus
  outline none
.change-btn
  background-color var(--cds-interactive-02)
  margin-left 25px
.lesson_list
  margin-bottom 0
.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)
.switcher
  margin-bottom: 5px
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
