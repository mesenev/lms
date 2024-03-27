<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col links">
        <div>
          <cv-skeleton-text v-if="loading"/>
          <div v-else>
            <h2>Регистрация на курс {{ currentCourse && currentCourse.name || '' }},
              <span v-if="currentCourse && currentCourse.author">преподаватель курса: {{ currentCourse.author.first_name }} {{ currentCourse.author.last_name }}.</span>
            </h2>
          </div>
          <div v-if="is_possible" style="display:flex; flex-direction: column; align-items: center">
            <h3>Нажав кнопку вы будете зарегистрированы на данный курс.</h3>
            <cv-inline-notification
              v-if="showNotification"
              :kind="notificationKind"
              :sub-title="notificationText"
              @close="hideNotification"/>
            <div class="buttons">
              <cv-button-skeleton v-if="registrationProcess"/>
              <cv-button v-else
                         :icon="Education16"
                         kind="secondary"
                         @click="registration">
                Зарегистрироваться
              </cv-button>
            </div>
          </div>
          <div v-if="!is_possible">
            <div v-if="student_registered" class="warningtxt">
              <h3> Вы уже зарегистрированы на данном курсе как студент. </h3>
            </div>
            <div v-else-if="teacher_registered" class="warningtxt">
              <h3> Вы уже зарегистрированы на данном курсе как преподаватель. </h3>
            </div>
            <div v-else-if="!usages_available" class="warningtxt">
              <h3> Данная ссылка более недействительна. Обратитесь к преподавателю курса.</h3>
            </div>
            <div class="buttons">
              <router-link to="/">
                <cv-button :icon="Home16" kind="secondary"> На главную</cv-button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import Home16 from '@carbon/icons-vue/lib/home/16';
import Education16 from '@carbon/icons-vue/lib/education/16';
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import { onMounted, ref, computed } from "vue";
import type { CourseModel } from "@/models/CourseModel";
import api from "@/stores/services/api";
import type { UserModel } from "@/models/UserModel";
import { useRouter } from "vue-router";
import type { GroupModel } from "@/models/GroupModel";
import useCourseStore from "@/stores/modules/course";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  linkProp: { type: String, required: true }
})

const courseStore = useCourseStore();

const router = useRouter();

const course = ref<CourseModel>({ ...courseStore.newCourse });
const group = ref<GroupModel | null>(null);
const loading = ref(true);
const is_possible = ref(false);
const student_registered = ref(false);
const usages_available = ref(false);
const teacher_registered = ref(false);
const registrationProcess = ref(false);

onMounted(async () => {
  await statusSetup();
  course.value = await courseStore.fetchCourseById(group.value!.course);
  loading.value = false;
})

const currentCourse = computed((): CourseModel | null => {
  return course.value;
})

async function statusSetup() {
  await api.get<{
    is_possible: boolean; usages_available: boolean; student_registered: boolean;
    teacher_registered: boolean; group: GroupModel; user: UserModel;
  }>(`/api/check-link/${props.linkProp}/`)
    .then(result => {
      is_possible.value = result.data.is_possible;
      usages_available.value = result.data.usages_available;
      student_registered.value = result.data.student_registered;
      teacher_registered.value = result.data.teacher_registered;
      group.value = result.data.group;
    })
    .catch(error => {
      notificationKind.value = 'error';
      notificationText.value = `Произошла ошибка при проверке возможности` +
        ` регистрации на курс. ${error.message}`;
      showNotification.value = true;
    })
}

async function registration() {
  registrationProcess.value = true;
  await api.get(`/api/group-registration/${props.linkProp}/`)
    .then(result => {
      router.push({
        name: 'CourseView',
        params: { courseId: result.data.courseId },
      })
      registrationProcess.value = false;
    }).catch(error => {
        notificationKind.value = 'error';
        notificationText.value = `Произошла ошибка при регистрации на курс. ${error.message}`;
        showNotification.value = true;
      },
    )
}


</script>

<style scoped lang="stylus">
.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.links
  color var(--cds-text-01)
  text-align: center
  display: flex
  justify-content: center
  align-items center
  height: 400px
  padding: 20px

.item
  min-height 85px

.buttons
  padding: 20px

.warningtxt
  font-style italic

</style>
