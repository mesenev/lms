<template>
  <div>
    <cv-modal
      class="confirm--modal"
      :visible="modalVisible"
      :primary-button-disabled="inAction"
      size="small"
      @primary-click="approve"
      @modal-hidden="hideModal">
      <template slot="label">Подтверждение</template>
      <template slot="title">Вы уверены?</template>
      <template slot="content">
        <div>
          {{ text }}
        </div>
      </template>
      <template slot="primary-button">Подтвердить</template>
      <template slot="secondary-button">Отмена</template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Watch, Vue} from "vue-property-decorator";

@Component({})
export default class ConfirmModal extends Vue {
  @Prop({required: true}) modalTrigger!: boolean;
  @Prop({required: true}) text!: string;
  @Prop({required: true}) approveHandler!: Function;

  modalVisible = false;
  inAction = false;

  @Watch('modalTrigger')
  showModal() {
    this.modalVisible = true;
  }

  hideModal() {
    this.modalVisible = false;
    this.sideModalAction();
  }

  sideModalAction() {
    this.$emit('show-modal');
  }

  async approve() {
    this.inAction = true;
    await this.approveHandler();
    this.inAction = false;
    this.hideModal();
  }
}
</script>

<style scoped>

</style>
