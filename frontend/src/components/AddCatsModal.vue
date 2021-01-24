<template>
  <div>
    <cv-button class="cats-btn" @click="showModal">
      Добавить аккаунт cats
    </cv-button>
    <cv-modal
      :visible="modalVisible"
      class="add_cats_modal" size="default"
      @modal-hidden="modalHidden">
      <template slot="title">
        Добавить аккаунт
      </template>
      <template slot="content">
        <div class="btns">
          <cv-text-input class="input" placeholder="Введите имя аккаунта"/>
          <cv-button class="btn"> Добавить </cv-button>
        </div>
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">

import {Component, Vue} from 'vue-property-decorator';


@Component({ components: { } })

export default class AddCatsModal extends Vue {
  modalVisible = false;

  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
  }
}
</script>

<style scoped lang="stylus">
.btns {
  float left;
  padding: 10px 24px;
  cursor: pointer;
  clear: both;
  display flex;
  flex-direction row;
}



.input {
  width 650px;
  padding-right 20px;
}
</style>
