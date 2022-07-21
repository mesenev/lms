<template>
  <div>
    <cv-button class="cats-btn" @click="showModal">
      Добавить аккаунт cats
    </cv-button>
    <cv-modal
      :visible="modalVisible"
      class="add_cats_modal" size="small"
      @modal-hidden="modalHidden">
      <template slot="title">
        Добавить аккаунт
      </template>
      <template slot="content">
        <div>
          <cv-text-input class="input"
                         label="Введите логин cats:"
                         v-model.trim="catsLogin"
          />
          <cv-text-input class="input"
                         type="password"
                         label="Введите пароль cats:"
                         v-model.trim="catsPassword"
                         invalid-message="Пароли не сохраняются!"
          />
          <cv-text-input class="input"
                         type="password"
                         label="Повторите пароль:"
                         v-model.trim="catsPasswordRepeat"
                         invalid-message="Пароли не сохраняются!"
          />
        </div>
        <div class="btns">
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
  catsLogin = '';
  catsPassword = '';
  catsPasswordRepeat = '';

  showModal() {
    this.modalVisible = true;
  }

  modalHidden() {
    this.modalVisible = false;
  }
}
</script>

<style scoped lang="stylus">
.add_cats_modal /deep/ .bx--modal-container {
  width: 25%;
}

.btns {
  float left;
  cursor: pointer;
  clear: both;
  display flex;
  flex-direction row;
}

.input {
  width 300px;
  padding-bottom 24px;
}
</style>
