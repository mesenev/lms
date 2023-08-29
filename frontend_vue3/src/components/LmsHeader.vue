<template>
  <cv-header class="lms-header" aria-label="Carbon tutorial">
    <cv-skip-to-content href="#main-content"> Skip to content </cv-skip-to-content>
    <cv-header-menu-button v-if="courseSelected" aria-controls="side-nav" aria-label="Header menu"/>
    <cv-header-name prefix="dvfu" to="/"><span class="lms"> lms </span></cv-header-name>
    <cv-header-nav v-if="courseSelected">
      <cv-header-menu-item
      >
        Решения
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="isStaff && courseSelected">
      <cv-header-menu-item
      >
        Успеваемость
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="isStaff && lessonSelected">
      <cv-header-menu-item
      >
        Успеваемость урока
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="isStaff && courseSelected">
      <cv-header-menu-item
      >
        Календарь
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="isStaff && courseSelected && !lessonSelected && !problemSelected">
      <cv-header-menu-item
      >
        Редактировать курс
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav
        v-if="isStaff && lessonSelected && !problemSelected && !materialSelected && !examSelected">
      <cv-header-menu-item
      >
        Редактировать урок
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="isStaff && problemSelected">
      <cv-header-menu-item
      >
        Редактировать задачу
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="isStaff && examSelected">
      <cv-header-menu-item
      >
        Редактировать тест
      </cv-header-menu-item>
    </cv-header-nav>
    <cv-header-nav v-if="isStaff && materialSelected">
      <cv-header-menu-item
      >
        Редактировать материалы
      </cv-header-menu-item>
    </cv-header-nav>

    <template v-slot:left-panels>
      <cv-side-nav id="side-nav" fixed>
        <cv-side-nav-items>
          <cv-header-side-nav-items>
            <cv-header-menu-item
                v-if="courseSelected"
            >
              Решения
            </cv-header-menu-item>
            <cv-header-menu-item
                v-if="isStaff && courseSelected"
            >
              Успеваемость
            </cv-header-menu-item>
            <cv-header-menu-item
                v-if="lessonSelected"
            >
              Успеваемость урока
            </cv-header-menu-item>
            <cv-header-menu-item
                v-if="isStaff && courseSelected"
            >
              Календарь
            </cv-header-menu-item>
            <cv-header-menu-item
                v-if="isStaff && courseSelected && !lessonSelected && !problemSelected"
            >
              Редактировать курс
            </cv-header-menu-item>
            <cv-header-menu-item
                v-if="isStaff && lessonSelected && !problemSelected && !materialSelected && !examSelected"
            >
              Редактировать урок
            </cv-header-menu-item>
            <cv-header-menu-item
                v-if="isStaff && problemSelected"
            >
              Редактировать задачу
            </cv-header-menu-item>
            <cv-header-menu-item
            >
              Редактировать тест
            </cv-header-menu-item>
            <cv-header-menu-item
                v-if="isStaff && materialSelected"
            >
              Редактировать материалы
            </cv-header-menu-item>
          </cv-header-side-nav-items>
        </cv-side-nav-items>
      </cv-side-nav>
    </template>
    <template v-slot:header-global>
      <cv-header-global-action aria-label="Notifications"
                               aria-controls="notifications">
        <notification-20/>
      </cv-header-global-action>
      <cv-header-global-action aria-label="User avatar"
                               aria-controls="account">
        <user-avatar-20/>
      </cv-header-global-action>
    </template>

    <template v-slot:right-panels>
      <cv-header-panel class="" id="account" :expanded="false">
        <UserView :userProp="userStore.user" class="user-view"/>
        <cv-switcher>
          <cv-switcher-item>
            <cv-switcher-item-link :to="{
                  name: 'profile-page',
                  params:  { userId: userStore.user.id }
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
          <cv-switcher-item>
            <cv-switcher-item-link @click="logout"> Выйти </cv-switcher-item-link>
          </cv-switcher-item>
        </cv-switcher>
        <cv-toggle class="toggle-theme" label="Тема" value="" v-model="currentTheme">
          <template v-slot:text-left>
            <component :is="iconLight"></component>
          </template>
          <template v-slot:text-right>
            <component :is="iconDark"></component>
          </template>
        </cv-toggle>
      </cv-header-panel>
    </template>

<!--    <template v-slot:right-panels>-->
<!--      <cv-header-panel class="" id="notifications">-->
<!--        <span class="acc_text">Оповещения</span>-->
<!--        <cv-switcher>-->
<!--          <template>-->
<!--            <cv-switcher-item>-->
<!--              <cv-switcher-item-link to="/">-->
<!--                <cv-toast-notification-->
<!--                    caption="текст оповещения"-->
<!--                    kind="info"-->
<!--                    title="тестовое уведомление"/>-->
<!--              </cv-switcher-item-link>-->
<!--            </cv-switcher-item>-->
<!--          </template>-->
<!--        </cv-switcher>-->
<!--      </cv-header-panel>-->
<!--    </template>-->
  </cv-header>
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
import {useTokenStore} from "@/stores/modules/token";
import {THEMES} from '@/utils/consts'
import {useRoute} from 'vue-router'
import {computed, ref, watch} from "vue";


const iconLight = Light20;
const iconDark = Asleep20;
const themes = THEMES;

const userStore = useUserStore();
const tokenStore = useTokenStore();

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
  console.log(userStore.user)
  return userStore.user.staff_for.includes(Number(route.params.courseId));
})

</script>

<style scoped lang="stylus">

.lms
  padding-left 5px

.acc_text
  margin: 32px 1rem 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid #525252;

.user-view
  padding-left 30px;
  padding-top 10px;

.toggle-theme
  position absolute
  bottom 0
  margin 0.5rem
</style>
