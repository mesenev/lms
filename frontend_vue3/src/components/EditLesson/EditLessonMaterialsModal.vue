<template>
  <div>
    <cv-button class="change-btn" @click="showModal">
      Материалы
    </cv-button>
    <cv-modal class="add_lesson_modal"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              :primary-button-disabled="isButtonDisabled"
              @primary-click="addMaterial"
              @secondary-click="() => {}">
      <template v-slot:label>{{ lesson.name }}</template>
      <template v-slot:title>
        Добавить материалы
      </template>
      <template v-slot:content>
        <section class="modal--content">
          <div class="materials-header">
            <cv-text-input label="Название материала"
                           @focus="invalidMessageHidden"
                           v-model.trim="currentMaterial.name">
              <template v-if="invalidMessageVisible && !currentMaterial.name"
                        v-slot:invalid-message>
                {{ emptyInvalidMessage }}
              </template>
              <template v-if="invalidMessageVisible && areSameMaterialNames(currentMaterial.name)"
                        v-slot:invalid-message>
                {{ invalidMessage }}
              </template>
            </cv-text-input>
            <cv-dropdown class="material-type-dropdown"
                         placeholder="Выберите тип"
                         label="Тип материала"
                         v-model:value="currentMaterial.content_type">
              <cv-dropdown-item value="text">Текст</cv-dropdown-item>
              <cv-dropdown-item value="url">Ссылка</cv-dropdown-item>
              <cv-dropdown-item value="video">Видео</cv-dropdown-item>
              <template v-slot:invalid-message
                        v-if="invalidMessageVisible && !currentMaterial.content_type">
                {{ emptyInvalidMessage }}
              </template>
            </cv-dropdown>
          </div>
          <br>
          <p class="materials-info">
            Добавление содержимого в материал доступно в редактировании.
          </p>
          <h5 class="materials-title" v-if="materials.length">Материалы урока:</h5>
          <cv-inline-notification
            v-if="showNotification"
            @close="() => showNotification=false"
            kind="error"
            :sub-title="notificationText"
          />
          <div class="materials-list-container" v-if="materials.length">
            <cv-structured-list class="materials-list">
              <template v-slot:items>
                <cv-structured-list-item
                  v-for="material in materials"
                  :key="material.id"
                >
                  <material-list-component :material-prop="material"
                                           :is-staff="isStaff"
                                           @modal-hidden="modalHidden"/>
                </cv-structured-list-item>
              </template>
            </cv-structured-list>
          </div>
          <empty-list-component v-else
                                class="empty-list"
                                :text="emptyMaterialsListText"
                                list-of="materials"/>
        </section>
      </template>
      <template v-slot:primary-button>
        Добавить материал
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts" setup>
import AddAlt20 from '@carbon/icons-vue/es/add--alt/20';
import SubtractAlt20 from '@carbon/icons-vue/es/subtract--alt/20';
import type { PropType } from "vue";
import type { LessonModel } from "@/models/LessonModel";
import useMaterialStore from "@/stores/modules/material";
import useUserStore from "@/stores/modules/user";
import { computed, ref } from "vue";
import type { MaterialModel } from "@/models/MaterialModel";
import api from "@/stores/services/api";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import { useRoute } from "vue-router";
import MaterialListComponent from "@/components/lists/MaterialListComponent.vue";
import EmptyListComponent from "@/components/lists/EmptyListComponent.vue";

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  _lesson: {type: Object as PropType<LessonModel>, required: true}
})

const route = useRoute();

  const lesson = ref<LessonModel>(props._lesson)
  const materialStore = useMaterialStore();
  const userStore = useUserStore();
  const currentMaterial = ref<MaterialModel>({ ...materialStore.getNewMaterial, lesson: lesson.value.id });
  const creationLoader = ref(false);
  const modalVisible = ref(false);
  const searchQueryForAllMaterials = ref('');
  const invalidMessageVisible = ref(false);
  const invalidMessage = 'Материал с таким названием уже существует!';
  const emptyInvalidMessage = 'Заполните поле!';
  const emptyMaterialsListText = 'Добавьте новый материал.';

  const materials = computed((): Array<MaterialModel> => {
    if (lesson.value)
      return [...materialStore.materials[lesson.value.id]].sort(
        (a, b) => {
          return (a.is_teacher_only === b.is_teacher_only ? 0 : b.is_teacher_only ? -1 : 1) || a.id - b.id;
        }
      );
    return [];
  })

  function showModal() {
    modalVisible.value = true;
    currentMaterial.value = { ...materialStore.getNewMaterial, lesson: lesson.value.id };
  }

  function modalHidden() {
    modalVisible.value = false;
  }

  function invalidMessageHidden() {
    if (areSameMaterialNames(currentMaterial.value.name))
      invalidMessageVisible.value = false;
  }

  async function addMaterial() {
    if (areSameMaterialNames(currentMaterial.value.name)
      || !currentMaterial.value.name
      || !currentMaterial.value.content_type) {
      invalidMessageVisible.value = true;
      return;
    }
    creationLoader.value = true;
    await createNewMaterial();
    creationLoader.value = false;
    if (materials.value.every((l) => l.name)) {
      // this.lessons.forEach((lesson) => this.lessonStore.addLessonToCourse(lesson));
      // this.lessons = [];
    }
  }

  async function createNewMaterial() {
    if (currentMaterial.value.content_type === 'text')
      currentMaterial.value.content = "### материал"
    const request = api.post('/api/material/', currentMaterial.value);
    request.then(response => {
      lesson.value.materials.push(response.data as MaterialModel);
      materialStore.setMaterials({ [lesson.value.id]: lesson.value.materials });
    });
    request.catch(error => {
      notificationKind.value = 'error';
      notificationText.value = `Что-то пошло не так: ${error.message}`;
      showNotification.value = true;
    });
    request.finally(() => {
      invalidMessageHidden();
    })
  }

  const isStaff = computed(() => {
    return userStore.user.staff_for.includes(Number(route.params.courseId));
  })

  const isButtonDisabled = computed(() => {
    return creationLoader.value;
  })

  function areSameMaterialNames(materialName: string) {
    return materials.value.filter(material => material.name === materialName).length != 0;
  }

  function sortMaterials(): Array<MaterialModel> {
    return materialStore.materials[lesson.value.id].sort(
        (a, b) => {
          return (a.is_teacher_only === b.is_teacher_only ? 0 : b.is_teacher_only ? -1 : 1) || a.id - b.id;
        }
      );
  }

</script>

<style scoped lang="stylus">

.bx--modal-content:focus
  outline none

.change-btn
  background-color var(--cds-interactive-02)
  margin-left 25px

  &:hover
    border var(--cds-ui-01) 1px solid

.materials-header
  display flex
  gap 1rem
  justify-content space-between

.cv-text-input
  /deep/ .bx--label
    margin-top 3px

.material-type-dropdown
  max-width 10rem

  /deep/ .bx--dropdown__wrapper.bx--list-box__wrapper
    align-self end

/deep/ .bx--list-box__field
  display flex

.materials-info
  margin-bottom 1rem
  text-decoration-line underline

.materials-title
  margin-bottom 0.5rem

.materials-list-container
  overflow-y auto
  max-height 15rem

.materials-list
  margin-bottom 0

.empty-list
  text-align center

.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)

.add_lesson_modal .bx--modal-container
  height 75vh

.add_lesson_modal .bx--modal-footer
  height 3.5rem

.add_lesson_modal .bx--btn
  height 3rem
  border none

.add_lesson_modal .bx--btn--secondary
  background-color var(--cds-hover-secondary)

  &:hover, &:active, &:focus
    outline none
    box-shadow none
    border none

.add_lesson_modal .bx--btn--primary[disabled = disabled],
.add_lesson_modal .bx--btn--primary
  background-color var(--cds-ui-05)

.modal--content
  height 400px
</style>
