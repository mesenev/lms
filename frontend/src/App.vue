<template>
  <div>
    <span>App main view</span>
    <br>
    <router-view class="router-view"/>
  </div>
</template>

<style lang="stylus">
#app
  font-family Avenir, Helvetica, Arial, sans-serif
  -webkit-font-smoothing antialiased
  -moz-osx-font-smoothing grayscale
  text-align center
  color #2c3e50
  margin-top 60px

.router-view
  margin 0 auto
  padding-top 100px
</style>
