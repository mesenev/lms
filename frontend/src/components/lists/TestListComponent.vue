<template>
  <div>
    <router-link :to="openTest(test)" class="list-element" v-for="test in testsList" :key="test.id">
      <div class="content-wrapper">
        <div class="title-wrapper">
          <h5 class="list-element--title"> {{ test.name }} </h5>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script lang="ts">
import TestModel from "@/models/TestModel";
import { Component, Prop, Vue } from 'vue-property-decorator';
import testStore from "@/store/modules/test"

@Component({ components: {} })
export default class TestListComponent extends Vue {
  @Prop({ required: true }) testsList!: Array<TestModel>;

  testStore = testStore;

  openTest(test: TestModel) {
    return { name: 'TestView', params: { testId: test.id.toString() } };
  }
}
</script>

<style scoped lang="stylus">
.list-element
  display flex
  flex-direction row
  justify-content space-between
  align-items center
  border-top 1px solid var(--cds-ui-03)
  border-bottom 1px solid var(--cds-ui-03)

.list-element:hover
  background-color var(--cds-ui-03)

.cv-tag
  display flex
  align-items stretch
  margin-right 1rem
</style>
