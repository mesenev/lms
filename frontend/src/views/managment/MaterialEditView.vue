<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <h1 class="main-title">Редактирование материала</h1>
      <div class="material-hide-button-container">
        <cv-button-skeleton v-if="changingVisibility || loading" kind="ghost"/>
        <cv-button v-else
                   class="material-hide-button"
                   :icon="hiddenIcon"
                   kind="ghost"
                   @click="changeMaterialVisibility">
          {{
            (currentMaterial.is_teacher_only) ?
                "Материал скрыт" : "Материал открыт"
          }}
        </cv-button>
      </div>
    </div>
    <cv-loading v-if="loading"/>
    <div v-else class="bx--row content">
      <div class="edit-container-wrapper bx--col-lg-5">
        <confirm-modal :modal-trigger="confirmModalTrigger"
                       :text="approvedText"
                       :approve-handler="deleteHandler"/>
        <div class="edit-container">
          <cv-inline-notification
              v-if="showNotification"
              :kind="notificationKind"
              :sub-title="notificationText"
              @close="hideSuccess"
          />
          <div class="edit-container-header">
            <cv-text-input label="Заголовок"
                           type="text"
                           v-model="materialEdit.name"/>
            <cv-dropdown class="material-type-dropdown"
                         @change="changeMaterialContent"
                         placeholder="Выберите тип"
                         label="Тип материала"
                         v-model:value="materialEdit.content_type">
              <cv-dropdown-item value="text">Текст</cv-dropdown-item>
              <cv-dropdown-item value="url">Ссылка</cv-dropdown-item>
              <cv-dropdown-item value="video">Видео</cv-dropdown-item>
            </cv-dropdown>
          </div>
          <cv-text-area v-if="isTextType"
                        label="Содержимое"
                        class="text-area"
                        v-model="materialEdit.content"/>
          <cv-text-input v-if="isUrlType"
                         placeholder="Вставьте ссылку"
                         label="Ссылка"
                         v-model="materialEdit.content"/>
          <cv-text-input v-if="isVideoType"
                         placeholder="Вставьте ссылку на видео или добавьте вложение"
                         label="Видео"
                         v-model="materialEdit.content"/>
          <p class="attachments-list-label">Вложения</p>
          <div class="attachments-list-container">
            <cv-structured-list class="attachments-list">
              <template v-slot:items>
                <cv-structured-list-item class="attachments-list-item"
                                         v-for="element in currentAttachments"
                                         :key="element.id">
                  <attachments-component-list :attachment="element"
                                              @show-confirm-modal="showConfirmModal">
                  </attachments-component-list>
                </cv-structured-list-item>
              </template>
            </cv-structured-list>
          </div>
          <input type="file"
                 id="files_input"
                 ref="files"
                 multiple
                 :disabled="attachmentLoading"
                 @change="uploadFiles($event)"/>
          <div class="action-btns">
            <cv-button kind="danger" @click="showConfirmModal(material)">
              Удалить
            </cv-button>
            <cv-button :disabled="canChangeMaterial"
                       @click="ChangeMaterial">
              Изменить
            </cv-button>
          </div>
        </div>
      </div>
      <div class="preview-container bx--col-lg-6">
        <h4 class="title" v-if="materialEdit.name.length > 0"> {{ materialEdit.name }} </h4>
        <h4 v-else>Введите название материала</h4>
        <lite-you-tube-embed v-if="isVideoType && isYoutubeFormat" :id="youtubeId"
                             ref="youtube"
                             title=""/>
        <lms-markdown v-else :source="materialEdit.content" class="markdown"/>
      </div>
    </div>
  </div>
</template>


<script lang="ts" setup>
import _ from 'lodash';
import viewOff from '@carbon/icons-vue/es/view--off/32';
import view from '@carbon/icons-vue/es/view/32';
import useMaterialStore from "@/stores/modules/material";
import {type Ref, computed, onMounted, ref } from "vue";
import type { MaterialModel } from "@/models/MaterialModel";
import useNotificationMixin from "@/components/common/NotificationMixinComponent.vue";
import type { AttachmentModel } from "@/models/Attachment";
import api from "@/stores/services/api";
import { useRouter } from "vue-router";
import ConfirmModal from "@/components/ConfirmModal.vue";
import AttachmentsComponentList from "@/components/lists/AttachmentsComponentList.vue";
import LmsMarkdown from "@/components/common/LmsMarkdown.vue";
import LiteYouTubeEmbed from 'vue-lite-youtube-embed'
import 'vue-lite-youtube-embed/style.css'

const { notificationText, notificationKind, showNotification, hideNotification } = useNotificationMixin();

const props = defineProps({
  materialId: { type: String, required: true }
})

const router = useRouter();

const materialStore = useMaterialStore();
const material = ref<MaterialModel>({
  id: NaN,
  lesson: NaN,
  name: '',
  content_type: '',
  content: '',
  is_teacher_only: false,
})

const materialId = ref<number>(parseInt(props.materialId));
const materialEdit = ref<MaterialModel>({ ...material.value })
const loading = ref(true);
const confirmModalTrigger = ref(false);
const approvedText = ref('');
const deletingValueId = ref<number | null>(null);
const attachmentLoading = ref(false);
const changingVisibility = ref(false);
const file: Ref<File | null> = ref(null);

function hideSuccess() {
  showNotification.value = false;
}

onMounted(async () => {
  const _material = await materialStore.fetchMaterialById(materialId.value);
  await materialStore.fetchAttachmentsByMaterialId(materialId.value);
  if (_material) {
    materialStore.setCurrentMaterial(_material);
    await materialStore.fetchMaterialsByLessonId(_material.lesson);
    material.value = materialStore.currentMaterial;
    materialEdit.value = _.cloneDeep(material.value)
  }
  loading.value = false;
})

async function uploadFiles(event: Event) {
  attachmentLoading.value = true;
  const fileList = (event.target as HTMLInputElement).files
  if (fileList) {
    for (const element of fileList) {
      const reader = new FileReader();
      reader.readAsDataURL(element);
      reader.onload = async () => {
        const encodedFile = (<string>reader.result).split(",")[1];
        const data = new FormData()
        data.append('id', '-1');
        data.append('name', element.name);
        data.append('material', material.value.id.toString());
        data.append('file_url', encodedFile);
        data.append('file_format', element.type);

        await materialStore.createAttachment(data).catch(error => {
          notificationKind.value = 'error';
          notificationText.value = `Что-то пошло не так: ${error.message}`;
          showNotification.value = true;
        })
      }
    }
    await updateAttachments();
    const input = window.document.getElementById('files_input') as HTMLInputElement
    input.value = '';
    attachmentLoading.value = false;
  }
}

const currentMaterial = computed((): MaterialModel => {
  return materialStore.currentMaterial;
})

const currentAttachments = computed((): Array<AttachmentModel> => {
  return materialStore.currentAttachments;
})

const isMaterialEmpty = computed((): boolean => {
  return materialEdit.value.name.length === 0 || materialEdit.value.content.length === 0;
})

const isTextType = computed(() => {
  return materialEdit.value.content_type === 'text';
})

const isUrlType = computed(() => {
  return materialEdit.value.content_type === 'url';
})

const isVideoType = computed(() => {
  return materialEdit.value.content_type === 'video';
})

const isYoutubeFormat = computed(() => {
  return materialEdit.value.content.includes('https://www.youtube.com/');
})

const youtubeId = computed(() => {
  const regExp =
      /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;

  const match = materialEdit.value.content.match(regExp);

  if (match && match[2].length === 11) {
    return match[2];
  }

  return '';
})

const canChangeMaterial = computed((): boolean => {
  return _.isEqual(currentMaterial.value, materialEdit.value) || isMaterialEmpty.value
})

const hiddenIcon = computed(() => {
  return (currentMaterial.value.is_teacher_only) ? viewOff : view;
})

function determineIsAttachmentOrMaterial(model: AttachmentModel | MaterialModel): model is AttachmentModel {
  return (model as AttachmentModel).file_url !== undefined;
}

function showConfirmModal(deletingValue: AttachmentModel | MaterialModel) {
  let deletingText = 'Удалить материал: ';
  if (determineIsAttachmentOrMaterial(deletingValue)) {
    deletingText = 'Удалить вложение: ';
  }
  deletingValueId.value = deletingValue.id;
  approvedText.value = `${deletingText}${deletingValue.name}`;
  confirmModalTrigger.value = !confirmModalTrigger.value;
}

function changeMaterialContent() {
  if (isTextType.value) {
    materialEdit.value.content = '### материал';
  } else {
    materialEdit.value.content = '';
  }
}

async function changeMaterialVisibility() {
  changingVisibility.value = true;
  await materialStore.patchMaterialVisibility({
    is_teacher_only: !currentMaterial.value.is_teacher_only,
    id: currentMaterial.value.id
  }).then(() => {
    updateAfterChangeMaterials(currentMaterial.value, currentMaterial.value);
    materialEdit.value.is_teacher_only = currentMaterial.value.is_teacher_only;
  })
  changingVisibility.value = false;
}

async function ChangeMaterial() {
  await api.patch(`/api/material/${materialEdit.value.id}/`, materialEdit.value)
      .then(response => {
        notificationKind.value = 'success';
        notificationText.value = 'Материалы успешно изменены';
        updateAfterChangeMaterials(material.value, materialEdit.value);
        material.value = response.data;
        materialStore.setCurrentMaterial(material.value);
      })
      .catch(error => {
        notificationText.value = `Что-то пошло не так: ${error.message}`;
        notificationKind.value = 'error';
      })
      .finally(() => showNotification.value = true);
}

async function deleteHandler() {
  if (approvedText.value.includes('материал')) {
    await deleteMaterial();
  } else {
    await deleteAttachment();
  }
}

async function deleteAttachment() {
  if (!deletingValueId.value)
    throw Error;
  await materialStore.deleteAttachment(deletingValueId.value)
      .catch(error => {
        notificationKind.value = 'error';
        notificationText.value = `Что-то пошло не так: ${error.message}`
        showNotification.value = true;
      })
}

async function deleteMaterial() {
  if (!deletingValueId.value)
    throw Error;
  await api.delete(`/api/material/${deletingValueId.value}/`)
      .then(async () => {
        await updateAfterDeleteMaterials();
        await router.push({
          name: 'LessonView',
          params: { lessonId: material.value.lesson.toString() }
        })
      })
      .catch(error => {
        notificationKind.value = 'error';
        notificationText.value = `Что-то пошло не так: ${error.message}`;
        showNotification.value = true;
      })
}

async function updateAttachments() {
  await materialStore.fetchAttachmentsByMaterialId(materialId.value);
}

async function updateAfterDeleteMaterials() {
  const materials = await materialStore.fetchMaterialsByLessonId(currentMaterial.value.lesson);
  materialStore.setMaterials({
    [currentMaterial.value.lesson]: materials.filter(
        x => x.id !== currentMaterial.value.id
    )
  });
}

async function updateAfterChangeMaterials(oldMaterial: MaterialModel, newMaterial: MaterialModel) {
  let materials = await materialStore.fetchMaterialsByLessonId(oldMaterial.lesson);
  materials = materials.filter(x => x.id !== oldMaterial.id);
  materials.push(newMaterial);
  materials.sort((a, b) => a.id - b.id);
  materialStore.setMaterials({ [newMaterial.lesson]: materials });
}

</script>

<style scoped lang="stylus">
.material-hide-button-container
  margin-left 1rem

.preview-container
  padding 1rem
  color var(--cds-text-01)
  background-color var(--cds-ui-01)
  border 2px black solid

.markdown
  overflow-wrap break-word
  margin-top 10px
  overflow-y auto
  max-height 40rem

.title
  overflow-wrap break-word

.content
  margin-top 1rem

.edit-container
  padding 1rem
  background-color var(--cds-ui-01)

.edit-container-header
  display flex
  gap 1rem
  justify-content space-between

.cv-text-input
  /deep/ .bx--label
    margin-top 2px

.material-type-dropdown
  max-width 10rem

  /deep/ .bx--dropdown
    background-color var(--cds-ui-background)

  /deep/ .bx--dropdown__wrapper.bx--list-box__wrapper
    align-self end

/deep/ .bx--list-box__field
  display flex

/deep/ .bx--text-input
  margin-bottom 1rem
  background-color var(--cds-ui-background)

.text-area >>> .bx--text-area
  background-color var(--cds-ui-background)
  min-height 13rem
  resize none
  margin-bottom 1rem

#files_input
  color var(--cds-text-01)

.action-btns
  display flex
  justify-content space-between
  margin-top 1rem

.attachments-list-label
  font-size var(--cds-label-01-font-size, 0.75rem)
  font-weight var(--cds-label-01-font-weight, 400)
  line-height var(--cds-label-01-line-height, 1.34)
  letter-spacing var(--cds-label-01-letter-spacing, 0.32px)
  display: inline-block
  margin-bottom 0.5rem
  color: var(--cds-text-02, #525252)
  vertical-align baseline

.attachments-list-container
  overflow auto
  max-height 200px
  margin-bottom 0.5rem
  color var(--cds-text-01)

.attachments-list
  margin-top 1px
  margin-bottom 0

.attachments-list-item
  border-right 1px solid var(--cds-ui-03)
  border-left 1px solid var(--cds-ui-03)

code {
  color: #f66;
}

</style>