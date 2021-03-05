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
            <template v-if="checkEmail" id="test_mail" slot="invalid-message">Введите корректный Email</template>
          </cv-text-input>
          <br>
          <cv-text-input v-model.trim="login" id="login" label="Придумайте логин" helper-text="">
            <template v-if="checkLoginAlphabet" slot="invalid-message">Введите корректный логин<br></template>
            <!--Todo: сделать отступ-->
            <template v-if="checkLoginLen" class="test_checkLoginLen" slot="invalid-message">Длина логина должна быть от 4 до 10 символов</template>
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
      <div class="bx--col-lg-5">
        <!-- TODO:  avatar component + storage add -->
        <label>
          <TextArea cols="50" placeHolder="О себе" rows="5"> </TextArea>
        </label>
      </div>
      <div class="bx--col-lg-4">
        <input type="file" ref="file1"  accept="image/*" v-on:change="Upload($event.target.files)"/>
        <label>Предварительный просмотр</label>
        <img v-bind:src="imagePreview" v-show="showPreview" alt="картинка" class="preview"/>
      </div>
    </div>
  </div>
</template>

<!-- TODO: password work w/ backend -->

<script lang="ts">
import Registration from '@/components/Registration.vue';
import axios from "axios";
import Vue from 'vue';
import Component from 'vue-class-component';

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

  file = new Blob();
  imagePreview: string|null|ArrayBuffer = '';
  showPreview= false;

  Upload(fileList: never) {
    this.file = fileList[0] ;
    const reader = new FileReader();
    reader.addEventListener("load",  () => {
      this.showPreview = true;
      this.imagePreview = reader.result;
    })
    if (this.file) {
      reader.readAsDataURL( this.file );
    }
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
    return true;
    //TODO: code below is not working
    if (this.password) {
      const re = /(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,20}/g;
      const res = !re.test(this.password);
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
    const fd = new FormData();
    fd.append('avatar_url',this.file );
    fd.append('email', this.email);
    fd.append('first_name', this.first_name);
    fd.append('last_name', this.last_name);
    fd.append('password', this.password);
    fd.append('username', this.login);
    //const r = axios.post( 'http://localhost:8000/api/users/', fd)
    const request = axios.post('http://localhost:8000/api/users/',fd);
    request.then(() => {
      this.notificationKind = 'success';
      this.notificationText = "Пользователь успешно создан";
      this.showNotification = true;
    })
    request.catch(error => {
      let err = '';
      if (error.response.data.email) {
        err = 'пользователь с такой почтой уже существует';
      }
      if (error.response.data.user) {
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
.preview
  object-fit:cover;
  width:250px;
  height:250px;
  border-radius: 150%;
  margin-top 10px;
  margin-bottom 10px;

img:hover
  transform: scale(1.2);

</style>
