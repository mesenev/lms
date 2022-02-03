<template>
  <div class="bx--grid main">
    <div class="bx--row">
      <div class="bx--col-lg-6 login-form">
        <cv-form>
          <h3 class="form-header">{{username}} - {{password}} </h3>
          <cv-text-input
            v-model="username"
            class="log-form"
            label="Логин"
            placeholder="Введите свой логин"
            >
          </cv-text-input>
          <cv-text-input
            v-model="password"
            class="pass-form"
            label="Пароль"
            placeholder="Введите свой пароль">
          </cv-text-input>
          <div class="submit-btn" @click="LogIn">
            <cv-button>Войти</cv-button>
          </div>
        </cv-form>
      </div>
    </div>
  </div>
</template>

<script>
import Component from "vue-class-component";
import Vue from "vue";
import axios from "axios";


@Component({ components: {} })
export default class LoginView extends Vue {
  username = "";
  password = "";

  LogIn(){
    debugger
    axios.post(`/api/login/`)
    .then(response => { console.log(response);
      this.$router.push({
          path:('/')
        })
    })
      .catch(error => {
        console.log(error.response);

      })
  }
}

</script>

<style lang="stylus" scoped>

.submit-btn
  display flex
  flex-direction row
  justify-content center

.form-header
  padding-bottom 2rem

.log-form
  padding-bottom 2rem

.pass-form
  padding-bottom 2rem

.main
  margin-left 5rem
  padding 5rem

.login-form
  padding 3rem
  background-color var(--cds-ui-background)


</style>
