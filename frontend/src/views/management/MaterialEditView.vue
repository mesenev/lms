<template>
  <div class="bx--grid">
    <div class="bx--row">
      <!--Todo: сделать нормальную верстку-->
      <h1>Редактирование материала</h1>
      <div class="bx--col-lg-16">
        <cv-inline-notification
        v-if="showNotification"
        @close="hideSuccess"
        :kind="notificationKind"
        :sub-title="notificationText"
        />
      </div>
      <div class="bx--col-lg-10"></div>
      <div class="less bx--col-lg-8">
        <label>
          <input :class="`bx--text-input`" type="text" v-model="materialEdit.name">
        </label>
        <cv-text-area style="height: auto;" v-model="materialEdit.content"></cv-text-area>
      </div>
      <div class="less bx--col-lg-8">
        <markdown-it-vue class="md-body" :content="materialEdit.content"/>
      </div>
      <cv-button class="change__btn" :disabled="canChangeMaterial" @click="ChangeMaterial">
        Изменить
      </cv-button>
    </div>
  </div>
</template>


<script lang="ts">
import LessonContent from "@/models/LessonContent";
import MarkdownItVue from 'markdown-it-vue'
import 'markdown-it-vue/dist/markdown-it-vue.css'
import materialStore from "@/store/modules/material";
import axios from "axios";
import _ from 'lodash';
import { Component, Prop } from 'vue-property-decorator';
import Vue, { VueConstructor } from 'vue';

@Component({ components: { MarkdownItVue: MarkdownItVue as VueConstructor<Vue> } })
export default class MaterialEditView extends Vue {
  @Prop() materialId!: number;
  private materialStore = materialStore;
  material: LessonContent = {
    id: NaN,
    lesson: NaN,
    name: '',
    content_type: '',
    content: '',
  }
  materialEdit: LessonContent = {...this.material}
  showNotification = false;
  notificationKind = 'success';
  notificationText = '';

  hideSuccess() {
    this.showNotification = false;
  }

  async created() {
    const material = await this.materialStore.fetchMaterialById(this.materialId);
    if (material) {
      this.materialStore.setCurrentMaterial(material);
      this.material = this.materialStore.currentMaterial;
      this.materialEdit = { ...this.material }
    }
  }

  get materials(): LessonContent {
    return this.material;
  }

  get canChangeMaterialName() {
    return this.materials.name === this.materialEdit.name;
  }

  get canChangeMaterial(): boolean {
    return _.isEqual(this.materials, this.materialEdit)
  }

  ChangeMaterial() {
    const request = axios.patch(`http://localhost:8000/api/material/${this.materialEdit.id}/`, this.materialEdit);
    request.then(() => {
      this.notificationKind = 'success';
      this.notificationText = 'Материалы успешно изменены';
      console.log(this.materialEdit);
    });
    request.catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.notificationKind = 'error';
    })
    request.finally(() => this.showNotification = true);
  }

}
</script>

<style scoped lang="stylus">
.less {
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)
  height auto
}

textarea,
#editor div {
  display: inline-block;
  width: 600px;
  height: 500px;
  vertical-align: top;
  box-sizing: border-box;
  padding: 0 20px;
}

textarea {
  background-color: #f6f6f6;
  font-size: 14px;
  font-family: "Monaco", courier, monospace;
  padding: 20px;
}

code {
  color: #f66;
}

</style>
