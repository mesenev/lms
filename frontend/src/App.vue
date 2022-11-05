<template>
  <cv-loading v-if="isLoading" overlay style="background: white"/>
  <div v-else-if="!isLoading && isLogin" v-bind:class="{
    white_theme: current_theme===this.themes.white,
    g10_theme: current_theme===this.themes.grey_10,
    g90_theme: current_theme===this.themes.grey_90,
    g100_theme: current_theme===this.themes.grey_100
  }" class="layout"
  >

    <lms-header @change-theme="changeTheme($event)" class="layout-header"/>

    <main class="layout-content">
      <lms-breadcrumb class="main--breadcrumb"/>
      <transition name="fade" mode="out-in">
        <router-view/>
      </transition>
    </main>
    <footer class="layout-footer">
      <div class="layout-footer-label">
        <span>dvfu/imcs/staff & Daria-squad</span><br>
        <span>
          feel free to contribute
          <cv-link href="https://github.com/mesenev/lms">
            <logo-github/>
          </cv-link>
        </span>
      </div>
    </footer>
  </div>
  <LoginView class="g100-theme" v-else></LoginView>
</template>

<script lang="ts">
import LmsBreadcrumb from '@/components/LmsBreadcrumb.vue';
import LmsHeader from '@/components/LmsHeader.vue';
import LogoGithub from '@carbon/icons-vue/es/logo--github/16';
import { Component, Vue, Watch } from 'vue-property-decorator';
import LoginView from "@/views/LoginView.vue";
import tokenStore from "@/store/modules/token";
import {themes} from '@/utils/consts';

@Component({ components: { LoginView, LmsHeader, LmsBreadcrumb, LogoGithub } })
export default class App extends Vue {
  //TODO set transition and styles for loader

  @Watch('isLogin')
  onIsLoginChanged(new_val: boolean) {
    if (new_val) {
      this.$router.push(((this.$route.query.nextUrl) ?? "/") as string);
    } else {
      this.$router.push('/login');
    }
  }

  themes = themes
  current_theme = this.themes.white

  changeTheme(theme: string){
    this.current_theme = theme;

  }

  get isLoading() {
    return tokenStore.isLoading;
  }
  get isLogin() {
    return tokenStore.isAuthenticated;
  }
  async created() {
    await tokenStore.setupTokenStore();
  }
}
</script>

<style lang="scss">
@use '~@carbon/themes';
@use '~@carbon/colors';

@import "styles/base";
@import "styles/carbon";

.white_theme {
  @include themes.theme($white)
}

.g10_theme {
  @include themes.theme($g10);
}

.g90_theme {
  @include themes.theme($g90);
}

.g100_theme {
  @include themes.theme($g100);
}
.layout{
  background: themes.$background;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */
{
  opacity: 0;
}

</style>

<style scoped lang="stylus">
@import 'styles/list-elements.styl';

.main--breadcrumb
  margin-top var(--cds-spacing-06);
.items
  display flex
  flex-wrap wrap
.item
  width: 60%
  color: var(--cds-support-02);
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
    background-color var(--cds-ui-05)
    color var(--cds-text-05)
    font-size 0.7em
    &-label
      margin var(--cds-spacing-06) var(--cds-spacing-06)
  &-content
    flex-grow 1
    width: 100%
</style>

<style lang="stylus">
@import "styles/list-elements";
</style>


