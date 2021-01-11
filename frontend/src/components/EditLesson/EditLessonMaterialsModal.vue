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
      </template>
      <template slot="content">
        <section class="modal--content">
          <cv-text-input label="Название" v-model.trim="currentMaterial.name"/>
          <h5>Выберите тип материала:</h5>
          <cv-radio-group :vertical=false>
            <cv-radio-button v-model="currentMaterial.content_type" label="Текст" value="text"/>
            <cv-radio-button v-model="currentMaterial.content_type" label="Ссылка" value="url"/>
            <cv-radio-button v-model="currentMaterial.content_type" label="Видео" value="video"/>
          </cv-radio-group>
          <br>
          <span>Редактирование материалов доступно после создания</span>
        </section>
      </template>
      <template slot="primary-button">
        Добавить
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import LessonModel from '@/models/LessonModel';
import { materialStore } from '@/store';
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
  selectedNew = true;
  showNotification = false;
  notificationText = '';
  creationLoader = false;
  materials: LessonContent[] = [];
  modalVisible = false;
  searchQueryForAllMaterials = '';


  showModal() {
    this.modalVisible = true;
    this.showNotification = false;
    this.currentMaterial = { ...this.materialStore.getNewMaterial, lesson: this.lesson.id };
  }

  modalHidden() {
    this.modalVisible = false;
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
    console.log(this.currentMaterial);
    this.currentMaterial.content = "### материал"
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
