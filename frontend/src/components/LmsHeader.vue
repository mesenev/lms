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
    <cv-header-nav v-if="courseSelected && !lessonSelected && !problemSelected">
      <cv-header-menu-item
        :to="{
          name: 'course-edit',
          params: { courseId: this.$route.params.courseId }
        }">
        Изменить
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="lessonSelected && !problemSelected && !materialSelected">
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
        Изменить
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="materialSelected">
      <cv-header-menu-item
        :to="{
          name: 'material-edit',
          params: { materialId: this.$route.params.materialId }
        }">
        Изменить
      </cv-header-menu-item>
    </cv-header-nav>

    <template slot="header-global">
      <cv-header-global-action aria-label="Notifications"
      aria-controls="notifications">
        <notification-20/>
      </cv-header-global-action>
      <cv-header-global-action aria-label="User avatar"
                               aria-controls="account">
        <user-avatar-20/>
      </cv-header-global-action>
    </template>

    <template slot="right-panels">
      <cv-header-panel class="" id="account">
        <UserView class="user-view" :user="user"/>
        <cv-switcher>
          <template>
            <cv-switcher-item>
              <cv-switcher-item-link
                :to="{
                  name: 'profile-page',
                  params:  { courseId: this.$route.params.courseId }
                }" >
                Профиль
              </cv-switcher-item-link>
            </cv-switcher-item>
            <!-- About -->
            <cv-switcher-item>
              <cv-switcher-item-link to="/">
                Мои курсы
              </cv-switcher-item-link>
              <cv-switcher-item-link to="/">
                Выйти
              </cv-switcher-item-link>
            </cv-switcher-item>
          </template>
        </cv-switcher>
      </cv-header-panel>
    </template>

    <template slot="right-panels">
      <cv-header-panel class="" id="notifications">
        <span class="acc_text">Оповещения </span>
        <cv-switcher>
          <template>
            <cv-switcher-item>
              <cv-switcher-item-link to="/" >
                <cv-toast-notification
                title="тестовое уведомление"
                caption="текст оповещения"></cv-toast-notification>
              </cv-switcher-item-link>
            </cv-switcher-item>
          </template>
        </cv-switcher>
      </cv-header-panel>
    </template>
  </cv-header>
</template>

<script lang="ts">
import AppSwitcher20 from '@carbon/icons-vue/es/app-switcher/20';
import Notification20 from '@carbon/icons-vue/es/notification/20';
import UserAvatar20 from '@carbon/icons-vue/es/user--avatar/20';
import Vue from 'vue';
import Component from 'vue-class-component';
import UserView from "@/views/UserView.vue";
import {userStore} from "@/store";

@Component({ components: {UserView, Notification20, UserAvatar20, AppSwitcher20 } })
export default class LmsHeader extends Vue {

  user = userStore.user;

  get courseSelected(): boolean {
    return this.$route.params.hasOwnProperty('courseId');
  }
  get lessonSelected(): boolean {
    return this.$route.params.hasOwnProperty('lessonId');
  }

  get problemSelected(): boolean {
    return this.$route.params.hasOwnProperty('problemId');
  }

  get materialSelected(): boolean {
    return this.$route.params.hasOwnProperty('materialId');
  }
}
</script>

<style scoped lang="stylus">
.bx--header
  position: unset

.lms
  padding-left 5px

.acc_text
    margin: 32px 1rem 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid #525252;
.user-view
    padding-left 30px;
    padding-top 10px;
    margin-bottom 0px;
</style>
