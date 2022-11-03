<template>
  <div>
    <cv-modal
      class="confirm--modal"
      :visible="modalVisible"
      size="small"
      @primary-click="doSomething"
      @modal-hidden="hideModal">
      <template slot="label">Подтверждение</template>
      <template slot="title">Вы уверены?</template>
      <template slot="content">
        <div>
          {{ approvedText }}
        </div>
      </template>
      <template slot="primary-button">Подтвердить</template>
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
  @Prop({required: true}) approvedText!: string;
  @Prop({required: true}) elementId!: number
  @Prop({required: true}) someFunction!: Function;

  modalVisible = false;


  @Watch('modalTrigger')
  showModal() {
    this.modalVisible = true;
  }

  hideModal() {
    this.modalVisible = false;
  }

  async doSomething() {
    await this.someFunction(this.elementId);
    this.hideModal();
  }
}
</script>

<style scoped>

</style>
