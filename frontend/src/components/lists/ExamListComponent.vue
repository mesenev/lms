<template>
  <div>
    <router-link :to="target(exam)" class="list-element" v-for="exam in examsList" :key="exam.id">
      <div class="content-wrapper">
        <div class="title-wrapper">
          <h5 class="list-element--title"> {{ exam.name }} </h5>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script lang="ts">
import ExamModel from "@/models/ExamModel";
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class ExamListComponent extends Vue {
  @Prop({ required: true }) examsList!: Array<ExamModel>;
  @Prop({ required: false }) isStaff!: boolean;

  target(exam: ExamModel) {
    return { name: 'ExamView', params: { examId: exam.id.toString() } };
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
