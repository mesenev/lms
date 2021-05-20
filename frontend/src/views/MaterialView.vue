<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-16">
        <cv-tile>
          <h1 class="material-title">{{ materials.name }}</h1>
        </cv-tile>
      </div>
      <div v-if="isMaterialAVideo" class="video bx--col-lg-10">
        <youtube :video-id="getVideoId"
                 ref="youtube"
                 player-width="980"
                 player-height="480"></youtube>
      </div>
      <div v-else class="less bx--col-lg-10">
        <MarkdownItVue class="md-body" :content="materials.content"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import MaterialModel from '@/models/MaterialModel';
import materialStore from '@/store/modules/material';
import MarkdownItVue from 'markdown-it-vue'
import 'markdown-it-vue/dist/markdown-it-vue.css'
import {Component, Prop} from 'vue-property-decorator';
import Vue, {VueConstructor} from 'vue';
import VueYouTubeEmbed from 'vue-youtube-embed'

Vue.use(VueYouTubeEmbed)

@Component({components: {MarkdownItVue: MarkdownItVue as VueConstructor<Vue>}})
export default class MaterialView extends Vue {
  @Prop() materialId!: number;
  private materialStore = materialStore;
  material!: MaterialModel;


  get getVideoId() {
    return this.youTubeGetID(this.materialUrl)
  }

  async created() {
    const material = await this.materialStore.fetchMaterialById(this.materialId);
    if (material) {
      this.materialStore.setCurrentMaterial(material);
    }
  }

  get materialUrl() {
    return this.materialStore.currentMaterialUrl;
  }

  function

  youTubeGetID(url) {
    let ID = '';
    url = url.replace(/(>|<)/gi, '').split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
    if (url[2] !== undefined) {
      ID = url[2].split(/[^0-9a-z_\-]/i);
      ID = ID[0];
    } else {
      ID = url;
    }
    return ID;
  }

  get isMaterialAVideo() {
    console.log(this.materialUrl)
    if (this.materialStore.currentMaterialType === 'video')
      return true;
  }

  get materials(): MaterialModel {
    return this.materialStore.currentMaterial;
  }

}
</script>

<style scoped lang="stylus">

.material-title
  margin-top 2rem

.video
  margin-left 1rem

.less
  border .5px solid rgba(0, 0, 0, .3)
  margin-left 2rem
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)
  min-height 10rem


code
  color: var(--color-b)
</style>
