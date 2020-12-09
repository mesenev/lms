<template>
  <cv-header class="lms-header" aria-label="Carbon tutorial">
    <cv-skip-to-content href="#main-content">
      Skip to content
    </cv-skip-to-content>
    <cv-header-name to="/" prefix="dvfu">
      <span class="lms">⠀lms</span>
    </cv-header-name>

    <cv-header-nav aria-label="">
      <cv-header-menu-item to="/overall">Overall page</cv-header-menu-item>
    </cv-header-nav>

    <template slot="header-global">
      <cv-header-global-action aria-label="Notifications">
        <notification-20/>
      </cv-header-global-action>
      <cv-header-global-action aria-label="User avatar">
        <user-avatar-20/>
      </cv-header-global-action>
      <cv-header-global-action aria-label="App switcher">
        <app-switcher-20/>
      </cv-header-global-action>
    </template>
  </cv-header>
</template>

<script lang="ts">
import AppSwitcher20 from '@carbon/icons-vue/es/app-switcher/20';
import Notification20 from '@carbon/icons-vue/es/notification/20';
import UserAvatar20 from '@carbon/icons-vue/es/user--avatar/20';
import Vue from 'vue';
import Component from 'vue-class-component';

@Component({ components: { Notification20, UserAvatar20, AppSwitcher20 } })
export default class LmsHeader extends Vue {
}
</script>

<style scoped lang="stylus">
.bx--header
  position: unset
</style>
