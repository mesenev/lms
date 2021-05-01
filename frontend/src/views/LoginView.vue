<template>
  <div class="bx--grid main">
    <div class="bx--row">
      <div class="bx--col-lg-6 login-form">
        <cv-form>
          <h3 class="form-header">Авторизация</h3>
          <cv-text-input
            class="log-form"
            label="Логин"
            placeholder="Введите свой логин">
          </cv-text-input>
          <cv-text-input
            class="pass-form"
            label="Пароль"
            placeholder="Введите свой пароль">
          </cv-text-input>
          <div class="submit-btn">
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


@Component({ components: {} })
export default class LoginView extends Vue {

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


<script>
import Component from "vue-class-component";
import Vue from "vue";

@Component({ components: {} })
export default class LoginView extends Vue {

}

</script>
