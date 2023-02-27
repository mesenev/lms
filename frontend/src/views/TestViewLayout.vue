<template>
  <transition mode="out-in" name="fade">
    <router-view v-if="test" :key="$route.params.testId"/>
    <div v-else class="loading-out">
      <cv-loading />
    </div>
  </transition>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import TestModel from "@/models/TestModel";
import testStore from '@/store/modules/test';

@Component({components: {}})
export default class TestViewLayout extends Vue {
  @Prop({required: true}) testId!: number;

  test: TestModel | null = null;
  testStore = testStore;

  async created() {
    this.testStore.changeCurrentTest(null);
    this.test = await this.testStore.fetchTestById(this.testId);
    this.testStore.changeCurrentTest(this.test);
    await this.testStore.fetchTestsByLessonId(this.test.lesson);
    console.log(this.test);
  }
}
</script>

<style scoped>

</style>
