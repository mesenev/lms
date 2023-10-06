<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-12">
        <br>
        <h3>Здравствуйте!</h3>
        <h4>
          Пожалуйста, заполните поля ниже, чтобы записаться на курс "{{ }}"
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
          <cv-text-input id="mail" v-model.trim="email" helper-text="" label="Почта">
            <template v-if="checkEmail" id="test_mail" slot="invalid-message">Введите корректный Email</template>
          </cv-text-input>
          <br>
          <cv-text-input v-model.trim="login" id="login" label="Придумайте логин" helper-text="">
            <template v-if="checkLoginAlphabet" slot="invalid-message">Введите корректный логин<br></template>
            <!--Todo: сделать отступ-->
            <template v-if="checkLoginLen" class="test_checkLoginLen" slot="invalid-message">Длина логина должна быть от
              4 до 10 символов
            </template>
          </cv-text-input>
          <br>
          <cv-text-input label="Придумайте пароль" v-model.trim="password" helper-text="">
            <template v-if="checkPasswordLen" slot="invalid-message">Длина пароля должна быть от 8 до 25<p></p>
            </template>
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
        <input type="file" ref="file1" accept="image/*" v-on:change="Upload($event.target.files)"/>
        <label>Предварительный просмотр</label>
        <img v-bind:src="imagePreview" v-show="showPreview" alt="картинка" class="preview"/>
      </div>
    </div>
  </div>
</template>

<!-- TODO: password work w/ backend -->

<script lang="ts" setup>
import api from '@/stores/services/api'
import { ref, type Ref, computed, onMounted } from 'vue';


const showNotification: Ref<boolean> = ref(false);
const notificationText: Ref<string> = ref('');
const modalVisible: Ref<boolean> = ref(false);
const notificationKind: Ref<string> = ref('success');

const first_name: Ref<string> = ref('');
const last_name: Ref<string> = ref('');
const email: Ref<string> = ref('');
const password: Ref<string> = ref('');
const password_repeat: Ref<string> = ref('');
const login: Ref<string> = ref('');
const validField: Ref<boolean> = ref(false);

const file: Ref<Blob> = ref(new Blob());
const imagePreview: Ref<string | null | ArrayBuffer> = ref('');
const showPreview: Ref<boolean> = ref(false);

function Upload(fileList: never) {
  file.value = fileList[0];
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    showPreview.value = true;
    imagePreview.value = reader.result;
  })
  if (file.value) {
    reader.readAsDataURL(file.value);
  }
}

const checkEmail = computed((): boolean => {
  if (email.value) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    const res = !re.test(email.value);
    if (res) {
      validField.value = true;
      return res;
    }
    validField.value = false;
    return res;
  }
  return false;
})

const checkLoginAlphabet = computed((): boolean => {
  if (login.value) {
    const re = /^[a-zA-Z0-9]+$/;
    const res = !re.test(login.value)
    if (res) {
      validField.value = true;
      return res;
    }
    validField.value = false;
    return res;
  }
  return false;
})

const checkLoginLen = computed((): boolean => {
  if (login.value) {
    return login.value.length < 4 || login.value.length > 10;
  }
  return false;
})

const checkPassword = computed((): boolean => {
  return true;
  //TODO: code below is not working
  if (password.value) {
    const re = /(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,20}/g;
    const res = !re.test(password.value);
    if (res) {
      validField.value = true;
      return res;
    }
    validField.value = false;
    return res;
  }
  return false;
})

const checkPasswordLen = computed((): boolean => {
  if (password.value) {
    return password.value.length < 8 || password.value.length > 20;
  }
  return false;
})

const checkRepeatPassword = computed((): boolean => {
  if (password_repeat.value) {
    return password.value !== password_repeat.value;
  }
  return false;
})

const canAction = computed((): boolean => {
  return !(login.value && password.value && first_name.value && last_name.value && email.value && password_repeat.value && !validField.value);
})

function modalHidden() {
  modalVisible.value = false;
}

async function action() {
  const fd = new FormData();
  fd.append('avatar_url', file.value);
  fd.append('email', email.value);
  fd.append('first_name', first_name.value);
  fd.append('last_name', last_name.value);
  fd.append('password', password.value);
  fd.append('username', login.value);
  //const r = axios.post( '/api/users/', fd)
  const request = api.post('/api/users/', fd);
  request.then(() => {
    notificationKind.value = 'success';
    notificationText.value = "Пользователь успешно создан";
    showNotification.value = true;
  })
  request.catch(error => {
    let err = '';
    if (error.response.data.email) {
      err = 'пользователь с такой почтой уже существует';
    }
    if (error.response.data.user) {
      err = 'пользователь с таким логином уже существует';
    }
    notificationKind.value = 'error';
    notificationText.value = `Что-то пошло не так: ${err}`;
    showNotification.value = true;
  })
}

</script>

<style scoped lang="stylus">
.preview
  object-fit: cover;
  width: 250px;
  height: 250px;
  border-radius: 150%;
  margin-top 10px;
  margin-bottom 10px;

img:hover
  transform: scale(1.2);

</style>
