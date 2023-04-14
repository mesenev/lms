<template>
  <cv-loading v-if="loading"></cv-loading>
  <div v-else class="bx--grid">
    <div class="bx--row header-container">
      <div class="main-title">
        <h1>{{ currentMaterial.name }}</h1>
      </div>
    </div>
    <div class="bx--row">
      <div v-if="isMaterialAVideo" class="material-content-video">
        <youtube v-if="isYoutubeFormat || !currentMaterial.content"
                 :video-id="youTubeGetID"
                 ref="youtube"
                 player-width="100%"
                 player-height="540"/>
        <vue-markdown v-else :html="true" :source="currentMaterial.content" class="md-body"/>
      </div>
      <div v-else class="less material-content">
        <vue-markdown :html="true" :source="currentMaterial.content" class="md-body"/>
      </div>
      <div class="bx--col-lg-3 bx--col-md-4">
        <div class="other-materials-container">
          <div class="other-materials">
            <h4 class="other-materials-title">Материалы:</h4>
            <div class="other-materials-list-container">
              <cv-structured-list class="other-materials-list">
                <template slot="items">
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

<script lang="ts">
import MaterialModel from '@/models/MaterialModel';
import materialStore from '@/store/modules/material';
import userStore from '@/store/modules/user';
import lessonStore from '@/store/modules/lesson';
import VueMarkdown from 'vue-markdown';
import { Component, Prop, Vue } from 'vue-property-decorator';
import VueYouTubeEmbed from 'vue-youtube-embed';
import { getIdFromURL } from "vue-youtube-embed";
import MaterialListComponent from "@/components/lists/MaterialListComponent.vue";
import EmptyListComponent from "@/components/EmptyListComponent.vue";

//TODO: check this is ok
Vue.use(VueYouTubeEmbed);

@Component({ components: { EmptyListComponent, VueMarkdown, MaterialListComponent } })
export default class MaterialView extends Vue {
  @Prop({ required: true }) materialId!: number;
  private materialStore = materialStore;
  userStore = userStore;
  lessonStore = lessonStore;
  _materials: Array<MaterialModel> = [];
  loading = true;

  async created() {
    const material = await this.materialStore.fetchMaterialById(this.materialId);
    if (material.id) {
      this.materialStore.setCurrentMaterial(material);
      this._materials = await this.materialStore.fetchMaterialsByLessonId(material.lesson);
      this.loading = false;
    }
  }

  get isStaff(): boolean {
    return this.userStore.user.staff_for.includes(Number(this.lessonStore.currentLesson?.course));
  }

  get youTubeGetID() {
    // const VID_REGEX = (/(?:youtube(?:-nocookie)?\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/)
    // return (this.materialUrl!.match(VID_REGEX)![1]);
    return getIdFromURL(this.currentMaterial.content);
  }

  get isYoutubeFormat() {
    return this.currentMaterial.content.includes('https://www.youtube.com/');
  }

  get isMaterialAVideo() {
    if (this.materialStore.currentMaterialType === 'video')
      return true;
  }

  get currentMaterial(): MaterialModel {
    return this.materialStore.currentMaterial;
  }

  get materials(): Array<MaterialModel> {
    return this._materials?.sort(
      (a, b) => {
        return (a.is_teacher_only === b.is_teacher_only ? 0
          : b.is_teacher_only ? -1 : 1) || a.id - b.id;
      });
  }

  isMaterialSelected(materialId: number) {
    return this.currentMaterial.id === materialId;
  }
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
