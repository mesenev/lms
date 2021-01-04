<template>
  <cv-header class="lms-header" aria-label="Carbon tutorial">
    <cv-skip-to-content href="#main-content">
      Skip to content
    </cv-skip-to-content>
    <cv-header-name to="/" prefix="dvfu">
      <span class="lms">lms</span>
    </cv-header-name>

    <cv-header-nav v-if="courseSelected">
      <cv-header-menu-item
        :to="{
          name: 'course-solutions-list',
          params: { courseId: this.$route.params.courseId }
        }">
        Решения
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="courseSelected">
      <cv-header-menu-item
        :to="{
          name: 'course-progress',
          params: { courseId: this.$route.params.courseId }
        }">
        Успеваемость
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="courseSelected">
      <cv-header-menu-item
        :to="{
          name: 'course-calendar',
          params: { courseId: this.$route.params.courseId }
        }">
        Календарь
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="courseSelected">
      <cv-header-menu-item
        :to="{
          name: 'course-edit',
          params: { courseId: this.$route.params.courseId }
        }">
        Изменить
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="lessonSelected">
      <cv-header-menu-item
        :to="{
          name: 'lesson-edit',
          params: { lessonId: this.$route.params.lessonId }
        }">
        Изменить
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="problemSelected">
      <cv-header-menu-item
        :to="{
          name: 'problem-edit',
          params: { courseId: this.$route.params.problemId }
        }">
        Изменить задание
      </cv-header-menu-item>
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

  get courseSelected(): boolean {
    return this.$route.params.hasOwnProperty('courseId');
  }
  get lessonSelected(): boolean {
    return this.$route.params.hasOwnProperty('lessonId');
  }

  get problemSelected(): boolean {
    return this.$route.params.hasOwnProperty('problemId');
  }

}
</script>

<style scoped lang="stylus">
.bx--header
  position: unset

.lms
  padding-left 5px
</style>
