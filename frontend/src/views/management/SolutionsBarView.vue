<template>
  <cv-grid>
    <cv-row class="header">
      <cv-column>
        <div class="solution-container--submit-list">
          <cv-structured-list
            class="submit-list">
            <template slot="headings">
              <cv-structured-list-heading class="list-header">Задачи:</cv-structured-list-heading>
            </template>


            <template slot="items">
              <cv-structured-list-item
                v-for="problem in problems"
                :key="problem.name"
                class="problem-table-item">
                <cv-structured-list-data>
                  <cv-tag class="tag" kind="gray" label=""></cv-tag>
                </cv-structured-list-data>
                <cv-structured-list-data>{{ problem }}</cv-structured-list-data>
              </cv-structured-list-item>
            </template>


          </cv-structured-list>
        </div>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
import ProblemModel from "@/models/ProblemModel";
import userStore from '@/store/modules/user';
import problemStore from '@/store/modules/problem';
import courseStore from '@/store/modules/course';

@Component({components: {}})
export default class SolutionsBarView extends Vue {
  @Prop({required: true}) courseId!: number;
  @Prop({required: true}) userId!: number;

  private problemStore = problemStore;
  private userStore = userStore;
  private courseStore = courseStore;

  get problems() {
    return ["Остров невезения", "Фибоначчи", "Простые числа на миллион долларов", "Очень сложная задача)", "Задача номер пять!", "Задача, которая не должна отображаться)"];
  }

  // get problems(): Promise<string[]> {
  //   console.log(this.problemStore.fetchProblemsByUserId() as Promise<string[]>);
  // }


}
</script>

<style lang="stylus" scoped>

.list-header
  font-size 1.1rem
  padding-bottom 1rem

.submit-list
  justify-content center

.table
  width 1rem

.list-item
  border 1px solid rgba(0, 0, 0, .3)

</style>
