<template>
  <div>
    <cv-modal
      class="confirm--modal"
      :visible="modalVisible"
      size="small"
      @primary-click="deleteSomething"
      @modal-hidden="hideModal">
      <template slot="label">Подтверждение</template>
      <template slot="title">Вы уверены?</template>
      <template slot="content">
        <div v-if="isProblem">
          Удалить задачу: {{ deletingObject.name }}?
        </div>
        <div v-else>
          Удалить урок: {{ deletingObject.name }}?
        </div>
      </template>
      <template slot="primary-button">Удалить</template>
      <template slot="secondary-button">Отмена</template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";
import ProblemModel from "@/models/ProblemModel";
import LessonModel from "@/models/LessonModel";

@Component({})
export default class ConfirmModal extends Vue{
  @Prop({required: true}) modalTrigger!: boolean;
  @Prop({required: false}) isProblem!: false | boolean;
  @Prop({required: true}) deletingObject!: ProblemModel | LessonModel;
  @Prop({required: true}) deleteMethod!: Function;

  modalVisible = false;


  @Watch('modalTrigger')
  showModal() {
    this.modalVisible = true;
  }

  hideModal() {
    this.modalVisible = false;
  }

  async deleteSomething() {
    await this.deleteMethod();
    this.hideModal();
  }
}
</script>

<style scoped>

</style>
