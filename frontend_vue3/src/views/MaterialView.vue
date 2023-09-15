<template>
  <cv-loading v-if="loading"/>
  <div v-else class="bx--grid">
    <div class="bx--row header-container">
      <div class="main-title">
        <h1>{{ currentMaterial.name }}</h1>
      </div>
    </div>
    <div class="bx--row">
      <div v-if="isMaterialAVideo" class="material-content-video">
        <lite-you-tube-embed v-if="isYoutubeFormat || !currentMaterial.content"
                             :id="youTubeGetID"
                             title=""
                             ref="youtube"/>
        <lms-markdown v-else :source="currentMaterial.content" class="md-body"/>
      </div>
      <div v-else class="less material-content">
        <lms-markdown :source="currentMaterial.content" class="md-body"/>
      </div>
      <div class="bx--col-lg-3 bx--col-md-4">
        <div class="other-materials-container">
          <div class="other-materials">
            <h4 class="other-materials-title">Материалы:</h4>
            <div class="other-materials-list-container">
              <cv-structured-list class="other-materials-list">
                <template v-slot:items>
                  <cv-structured-list-item
                      v-for="material in materials"
                      :key="material.id"
                  >
                    <material-list-component :is-selected="isMaterialSelected(material.id)"
                                             :is-staff="isStaff"
                                             :material-prop="material"/>
                  </cv-structured-list-item>
                </template>
              </cv-structured-list>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import MarkdownIt from 'markdown-it';
import useMaterialStore from "@/stores/modules/material";
import useUserStore from "@/stores/modules/user";
import useLessonStore from "@/stores/modules/lesson";
import type { MaterialModel } from "@/models/MaterialModel";
import { computed, onMounted, ref } from "vue";
import MaterialListComponent from "@/components/lists/MaterialListComponent.vue";
import CvStructuredList from "@/components/CvStructuredList/CvStructuredList.vue";
import CvStructuredListItem from "@/components/CvStructuredList/CvStructuredListItem.vue";
import LmsMarkdown from "@/components/common/LmsMarkdown.vue";
import LiteYouTubeEmbed from 'vue-lite-youtube-embed'
import 'vue-lite-youtube-embed/style.css'

const props = defineProps({
  materialId: { type: Number, required: true }
})

const materialStore = useMaterialStore();
const userStore = useUserStore();
const lessonStore = useLessonStore();
const _materials = ref<Array<MaterialModel>>([]);
const loading = ref(true);

onMounted(async () => {
  const material = await materialStore.fetchMaterialById(props.materialId);
  if (material.id) {
    materialStore.setCurrentMaterial(material);
    _materials.value = await materialStore.fetchMaterialsByLessonId(material.lesson);
    loading.value = false;
  }
})

const isStaff = computed((): boolean => {
  return userStore.user.staff_for.includes(Number(lessonStore.currentLesson?.course));
})

const youTubeGetID = computed(() => {
  const regExp =
      /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;

  const match = currentMaterial.value.content.match(regExp);

  if (match && match[2].length === 11) {
    return match[2];
  }
  return '';
})

const isYoutubeFormat = computed(() => {
  return currentMaterial.value.content.includes('https://www.youtube.com/');
})

const isMaterialAVideo = computed(() => {
  return materialStore.currentMaterialType === 'video'
})

const currentMaterial = computed((): MaterialModel => {
  return materialStore.currentMaterial;
})

const materials = computed((): Array<MaterialModel> => {
  return [..._materials.value].sort(
      (a, b) => {
        return (a.is_teacher_only === b.is_teacher_only ? 0
            : b.is_teacher_only ? -1 : 1) || a.id - b.id;
      });
})

function isMaterialSelected(materialId: number) {
  return currentMaterial.value.id === materialId;
}

</script>

<style scoped lang="stylus">
/deep/ .bx--title
  background-color var(--cds-ui-background)

.material-title
  color var(--cds-text-01)
  margin-top 2rem

.material-content-video
  width 70%

.material-content
  width 70%
  min-height 20rem

.less
  color var(--cds-text-01)
  border .5px solid var(--cds-ui-04)
  background-color var(--cds-ui-01)
  padding var(--cds-spacing-05)

.other-materials-container
  padding 1rem
  color var(--cds-text-01)

.other-materials-list-container
  background-color var(--cds-ui-01)
  border 1px solid var(--cds-ui-05)
  max-height 18rem
  overflow-y auto

.other-materials-list
  margin-bottom 0

.other-materials-title
  margin-bottom 1rem

.empty-other-materials-title
  text-align center

code
  color: var(--color-b)


</style>

<style lang="sass">
.md-body img
  max-width: 100%
  height: auto
</style>
