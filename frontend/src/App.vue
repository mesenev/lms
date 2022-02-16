<template>
  <div class="layout">
    <lms-header class="layout-header"/>
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
</template>

<style lang="scss">
@import "styles/base";
@import "styles/carbon";

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
  color: var(--cds-support-02)

.layout
  height: 100%
  display flex
  flex-flow column

  &-content
    background-color var(--cds-ui-01)
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

<script lang="ts">
import LmsBreadcrumb from '@/components/LmsBreadcrumb.vue'
import LmsHeader from '@/components/LmsHeader.vue';
import LogoGithub from '@carbon/icons-vue/es/logo--github/16';
import { Component, Vue } from 'vue-property-decorator';

@Component({ components: { LmsHeader, LmsBreadcrumb, LogoGithub } })
export default class App extends Vue {
  public connection?: WebSocket;
  public signals: unknown;
  created() {
            this.connection = new WebSocket(
              'ws://' + window.location.host + `/ws/notifications?user_id=${123}&problem_id=${456}`
              );
            this.connection.onmessage = (event) => {
                this.signals = event.data;
                console.log("Successfully retrieved message from websocket");
                console.log(this.signals);
            };
  }
}
</script>
