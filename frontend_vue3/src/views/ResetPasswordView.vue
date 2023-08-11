<template>
  <div>
    ResetPasswordView
  </div>
</template>

<script lang="ts" setup>
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import api from "@/stores/services/api";

</script>

<style lang="stylus" scoped>


.reset-password
  width 20%
  text-align end
  @media (min-width: 401px)
    min-width 400px
  @media (max-width: 400px)
    min-width 80%

.form
  position absolute
  width 100%
  height 100%
  display flex
  flex-direction column
  align-items center
  justify-content center

.submit-btn
  display flex
  flex-direction row
  justify-content center

.form-header
  text-align center
  padding-bottom 2rem

.log-form
  padding-bottom 2rem

.pass-form
  padding-bottom 0.5rem

.main
  text-align center
  padding 5rem

.login-form
  padding 3rem
  background-color var(--cds-ui-background)


</style>
