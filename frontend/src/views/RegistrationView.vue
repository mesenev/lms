<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-12">
        <br>
        <h3>Здравствуйте!</h3>
        <h4>
          Пожалуйста, заполните поля ниже, чтобы записаться на курс "{{  }}"
        </h4>
        <br>
        <cv-inline-notification
        v-if="showNotification"
        @close="() => showNotification=false"
        :kind="notificationKind"
        :sub-title="notificationText"
        />
      </div>
      <div class="bx--col-lg-7">
        <cv-form @submit.prevent="action">
          <cv-text-input v-model="first_name" id="name" label="Имя" helper-text=""/>
          <br>
          <cv-text-input v-model="last_name" id="surname" label="Фамилия" helper-text=""/>
          <br>
          <cv-text-input id="group" label="Группа обучения" helper-text=""/>
          <br>
          <cv-text-input v-model.trim="email"
                         id="mail"
                         label="Почта"
                         helper-text=""
          >
            <template v-if="checkEmail" slot="invalid-message">Введите корректный Email</template>
          </cv-text-input>
          <br>
          <cv-text-input v-model.trim="login" id="login" label="Придумайте логин" helper-text="">
            <template v-if="checkLoginAlphabet" slot="invalid-message">Введите корректный логин<br></template>
            <!--Todo: сделать отступ-->
            <template v-if="checkLoginLen" slot="invalid-message">Длина логина должна быть от 4 до 10 символов</template>
          </cv-text-input>
          <br>
          <cv-text-input label="Придумайте пароль" v-model.trim="password" helper-text="">
            <template v-if="checkPasswordLen" slot="invalid-message">Длина пароля должна быть от 8 до 25<p></p></template>
            <template v-if="checkPassword" slot="invalid-message">Некоректный пароль</template>
          </cv-text-input>

          <br>
          <cv-text-input label="Подтверждение пароля" helper-text="" v-model.trim="password_repeat">
            <template v-if="checkRepeatPassword" slot="invalid-message">Пароли должны совпадать</template>
          </cv-text-input>
          <br>
          <cv-button :disabled="canAction" kind="secondary">Отправить</cv-button>
        </cv-form>
      </div>
      <div class="bx--col-lg-9">
        <!-- TODO:  avatar component + storage add -->
        <cv-file-uploader
          accept="image/jpg,image/png"
          clear-on-reselect
          initial-state-uploading
          multiple
          removable
          label="Загрузите аватарку"/>
        <label>
          <TextArea cols="50" placeHolder="О себе" rows="5"> </TextArea>
        </label>
      </div>
    </div>
  </div>
</template>

<!-- TODO: password work w/ backend -->

<script lang="ts">
import Registration from '@/components/Registration.vue';
import Vue from 'vue';
import Component from 'vue-class-component';
import axios from "axios";
import UserModel from "@/models/UserModel";

@Component({ components: { Registration } })
export default class RegistrationView extends Vue {
  showNotification = false;
  notificationText = '';
  modalVisible = false;
  notificationKind = 'success';

  first_name = '';
  last_name = '';
  email = '';
  password = '';
  password_repeat = '';
  login = '';
  validField = false;

  user = {
    username: this.login,
    first_name: this.first_name,
    last_name:this.last_name,
    email: this.email,
    password: this.password,
  }

  get checkEmail(): boolean {
    if (this.email) {
      const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      const res =  !re.test(this.email);
      if (res) {
        this.validField = true;
        return res;
      }
      this.validField = false;
      return res;
    }
    return false;
  }

  get checkLoginAlphabet(): boolean{
    if (this.login) {
      const re = /^[a-zA-Z0-9]+$/;
      const res = !re.test(this.login)
      if (res) {
        this.validField = true;
        return res;
      }
      this.validField = false;
      return res;
    }
    return false;
  }

  get checkLoginLen(): boolean{
    if (this.login) {
      return this.login.length < 4 || this.login.length > 10;
    }
    return false;
  }

  get checkPassword(): boolean {
    if (this.password) {
      const re  = /(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,20}/g;
      const res =  !re.test(this.password);
      if (res) {
        this.validField = true;
        return res;
      }
      this.validField = false;
      return res;
    }
    return false;
  }

  get checkPasswordLen(): boolean {
    if (this.password){
      return this.password.length < 8 || this.password.length > 20;
    }
    return false;
  }

  get checkRepeatPassword(): boolean {
    if (this.password_repeat) {
      return this.password !== this.password_repeat;
    }
    return false;
  }

  get canAction(): boolean {
    return !(this.login && this.password && this.first_name && this.last_name && this.email && this.password_repeat && !this.validField);

  }
  modalHidden() {
    this.modalVisible = false;
  }

  async action() {
    this.user = { email: this.email, first_name: this.first_name, last_name: this.last_name, password: this.password, username: this.login }
    const request = axios.post('http://localhost:8000/api/users/',this.user);
    request.then(response => {
      this.notificationKind = 'success';
      this.notificationText = "Пользователь успешно создан";
      this.showNotification = true;
    })
    request.catch(error => {
      console.log(error.response);
      let err = '';
      if (error.response.data.email) {
        err = 'пользователь с такой почтой уже существует';
      }
      if ( error.response.data.user) {
        err = 'пользователь с таким логином уже существует';
      }
      this.notificationKind = 'error';
      this.notificationText = `Что-то пошло не так: ${ err }`;
      this.showNotification = true;
    })
  }

}

</script>

<style scoped lang="stylus">

</style>
