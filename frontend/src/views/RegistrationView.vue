<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-12">
        <br>
        <h3> Здравствуйте! </h3>
        <h4> Пожалуйста, заполните поля ниже, чтобы записаться на курс "{{ courseArray.name }}"
        </h4>
        <br>
      </div>
      <div class="bx--col-lg-7">
        <cv-form @submit.prevent="">
          <cv-text-input id="name"
                         label="Ф.И.О."
                         helper-text="">
          </cv-text-input>
          <br>
          <cv-text-input id="group"
                         label="Группа обучения"
                         helper-text="">
          </cv-text-input>
          <br>
          <cv-text-input id="mail"
                         label="Почта"
                         helper-text="">
          </cv-text-input>
          <br>
          <cv-text-input id="login"
                         label="Придумайте логин"
                         helper-text="">
          </cv-text-input>
          <br>
          <cv-text-input
            label="Придумайте пароль"
            helper-text="">
          </cv-text-input>
          <br>
          <cv-text-input
            label="Подтверждение пароля"
            helper-text="">
          </cv-text-input>
          <br>
          <cv-button kind="secondary">Отправить</cv-button>
        </cv-form>
      </div>
      <div class="bx--col-lg-9">
        <!-- TODO:  avatar component + mainStorage adding -->
        <cv-file-uploader
          accept="image/jpg,image/png"
          clear-on-reselect
          initial-state-uploading
          multiple
          removable
          label="Загрузите аватарку">
        </cv-file-uploader>
        <label>
          <TextArea
            cols="50"
            placeHolder="О себе"
            rows="5">
          </TextArea>
        </label>
      </div>
    </div>
  </div>
</template>

<!-- TODO: password work w/ backend -->

<script lang="ts">
import Registration from '@/components/Registration.vue';
import { modBStore } from '@/store';
import Vue from 'vue';
import Component from 'vue-class-component';

@Component({ components: { Registration } })
export default class RegistrationView extends Vue {

  private store = modBStore;

  courseArray = this.store.getCourse;
}

</script>

<style scoped lang="stylus">

</style>
