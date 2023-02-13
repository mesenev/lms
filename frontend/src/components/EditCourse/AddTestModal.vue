<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить тест
    </cv-button>
    <cv-modal
      size="large"
      class="add-test-modal"
      :visible="modalVisible"
      @modal-hidden="modalHidden"
    >
      <template slot="title">Создание теста</template>
      <template slot="content">
        <div :class="expanded ? 'expand-container expanded' : 'expand-container'">
          <div @click="expand" class="expand-container-head">
            <p>Настройки теста</p>
            <component class="expand-btn" :is="chevronDown"/>
          </div>
          <div class="expand-fields">
            <cv-text-input label="Название теста"/>
            <cv-text-input label="Описание"/>
            <cv-dropdown label="Способ тестирования" placeholder="Выберите способ тестирования">
              <cv-dropdown-item value="1">Auto</cv-dropdown-item>
              <cv-dropdown-item value="2">Manual</cv-dropdown-item>
              <cv-dropdown-item value="3">Auto & Manual</cv-dropdown-item>
            </cv-dropdown>
            <cv-date-picker kind="single" date-label="Дедлайн"/>
          </div>
        </div>
        <test-question-component/>
        <test-question-component/>
        <div class="action-container">
          <div class="action-btns">
            <component class="action-btn" :is="addAlt"/>
            <component class="action-btn" :is="image"/>
            <component class="action-btn" :is="videoAdd"/>
            <component class="action-btn" :is="attachment"/>
          </div>
        </div>
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import { Component } from "vue-property-decorator";
import chevronUp from "@carbon/icons-vue/lib/chevron--up/16"
import chevronDown from "@carbon/icons-vue/lib/chevron--down/16"
import image from "@carbon/icons-vue/lib/image/24"
import addAlt from "@carbon/icons-vue/lib/add--alt/24"
import videoAdd from "@carbon/icons-vue/lib/video--add/24"
import attachment from "@carbon/icons-vue/lib/attachment/24"

import TestQuestionComponent from "@/components/TestQuestionComponent.vue";

@Component({
  components: {
    chevronUp,
    chevronDown,
    addAlt,
    videoAdd,
    image,
    attachment,
    TestQuestionComponent
  }
})
export default class AddTestModal extends NotificationMixinComponent {

  modalVisible = false;

  chevronDown = chevronDown;
  image = image;
  addAlt = addAlt;
  videoAdd = videoAdd;
  attachment = attachment;

  expanded = false;

  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
  }

  expand() {
    console.log(this.expanded);
    this.expanded = !this.expanded;
  }
}
</script>

<style scoped lang="stylus">
/deep/ .bx--modal-container
  background var(--cds-ui-02)

.expand-container-head
  cursor pointer
  display flex
  align-items center
  justify-content space-between
  margin-bottom 1rem

.expand-container
  max-height 3.25rem
  overflow hidden
  transition all .3s ease
  background var(--cds-ui-01)
  padding 1rem

.expand-container.expanded
  max-height 500px

/deep/ .bx--list-box__field
  display flex

.action-container
  display flex
  justify-content end

.expand-fields
  display flex
  flex-direction column
  gap 1rem

.action-btns
  background var(--cds-ui-01)
  display flex
  gap 1rem
  border-radius 5px
  margin-top 1rem
  padding 1rem

.action-btn
  cursor pointer
  transition ease-in-out 0.1s

.action-btn:active
  transform scale(0.9)

</style>
