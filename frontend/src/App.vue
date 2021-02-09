<template>
  <div class="layout">
    <lms-header class="layout-header"/>
    <main class="layout-content">
      <lms-breadcrumb />
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>
    </main>
    <footer class="layout-footer">
      <div class="layout-footer-label">
        <span>dvfu/imcs/staff & Daria-squad</span><br>
        <span>
          feel free to contribute
          <cv-link href="https://github.com/mesenev/lms"><logo-github/></cv-link>
        </span>
      </div>
    </footer>
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

  &-content
    background-color var(--cds-ui-01)
    padding-bottom var(--cds-spacing-05)

  &-header, &-footer
    flex-shrink 0

  &-footer
    min-height 100px
    background-color var(--cds-ui-05)
    color var(--cds-text-05)
    font-size 0.7em

    &-label
      margin 30px 30px

  &-content
    flex-grow 1
    width: 100%
</style>

<script lang="ts">
import LmsBreadcrumb from '@/components/LmsBreadcrumb.vue'
import LmsHeader from '@/components/LmsHeader.vue';
import LogoGithub from '@carbon/icons-vue/es/logo--github/16';
import { Component, Vue } from 'vue-property-decorator';

@Component({ components: { LmsHeader, LmsBreadcrumb, LogoGithub } })
export default class App extends Vue {

}
</script>

<style lang="scss">
@import "styles/carbon";

html, body, body > div {
  height: 100%;
  background-color: var(--cds-ui-background);
  color: var(--cds-text-01);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .1s
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */
{
  opacity: 0
}
</style>
