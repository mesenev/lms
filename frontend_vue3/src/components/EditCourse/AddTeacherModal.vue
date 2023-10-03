<template>
  <div>
    <cv-button class="change-btn" kind="secondary" @click="showModal">
      Добавить преподавателей в курс
    </cv-button>
    <cv-modal :visible="modalVisible"
              class="add_lesson_modal"
              :disableTeleport="true"
              @modal-hidden="modalHidden"
              @secondary-click="() => {}">
      <template v-slot:title>
        <h3>Выбор преподавателей</h3>
      </template>
      <template v-slot:content>
        <cv-inline-notification
            v-if="showNotification"
            :kind="notificationKind"
            :sub-title="notificationText"
            @close="hideNotification"
        />
        <cv-structured-list>
          <template v-slot:headings>
            <cv-structured-list-heading>
              <cv-search
                  label="label"
                  placeholder="Введите почту прeподавателя"
                  v-model:value.trim="searchValue"/>
            </cv-structured-list-heading>
            <cv-structured-list-heading>
              <div class="list-headings">
                <cv-button
                    class="heading-btn"
                    :disabled="teacherNotPicked"
                    @click="addStuff()">
                  Добавить
                </cv-button>
              </div>
            </cv-structured-list-heading>
          </template>
          <template v-slot:items>
            <cv-structured-list-item v-for="k in teachersList" :key="k.id" checked>
              <cv-structured-list-data>
                {{ k.first_name + " " + k.last_name }}
              </cv-structured-list-data>
              <cv-structured-list-data>
                <cv-checkbox
                    class="list-checkbox"
                    value="value"
                    @click="actionSelected(k)">
                </cv-checkbox>
              </cv-structured-list-data>
            </cv-structured-list-item>
          </template>
        </cv-structured-list>
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts" setup>
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import { computed, ref, watch } from "vue";
import useUserStore from "@/stores/modules/user";
import type { UserModel } from "@/models/UserModel";
import api from "@/stores/services/api";
import { TEACHER } from "@/utils/consts";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  courseId: { type: Number, required: true }
})

const searchValue = ref("");
const userStore = useUserStore();
const teachersArray = ref<UserModel[]>([]);
const pickedTeachers = ref<Set<UserModel>>(new Set<UserModel>());
const modalVisible = ref(false);
const teacherNotPicked = ref(true);

const breakFlag = ref(false);

watch(() => searchValue.value, async (val: string) => {
  if (val.length >= 4) {
    await api.get(
        '/api/users/', { params: { email__icontains: searchValue.value, group: TEACHER } },
    ).then(response => {
          teachersArray.value = response.data;
          pickedTeachers.value.clear();
          teacherNotPicked.value = true;
        },
    ).catch(error => {
      console.log(error);
    })
  } else if (val.length === 0) {
    teachersArray.value = [];
    pickedTeachers.value.clear();
    teacherNotPicked.value = true;
  }
})

const teachersList = computed(() => {
  return teachersArray.value.filter(x => !x.staff_for.includes(props.courseId));
})

function showModal() {
  modalVisible.value = true;
}

function modalHidden() {
  modalVisible.value = false;
}

function isAnyTeacherPicked() {
  teacherNotPicked.value = pickedTeachers.value.size <= 0;
}

function setNotificationText() {
  if (pickedTeachers.value.size > 1) {
    notificationText.value = "Преподаватели успешно добавлены"
  } else {
    notificationText.value = "Преподаватель успешно добавлен"
  }
}

//ToDo: do it without flag
async function addStuff() {
  breakFlag.value = false;
  for (const teacher of pickedTeachers.value) {
    if (breakFlag.value)
      break;
    await api.post(`/api/course/${props.courseId}/assign-teacher/`, { id: teacher.id })
        .then(response => {
          notificationKind.value = 'success';
          setNotificationText();
          showNotification.value = true;
          teacher.staff_for.push(props.courseId);
          pickedTeachers.value.delete(teacher);
          isAnyTeacherPicked();
        })
        .catch(error => {
          notificationKind.value = 'error';
          notificationText.value = `Что-то пошло не так: ${error.message}`;
          showNotification.value = true;
          breakFlag.value = true;
        });
  }
}

function actionSelected(user: UserModel) {
  if (pickedTeachers.value.has(user)) {
    pickedTeachers.value.delete(user);
  } else {
    pickedTeachers.value.add(user);
  }
  isAnyTeacherPicked();
}
</script>

<style lang="stylus" scoped>
.list-headings
  width 5rem

.list-checkbox
  display flex
  flex-direction row
  justify-content center

.bx--modal-content:focus
  outline none

.lesson_list
  margin-bottom 0

.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)

.switcher
  margin-bottom: 5px

.add_lesson_modal .bx--modal-container
  height 75vh

.add_lesson_modal .bx--modal-footer
  height 3.5rem

.add_lesson_modal .bx--btn
  height 3rem
  border none

  &:hover, &:active, &:focus
    outline none
    box-shadow none
    border none

.modal--content
  height 500px
</style>
