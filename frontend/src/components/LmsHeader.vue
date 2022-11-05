<template>
  <cv-header class="lms-header" aria-label="Carbon tutorial">
    <cv-skip-to-content href="#main-content"> Skip to content</cv-skip-to-content>
    <cv-header-menu-button v-if="courseSelected" aria-controls="side-nav" aria-label="Header menu"/>
    <cv-header-name prefix="dvfu" to="/"><span class="lms">lms</span></cv-header-name>
    <cv-header-nav v-if="courseSelected">
      <cv-header-menu-item
        :to="{
          name: 'course-solutions-list',
          params: { courseId: this.$route.params.courseId }
        }"
      >
        Решения
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="courseSelected">
      <cv-header-menu-item
        :to="{
          name: 'course-progress',
          params: { courseId: this.$route.params.courseId }
        }"
      >
        Успеваемость
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="lessonSelected">
      <cv-header-menu-item
        :to="{
          name: 'lesson-progress',
          params: { lessonId: this.$route.params.lessonId }
        }"
      >
        Успеваемость урока
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="courseSelected">
      <cv-header-menu-item
        :to="{ name: 'course-calendar', params: { courseId: this.$route.params.courseId } }"
      >
        Календарь
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="isStaff && courseSelected && !lessonSelected && !problemSelected">
      <cv-header-menu-item
        :to="{ name: 'course-edit', params: { courseId: this.$route.params.courseId } }"
      >
        Редактировать курс
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="isStaff && lessonSelected && !problemSelected && !materialSelected">
      <cv-header-menu-item
        :to="{ name: 'lesson-edit', params: { lessonId: this.$route.params.lessonId } }"
      >
        Редактировать урок
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="isStaff && problemSelected">
      <cv-header-menu-item
        :to="{ name: 'problem-edit', params: { problemId: this.$route.params.problemId } }"
      >
        Редактировать задачу
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="isStaff && materialSelected">
      <cv-header-menu-item
        :to="{ name: 'material-edit', params: { materialId: this.$route.params.materialId } }"
      >
        Редактировать материалы
      </cv-header-menu-item>
    </cv-header-nav>

    <template slot="left-panels">
      <cv-side-nav id="side-nav" fixed>
        <cv-side-nav-items>
          <cv-header-side-nav-items>
            <cv-header-menu-item
              v-if="courseSelected"
              :to=" { name: 'course-solutions-list', params: { courseId: this.$route.params.courseId } }"
            >
              Решения
            </cv-header-menu-item>
            <cv-header-menu-item
              v-if="courseSelected"
              :to="{ name: 'course-progress', params: { courseId: this.$route.params.courseId } }"
            >
              Успеваемость
            </cv-header-menu-item>
            <cv-header-menu-item
              v-if="lessonSelected"
              :to="{ name: 'lesson-progress', params: { lessonId: this.$route.params.lessonId } }"
            >
              Успеваемость урока
            </cv-header-menu-item>
            <cv-header-menu-item
              v-if="courseSelected"
              :to="{ name: 'course-calendar', params: { courseId: this.$route.params.courseId } }"
            >
              Календарь
            </cv-header-menu-item>
            <cv-header-menu-item
              v-if="isStaff && courseSelected && !lessonSelected && !problemSelected"
              :to="{ name: 'course-edit', params: { courseId: this.$route.params.courseId } }"
            >
              Редактировать курс
            </cv-header-menu-item>
            <cv-header-menu-item
              v-if="isStaff && lessonSelected && !problemSelected && !materialSelected"
              :to="{ name: 'lesson-edit', params: { lessonId: this.$route.params.lessonId } }"
            >
              Редактировать урок
            </cv-header-menu-item>
            <cv-header-menu-item
              v-if="isStaff && problemSelected"
              :to="{ name: 'problem-edit', params: { problemId: this.$route.params.problemId } }"
            >
              Редактировать задачу
            </cv-header-menu-item>
            <cv-header-menu-item
              v-if="isStaff && materialSelected"
              :to="{ name: 'material-edit', params: { materialId: this.$route.params.materialId } }"
            >
              Редактировать материалы
            </cv-header-menu-item>
          </cv-header-side-nav-items>
        </cv-side-nav-items>
      </cv-side-nav>
    </template>
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
        <UserView :userProp="user" class="user-view"/>
        <cv-switcher>
          <template>
            <cv-switcher-item>
              <cv-dropdown v-model="current_theme">
                <cv-dropdown-item :value="themes.white">white</cv-dropdown-item>
                <cv-dropdown-item :value="themes.grey_10">g10</cv-dropdown-item>
                <cv-dropdown-item :value="themes.grey_90">g90</cv-dropdown-item>
                <cv-dropdown-item :value="themes.grey_100">g100</cv-dropdown-item>
              </cv-dropdown>
            </cv-switcher-item>
            <cv-switcher-item>
              <cv-switcher-item-link
                :to="{
                  name: 'profile-page',
                  params:  { userId: this.user.id }
                }"
              >
                Профиль
              </cv-switcher-item-link>
            </cv-switcher-item>
            <cv-switcher-item>
              <cv-switcher-item-link to="/">
                Мои курсы
              </cv-switcher-item-link>
            </cv-switcher-item>
            <cv-switcher-item>
              <cv-switcher-item-link :to="{
                  name: 'course-add',
                  params:  { courseId: null }
                }"
              >
                Создать курс
              </cv-switcher-item-link>
            </cv-switcher-item>
            <LoginAsUserModal/>
            <cv-switcher-item>
              <cv-switcher-item-link @click="logout" > Выйти </cv-switcher-item-link>
            </cv-switcher-item>
          </template>
        </cv-switcher>
      </cv-header-panel>
    </template>

    <template slot="right-panels">
      <cv-header-panel class="" id="notifications">
        <span class="acc_text">Оповещения</span>
        <cv-switcher>
          <template>
            <cv-switcher-item>
              <cv-switcher-item-link to="/">
                <cv-toast-notification
                  caption="текст оповещения"
                  kind="info"
                  title="тестовое уведомление"/>
              </cv-switcher-item-link>
            </cv-switcher-item>
          </template>
        </cv-switcher>
      </cv-header-panel>
    </template>
  </cv-header>
</template>

<script lang="ts">
import UserView from "@/components/UserComponent.vue";
import LoginAsUserModal from "@/components/LoginAsUserModal.vue";
import userStore from "@/store/modules/user";
import AppSwitcher20 from '@carbon/icons-vue/es/app-switcher/20';
import Notification20 from '@carbon/icons-vue/es/notification/20';
import UserAvatar20 from '@carbon/icons-vue/es/user--avatar/20';
import Vue from 'vue';
import Component from 'vue-class-component';
import tokenStore from '@/store/modules/token'
import {themes} from '@/utils/consts'
import { Watch } from "vue-property-decorator";
import ProblemModel from "@/models/ProblemModel";

@Component({ components: { UserView, LoginAsUserModal, Notification20, UserAvatar20, AppSwitcher20 } })
export default class LmsHeader extends Vue {

  @Watch('current_theme')
  changeTheme(){
    this.$emit("change-theme", this.current_theme);
  }

  current_theme = '';
  themes = themes;
  user = userStore.user;

  logout(){
    tokenStore.logout();
  }

  get courseSelected(): boolean {
    return this.$route.params.hasOwnProperty('courseId') && this.$route.params['courseId'] != null;
  }

  get lessonSelected(): boolean {
    return this.$route.params.hasOwnProperty('lessonId') && this.$route.params['lessonId'] != null;
  }

  get problemSelected(): boolean {
    return this.$route.params.hasOwnProperty('problemId') && this.$route.params['problemId'] != null;
  }

  get materialSelected(): boolean {
    return this.$route.params.hasOwnProperty('materialId') && this.$route.params['materialId'] != null;
  }

  get isStaff(): boolean {
    return this.user.staff_for.includes(Number(this.$route.params.courseId));
  }

}
</script>

<style scoped lang="stylus">


</style>
