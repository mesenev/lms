<template>
  <div class="layout">
    <header class="layout-header">
      <h1 class="title">Курсы</h1>
    </header>
    <main class="layout-content">
      <cv-button>button</cv-button>
      <div class="items">
        <div class="item" v-for="{ id } of courses" :key="id">
          Курс номер {{ id }}
        </div>
      </div>
<!--      <cv-content>-->
        <router-view/>
<!--      </cv-content>-->
    </main>
    <footer class="layout-footer"> (c) pocony</footer>
  </div>
</template>
<style scoped lang="stylus">
.items
  display flex
  flex-wrap wrap

.item
  width: 60%
  color: var(--cds-support-02)

.layout
  height: 100%
  display flex
  flex-flow column
  //background gray

  &-header, &-footer
    flex-shrink 0

  &-content
    flex-grow 1
</style>
<script>
// import Notification32 from '@carbon/icons-vue/es/notification/20';
// import UserAvatar32 from '@carbon/icons-vue/es/user--avatar/20';
// import AppSwitcher32 from '@carbon/icons-vue/es/app-switcher/20';

export default {
  name: 'App',
  data: () => ({
    courses: [
      { id: 1 },
      { id: 2 },
      { id: 3 },
      { id: 4 },
      { id: 5 },
    ],
  }),
};
</script>
<style lang="scss">
@import "styles/carbon";

html, body, body > div {
  height: 100%;
}
</style>
