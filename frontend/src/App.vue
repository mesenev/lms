<template>
  <cv-loading v-if="isLoading" overlay style="background: white"/>
  <div v-else-if="isLogin" :class="current_theme" class="layout">
    <lms-header @toggle-theme="toggleTheme($event)" class="layout-header"/>
    <main class="layout-content">
      <lms-breadcrumb class="main--breadcrumb"/>
      <transition name="fade" mode="out-in">
        <router-view/>
      </transition>
    </main>
    <footer class="layout-footer">
      <div class="layout-footer-label">
        <div>
          <span>dvfu/imcs/staff & Daria-squad</span><br>
          <span>
            feel free to contribute
            <cv-link href="https://github.com/mesenev/lms">
              <logo-github/>
            </cv-link>
          </span>
        </div>
          <cv-link class="layout-footer-link" href="https://t.me/+FBUuuC4qdvc1ZTIy">
            <span><b>Чат для обратной связи</b></span>
          </cv-link>
      </div>
    </footer>
  </div>
  <reset-password-view v-else-if="isResetPassword"></reset-password-view>
  <LoginView v-else-if="shouldRedirectToLogin"></LoginView>
</template>

<script lang="ts">
import LmsBreadcrumb from '@/components/LmsBreadcrumb.vue';
import LmsHeader from '@/components/LmsHeader.vue';
import LogoGithub from '@carbon/icons-vue/es/logo--github/16';
import FaceWink from '@carbon/icons-vue/es/face--wink/16';
import { Component, Vue, Watch } from 'vue-property-decorator';
import { THEMES } from "@/utils/consts";
import LoginView from "@/views/LoginView.vue";
import tokenStore from "@/store/modules/token";
import ResetPasswordView from "@/views/ResetPasswordView.vue";

@Component({ components: {
  ResetPasswordView, LoginView, LmsHeader, LmsBreadcrumb, LogoGithub, FaceWink
} })
export default class App extends Vue {
  //TODO set transition and styles for loader
  @Watch('isLogin')
  onIsLoginChanged(new_val: boolean, old_val: boolean) {
    if (new_val) {
        this.$router.push(((this.$route.query.nextUrl) ?? "/") as string);
    } else {
      if (this.shouldRedirectToLogin) {
        this.$router.push('/login');
      }
    }
  }

  current_theme = localStorage.getItem('theme') || THEMES.g10;

  toggleTheme(theme: string) {
    this.current_theme = theme;
    localStorage.setItem('theme', theme);
  }

  get isLoading() {
    return tokenStore.isLoading;
  }

  get isLogin() {
    return tokenStore.isAuthenticated;
  }

  get isResetPassword() {
    return this.$route.name === 'ResetPasswordView';
  }

  get shouldRedirectToLogin() {
    return !this.isLogin && !this.isResetPassword;
  }

  async created() {
    await tokenStore.setupTokenStore();
  }
}
</script>

<style lang="sass">
@use '~@carbon/themes'
@use '~carbon-components/scss/globals/scss/theme-tokens' as carbon
@import "styles/base"
@import "styles/carbon"

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

<style scoped lang="stylus">
@import 'styles/list-elements.styl';

.layout-content
  background-color var(--cds-ui-background)

.main--breadcrumb
  margin-top var(--cds-spacing-06);

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
  &-content
    padding-bottom var(--cds-spacing-05)
    margin-top: 3rem;
  &-header, &-footer
    flex-shrink 0
  &-footer
    min-height 100px
    background-color #161616
    color var(--cds-text-05)
    font-size 0.7em

    &-link
      color var(--cds-text-05)
    &-label
      margin var(--cds-spacing-06) var(--cds-spacing-06)
  &-content
    flex-grow 1
    width: 100%
</style>

<style lang="stylus">
@import "styles/list-elements";
</style>
