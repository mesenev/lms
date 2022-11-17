<template>
  <cv-loading v-if="loading"></cv-loading>
  <div v-else class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-9">
        <cv-tile>
          <h2 class="material-title">{{ currentMaterial.name }}</h2>
        </cv-tile>
        <div v-if="isMaterialAVideo" class="video material-content-video">
          <youtube v-if="currentMaterial.content" :video-id="youTubeGetID"
                   ref="youtube"
                   player-width="640"
                   player-height="360"></youtube>
        </div>
        <div v-else class="less material-content">
          <vue-markdown :source="currentMaterial.content" class="md-body"/>
        </div>
      </div>
      <div class="bx--col-lg-3 bx--col-md-4">
        <div class="other-materials-container">
          <div class="other-materials">
            <h4 class="other-materials-title">Другие материалы:</h4>
            <div class="other-materials-list-container" v-if="otherMaterials.length">
              <cv-structured-list class="other-materials-list">
                <template slot="items">
                  <cv-structured-list-item
                    v-for="material in otherMaterials"
                    :key="material.id"
                  >
                    <material-list-component :material-prop="material"/>
                  </cv-structured-list-item>
                </template>
              </cv-structured-list>
            </div>
            <h5 v-else class="empty-other-materials-title">Это единственный материал!</h5>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import MaterialModel from '@/models/MaterialModel';
import materialStore from '@/store/modules/material';
import VueMarkdown from 'vue-markdown-render';
import { Component, Prop, Vue } from 'vue-property-decorator';
import VueYouTubeEmbed from 'vue-youtube-embed';
import { getIdFromURL } from "vue-youtube-embed";
import MaterialListComponent from "@/components/lists/MaterialListComponent.vue";

//TODO: check this is ok
Vue.use(VueYouTubeEmbed);

@Component({ components: { VueMarkdown, MaterialListComponent } })
export default class MaterialView extends Vue {
  @Prop({ required: true }) materialId!: number;
  private materialStore = materialStore;
  materials: Array<MaterialModel> = [];
  loading = true;

  async created() {
    const material = await this.materialStore.fetchMaterialById(this.materialId);
    if (material.id) {
      this.materialStore.setCurrentMaterial(material);
      this.materials = await this.materialStore.fetchMaterialsByLessonId(material.lesson);
      this.loading = false;
    }
  }

  get materialUrl() {
    if (this.materialStore.currentMaterialUrl != null)
      return this.materialStore.currentMaterialUrl;
  }

  get youTubeGetID() {
    // const VID_REGEX = (/(?:youtube(?:-nocookie)?\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/)
    // return (this.materialUrl!.match(VID_REGEX)![1]);
    return getIdFromURL(this.currentMaterial.content);
  }

  get isMaterialAVideo() {
    if (this.materialStore.currentMaterialType === 'video')
      return true;
  }

  get currentMaterial(): MaterialModel {
    return this.materialStore.currentMaterial;
  }

  get otherMaterials(): Array<MaterialModel> {
    if (this.materials)
      return this.materials.filter(x => x.id != this.materialId).sort(
        (a, b) => {
          return (a.is_teacher_only === b.is_teacher_only ? 0
            : b.is_teacher_only ? -1 : 1) || a.id - b.id;
        });
    return this.materials;
  }
}
</script>

<style scoped lang="stylus">

.material-title
  margin-top 2rem

.material-content-video
  min-height 20rem
  min-width 980px

.material-content
  min-height 20rem

.less
  border .5px solid var(--cds-ui-04)
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.other-materials-container
  margin-top 4rem
  min-height 22.5rem
  background-color var(--cds-ui-background)
  border 0.5px solid var(--cds-ui-04)

.other-materials
  margin 0.5rem 1rem 1rem 1rem

.other-materials-list-container
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
