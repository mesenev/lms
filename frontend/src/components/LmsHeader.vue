<template>
  <div class="lms-chrome">
    <aside class="lms-sidebar" aria-label="Основная навигация">
      <RouterLink class="lms-sidebar-logo" to="/">LMS</RouterLink>
      <nav class="lms-sidebar-nav">
        <RouterLink :to="{ name: 'profile-page', params: { userId: userStore.user.id } }">Мой профиль</RouterLink>
        <RouterLink to="/">Список курсов</RouterLink>
        <RouterLink v-if="courseSelected" :to="{ name: 'course-calendar', params: { courseId: route.params.courseId } }">
          Календарь
        </RouterLink>
        <RouterLink v-if="isStaff && courseSelected" :to="{ name: 'course-progress', params: { courseId: route.params.courseId } }">
          Успеваемость
        </RouterLink>
        <RouterLink v-if="isStaff && courseSelected" :to="{ name: 'course-groups', params: { courseId: route.params.courseId } }">
          Группы
        </RouterLink>
        <RouterLink :to="{ name: 'course-add', params: { courseId: null } }">Создать курс</RouterLink>
        <RouterLink :to="{ name: 'generate-course', params: { courseId: null } }">Сгенерировать курс</RouterLink>
      </nav>
      <button class="lms-logout" type="button" @click="logout">Выход</button>
    </aside>

    <header class="lms-topbar">
      <RouterLink class="lms-path" to="/">
        {{ headerPath }}
      </RouterLink>

      <nav v-if="contextLinks.length" class="lms-context-nav" aria-label="Навигация страницы">
        <RouterLink v-for="link in contextLinks" :key="link.label" :to="link.to">
          {{ link.label }}
        </RouterLink>
      </nav>

      <div class="lms-actions">
        <button class="lms-icon-button" type="button" aria-label="Профиль" @click="accountMenuOpen = !accountMenuOpen">
          <user-avatar-20/>
        </button>
        <button class="lms-icon-button lms-notification" type="button" aria-label="Оповещения">
          <notification-20/>
          <span class="lms-notification-dot"></span>
        </button>
        <label class="lms-search">
          <search-20/>
          <input type="search" placeholder="Поиск"/>
        </label>
      </div>

      <div v-if="accountMenuOpen" class="lms-account-menu">
        <UserView :userProp="userStore.user" class="user-view"/>
        <RouterLink :to="{ name: 'profile-page', params: { userId: userStore.user.id } }" @click="accountMenuOpen = false">
          Профиль
        </RouterLink>
        <RouterLink to="/" @click="accountMenuOpen = false">Мои курсы</RouterLink>
        <RouterLink :to="{ name: 'course-add', params: { courseId: null } }" @click="accountMenuOpen = false">
          Создать курс
        </RouterLink>
        <RouterLink :to="{ name: 'generate-course', params: { courseId: null } }" @click="accountMenuOpen = false">
          Сгенерировать курс
        </RouterLink>
        <cv-toggle class="toggle-theme" label="Тема" value="" v-model="currentTheme">
          <template v-slot:text-left>
            <component :is="iconLight"></component>
          </template>
          <template v-slot:text-right>
            <component :is="iconDark"></component>
          </template>
        </cv-toggle>
        <button class="lms-account-logout" type="button" @click="logout">Выйти</button>
      </div>
    </header>
  </div>
</template>

<script lang="ts" setup>
import UserView from "@/components/UserComponent.vue";
// import LoginAsUserModal from "@/components/LoginAsUserModal.vue";
import useUserStore from "@/stores/modules/user";
// import AppSwitcher20 from '@carbon/icons-vue/es/app-switcher/20';
import Notification20 from '@carbon/icons-vue/es/notification/20';
import UserAvatar20 from '@carbon/icons-vue/es/user--avatar/20';
import Light20 from '@carbon/icons-vue/es/light/20'
import Asleep20 from '@carbon/icons-vue/es/asleep/20'
import Search20 from '@carbon/icons-vue/es/search/20'
import { useTokenStore } from "@/stores/modules/token";
import { THEMES } from '@/utils/consts'
import { useRoute, type RouteLocationRaw } from 'vue-router'
import { computed, ref, watch } from "vue";
import useCourseStore from "@/stores/modules/course";

type HeaderLink = {
  label: string;
  to: RouteLocationRaw;
}

const iconLight = Light20;
const iconDark = Asleep20;

const userStore = useUserStore();
const courseStore = useCourseStore();
const tokenStore = useTokenStore();
const accountMenuOpen = ref(false);

const emit = defineEmits<{ (e: 'toggle-theme', theme: string): void }>();

const route = useRoute()

async function logout() {
  await tokenStore.logout();
  window.location.reload();
}

const courseSelected = computed((): boolean => {
  return route.params.hasOwnProperty('courseId') && route.params['courseId'] != null;
})

const lessonSelected = computed((): boolean => {
  return route.params.hasOwnProperty('lessonId') && route.params['lessonId'] != null;
})

const problemSelected = computed((): boolean => {
  return route.params.hasOwnProperty('problemId') && route.params['problemId'] != null;
})

const examSelected = computed((): boolean => {
  return route.params.hasOwnProperty('examId') && route.params['examId'] != null;
})

const materialSelected = computed((): boolean => {
  return route.params.hasOwnProperty('materialId') && route.params['materialId'] != null;
})

const getTheme = computed((): boolean => {
  return localStorage.getItem('theme') === THEMES.g90
})

const currentTheme = ref<boolean>(getTheme.value);

watch(() => currentTheme.value, () => {
  emit('toggle-theme', currentTheme.value ? THEMES.g90 : THEMES.g10)
})

const isStaff = computed((): boolean => {
  return userStore.user.staff_for.includes(Number(route.params.courseId))
    || courseSelected.value && courseStore.currentCourse?.author?.id === userStore.user.id;
})

const headerPath = computed((): string => {
  const courseName = courseStore.currentCourse?.name;
  if (!courseSelected.value || !courseName) {
    return 'Список курсов';
  }
  return `Список курсов/${courseName}`;
})

const contextLinks = computed<HeaderLink[]>(() => {
  const links: HeaderLink[] = [];
  if (courseSelected.value) {
    links.push({
      label: 'Решения',
      to: { name: 'course-solutions-list', params: { courseId: route.params.courseId } }
    });
  }
  if (isStaff.value && courseSelected.value) {
    links.push({
      label: 'Успеваемость',
      to: { name: 'course-progress', params: { courseId: route.params.courseId } }
    });
    links.push({
      label: 'Календарь',
      to: { name: 'course-calendar', params: { courseId: route.params.courseId } }
    });
  }
  if (isStaff.value && courseSelected.value && !lessonSelected.value && !problemSelected.value) {
    links.push({
      label: 'Группы',
      to: { name: 'course-groups', params: { courseId: route.params.courseId } }
    });
    links.push({
      label: 'Редактировать курс',
      to: { name: 'course-edit', params: { courseId: route.params.courseId } }
    });
  }
  if (isStaff.value && lessonSelected.value) {
    links.push({
      label: 'Успеваемость урока',
      to: { name: 'lesson-progress', params: { lessonId: route.params.lessonId, courseId: route.params.courseId } }
    });
  }
  if (isStaff.value && lessonSelected.value && !problemSelected.value && !materialSelected.value && !examSelected.value) {
    links.push({
      label: 'Редактировать урок',
      to: { name: 'lesson-edit', params: { lessonId: route.params.lessonId } }
    });
  }
  if (isStaff.value && problemSelected.value) {
    links.push({
      label: 'Редактировать задачу',
      to: { name: 'problem-edit', params: { problemId: route.params.problemId } }
    });
  }
  if (isStaff.value && examSelected.value) {
    links.push({
      label: 'Редактировать тест',
      to: { name: 'exam-edit', params: { examId: route.params.examId } }
    });
  }
  if (isStaff.value && materialSelected.value) {
    links.push({
      label: 'Редактировать материалы',
      to: { name: 'material-edit', params: { materialId: route.params.materialId } }
    });
  }
  return links;
})

</script>

<style scoped lang="stylus">

.lms-chrome
  display contents
  color #111

.lms-sidebar
  z-index 7000
  grid-column 1
  grid-row 1 / span 2
  width 10.75rem
  min-height 33.5rem
  max-height calc(100vh - 2rem)
  display flex
  flex-direction column
  padding 1.55rem 1.35rem
  overflow-y auto
  background #cfcfcf
  border-radius 10px
  box-shadow 0 16px 35px rgba(0, 0, 0, 0.12)

.lms-sidebar-logo
  display block
  margin-bottom 3rem
  color #050505
  font-size 2.55rem
  line-height 1
  font-weight 900
  letter-spacing 0
  text-transform uppercase
  text-decoration none

.lms-sidebar-logo:hover
  background transparent

.lms-sidebar-nav
  display flex
  flex-direction column
  gap 1.05rem

.lms-sidebar-nav a
  color #171717
  font-size 1rem
  line-height 1.2
  font-weight 500
  text-decoration none

.lms-sidebar-nav a:hover,
.lms-sidebar-nav a.router-link-active
  color #000
  background transparent
  text-decoration underline
  text-underline-offset 4px

.lms-logout
  width 5.55rem
  min-height 1.45rem
  margin-top auto
  align-self center
  border 0
  border-radius 3px
  background #505050
  color #fff
  font-size .86rem
  font-weight 700
  cursor pointer

.lms-topbar
  position relative
  z-index 6500
  grid-column 2
  grid-row 1
  min-height 2.1rem
  display flex
  align-items center
  gap .75rem
  padding .25rem .45rem .25rem 1.5rem
  background #cfcfcf
  border-radius 6px
  box-shadow 0 7px 20px rgba(0, 0, 0, 0.10)

.lms-path
  min-width 0
  max-width 38rem
  overflow hidden
  white-space nowrap
  text-overflow ellipsis
  color #222
  font-size .9rem
  text-decoration none

.lms-path:hover
  background transparent

.lms-context-nav
  min-width 0
  display flex
  gap .35rem
  align-items center
  overflow hidden

.lms-context-nav a
  flex 0 0 auto
  max-width 12rem
  overflow hidden
  white-space nowrap
  text-overflow ellipsis
  padding .3rem .55rem
  border-radius 4px
  color #1d1d1d
  font-size .78rem
  line-height 1
  text-decoration none

.lms-context-nav a:hover,
.lms-context-nav a.router-link-active
  background rgba(255, 255, 255, .55)

.lms-actions
  position relative
  display flex
  align-items center
  gap .35rem
  margin-left auto

.lms-icon-button
  position relative
  width 1.35rem
  height 1.35rem
  display inline-flex
  align-items center
  justify-content center
  border 0
  padding 0
  border-radius 50%
  color #000
  background transparent
  cursor pointer

.lms-icon-button:hover
  background rgba(255, 255, 255, .55)

.lms-notification-dot
  position absolute
  top .05rem
  right .05rem
  width .45rem
  height .45rem
  border 1px solid #fff
  border-radius 50%
  background #f24a43

.lms-search
  height 1.55rem
  width 7.1rem
  display flex
  align-items center
  gap .2rem
  padding 0 .35rem
  border 1px solid #ababab
  border-radius 5px
  background #f5f5f5
  color #b8b8b8

.lms-search svg
  flex 0 0 auto

.lms-search input
  width 100%
  min-width 0
  border 0
  outline none
  background transparent
  color #222
  font-size .82rem

.lms-search input::placeholder
  color #b8b8b8

.lms-account-menu
  position absolute
  top calc(100% + .45rem)
  right .45rem
  width 18rem
  display flex
  flex-direction column
  gap .15rem
  padding .85rem
  background #f4f4f4
  border 1px solid #d0d0d0
  border-radius 7px
  box-shadow 0 18px 40px rgba(0, 0, 0, .22)

.lms-account-menu a,
.lms-account-logout
  min-height 2rem
  display flex
  align-items center
  padding 0 .55rem
  border 0
  border-radius 4px
  background transparent
  color #161616
  font-size .9rem
  text-align left
  text-decoration none
  cursor pointer

.lms-account-menu a:hover,
.lms-account-logout:hover
  background #e0e0e0

.user-view
  padding .25rem .25rem .65rem

.toggle-theme
  margin .45rem 0 .35rem

@media (max-width: 900px)
  .lms-sidebar
    grid-column 1
    grid-row 1
    width auto
    max-height none
    min-height 4.2rem
    display grid
    grid-template-columns auto 1fr auto
    align-items center
    padding .75rem 1rem

  .lms-sidebar-logo
    margin 0 1rem 0 0
    font-size 2rem

  .lms-sidebar-nav
    flex-direction row
    gap .75rem
    overflow-x auto

  .lms-sidebar-nav a
    white-space nowrap

  .lms-logout
    margin-top 0

  .lms-topbar
    grid-column 1
    grid-row 2
    flex-wrap wrap
    padding .4rem .5rem

  .lms-context-nav
    order 3
    width 100%
    overflow-x auto

  .lms-search
    width 6.5rem
</style>
