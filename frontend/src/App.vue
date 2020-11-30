<template>
  <div>
    <header class="header">
      <div class="header__container">
        <div class="header__left"></div>
        <div class="header__right">
        </div>
      </div>
    </header>
    <router-view class="router-view"/>
  </div>
</template>
<script>

export default {
  name: 'App',
  data() {
    return {};
  },
};
</script>
<style lang="stylus">
body
  background-color #171b24
  color rgb(208, 212, 222)
  font-size 1.3em

a
  font-weight 700
  text-decoration none
  color rgb(208, 212, 222)

a:hover
  color rgb(167, 89, 255)

#app
  font-family Avenir, Helvetica, Arial, sans-serif
  -webkit-font-smoothing antialiased
  -moz-osx-font-smoothing grayscale
  text-align center
  margin-top 60px

.router-view
  margin 0 auto
  padding-top 100px
</style>
