<template>
  <cv-loading v-if='tokenStore.isLoading' overlay style='background: white' />
  <div v-else-if='tokenStore.isLogin' :class='current_theme' class='layout'>
    <lms-header @toggle-theme='toggleTheme($event)' class='layout-header' />
    <main class='layout-content'>
      <lms-breadcrumb class='main--breadcrumb' />
      <router-view />
    </main>
    <footer class='layout-footer'>
      <div class='layout-footer-label'>
        <div>
          <span>dvfu/imcs/staff & Daria-squad</span><br>
          <span>
            feel free to contribute
            <cv-link href='https://github.com/mesenev/lms'>
              <logo-github />
            </cv-link>
          </span>
        </div>
        <div>
          <span>{{ commit_hash }}</span>
        </div>
      </div>
    </footer>
  </div>
  <reset-password-view v-else-if='isResetPassword'></reset-password-view>
  <LoginView v-else-if='shouldRedirectToLogin'></LoginView>
</template>


<script lang='ts' setup>

import LogoGithub from '@carbon/icons-vue/es/logo--github/16'
import { THEMES } from '@/utils/consts'

import { useTokenStore } from '@/stores/modules/token'
import LmsHeader from '@/components/LmsHeader.vue'

import LoginView from '@/views/LoginView.vue'
import ResetPasswordView from '@/views/ResetPasswordView.vue'
import { useRoute } from 'vue-router'
import { computed, ref, watch } from 'vue'
import LmsBreadcrumb from '@/components/LmsBreadcrumb.vue'

const tokenStore = useTokenStore()
const route = useRoute()
tokenStore.setupTokenStore()

const current_theme = ref(localStorage.getItem('theme') || THEMES.g10)
const commit_hash = import.meta.env.GIT_HASH

function toggleTheme(theme: string) {
  current_theme.value = theme
  localStorage.setItem('theme', theme)
}

const isResetPassword = computed(() => {
  return route.name === 'ResetPasswordView'
})

const shouldRedirectToLogin = computed(() => {
  return !tokenStore.isLogin && !isResetPassword.value
})


</script>

<style lang='sass'>
@use '@carbon/themes'
@use 'carbon-components/scss/globals/scss/theme-tokens' as carbon
@import "styles/base"
@import "styles/carbon"

h1
  font-size: 2rem



body
  font-family: 'IBM Plex Sans', Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif

.main-title,
.lms-sidebar-logo,
.content-info-title,
.content-tasks-title,
.other-materials-title,
.lesson--list--title,
.materials-title,
.empty-title,
.no-lessons-title,
.title
  font-family: 'Medium Cyrillic', 'IBM Plex Sans', Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif
  font-weight: 500

.list-element--title,
.problem--title,
.submit-title,
.material-title
  font-family: 'IBM Plex Sans', Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif


.theme
  &-white
    //@include themes.theme($white)
    $carbon--theme: carbon.$carbon--theme--white
    @include carbon.carbon--theme(carbon.$carbon--theme--white, true)

  &-g10
    //@include themes.theme($g10)
    $carbon--theme: carbon.$carbon--theme--g10
    @include carbon.carbon--theme(carbon.$carbon--theme--g10, true)

  &-g90
    //@include themes.theme($g90)
    $carbon--theme: carbon.$carbon--theme--g90
    @include carbon.carbon--theme(carbon.$carbon--theme--g90, true)

  &-g100
    //@include themes.theme($g100)
    $carbon--theme: carbon.$carbon--theme--g100
    @include carbon.carbon--theme(carbon.$carbon--theme--g100, true)


.fade-enter-active, .fade-leave-active
  transition: opacity .1s


.fade-enter, .fade-leave-to
  opacity: 0
/* .fade-leave-active in <2.1.8 */

</style>

<style scoped lang='stylus'>
@import 'styles/list-elements.styl';


.layout-content
  background transparent

.main--breadcrumb
  margin-top var(--cds-spacing-06);

.items
  display flex
  flex-wrap wrap

.item
  width: 60%
  color: var(--cds-support-02)

.layout
  min-height: 100%
  display grid
  grid-template-columns 10.75rem minmax(0, 1fr)
  grid-template-rows auto minmax(0, 1fr) auto
  gap .75rem
  padding 1rem
  background:
    radial-gradient(circle at 78% 86%, rgba(245, 82, 43, .96) 0, rgba(245, 82, 43, .72) 17%, rgba(223, 113, 91, .38) 37%, rgba(226, 226, 226, .72) 63%, rgba(247, 247, 247, .96) 100%),
    linear-gradient(135deg, #f8f8f8 0%, #eeeeee 47%, #f7d8d1 100%)
  background-attachment fixed

  &-content
    padding-bottom var(--cds-spacing-05)
    grid-column 2
    grid-row 2
    min-width 0
    min-height 36rem
    padding 2rem 2rem 3rem
    border-radius 2px
    background transparent

  &-header, &-footer
    flex-shrink 0

  &-footer
    grid-column 1 / -1
    grid-row 3
    min-height 100px
    background-color #161616
    color var(--cds-text-05)
    font-size 0.7em

    &-link
      color var(--cds-text-05)

    &-label
      margin var(--cds-spacing-06) var(--cds-spacing-06)

  &-content
    width: 100%

@media (max-width: 900px)
  .layout
    grid-template-columns minmax(0, 1fr)
    grid-template-rows auto auto minmax(0, 1fr) auto
    padding .5rem

    &-content
      grid-column 1
      grid-row 3
      padding 1.25rem 1rem 2rem

    &-footer
      grid-column 1
      grid-row 4
</style>

<style lang='stylus'>
@import "styles/list-elements";
</style>
