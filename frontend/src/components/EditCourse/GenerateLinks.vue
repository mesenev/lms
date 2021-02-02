<template>
<div>
  <cv-button size="field" kind="secondary" @click="createNewLink">
    Сгенерировать ссылку-приглашения
  </cv-button>
  <cv-text-input v-if="tmp > 0" :value="'11'" helper-text="Ваша ссылка:">
  </cv-text-input>
  <cv-text-input v-else :value="'Press the button'" helper-text="Ваша ссылка появится после нажатия" disabled="true">
  </cv-text-input>
</div>
</template>

<!-- TODO: get link from api -->
<script lang="ts">
import {Component, Vue, Prop} from "vue-property-decorator";
import LinkModel from "@/models/LinkModel";
import axios from 'axios';
import CourseModel from "@/models/CourseModel";

@Component({ components: {} })
export default class CourseView extends Vue {
  @Prop({ required: true }) counter!: number;
  @Prop({ required: true }) course!: CourseModel;

  async createNewLink() {
    const request = axios.post('http://localhost:8000/api/courselink/', {course: this.course.id, usages: this.counter});
    await axios.get('http://localhost:8000/api/courselink/')
      .then(response => {
        console.log(response.data)
      })
      .catch(error => {
        console.log(error);
      })
  }


}
</script>

<style scoped>

</style>
