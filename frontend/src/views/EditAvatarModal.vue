<template>
  <div>
    <cv-button class="change-btn" @click="showModal"/>
    <cv-modal size="default"
              class="add_lesson_modal"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              :primary-button-disabled="!avatarChanged"
              @primary-click="changeAvatar">
      <template slot="label">Изменить аватар</template>
    </cv-modal>
  </div>
</template>

<script lang="ts">

import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';
import { Component, Vue } from 'vue-property-decorator';

@Component({ components: { AddAlt20, SubtractAlt20 } })
export default class EditAvatarModal extends Vue {

  AddAlt32 = AddAlt20;
  SubtractAlt32 = SubtractAlt20;
  avatarChanged = false;
  modalVisible = false;

  showModal() {
    this.modalVisible = true;

  }

  modalHidden() {
    this.modalVisible = false;
    this.avatarChanged = false;
  }

  changeAvatar() {
    return;
  }
}
</script>

<style scoped lang="stylus">
.bx--modal-content:focus
  outline none

.change-btn
  background-color var(--cds-interactive-02)

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
