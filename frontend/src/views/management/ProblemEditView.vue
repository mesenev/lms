<template>
  <div class="bx--grid">
    <div class="bx--row header"><h1>Редактирование задачи</h1></div>
    <div v-if="showNotification" class="bx--row">
      <cv-inline-notification
        :kind="notificationKind"
        :sub-title="notificationText"
        @close="() => showNotification = false"
      />
    </div>
    <div class="bx--row">
      <div class="bx--col-lg-7 items">
        <cv-skeleton-text
          v-if="loading"
          :line-count="6"
          :paragraph="true"
          :width="'80%'"/>
        <div v-else>
          <cv-text-input v-model.trim="problemEdit.name" label="Название"/>
          <cv-text-area v-model.trim="problemEdit.description" label="Описание"/>
          <div>
            <br>
            <cv-multi-select
              :options="availableLanguages"
              aria-label="Языки"
              label="Доступные языки"/>
            <h5>Выбраны сейчас:</h5>
            <cv-list>
              <cv-list-item v-for="l in problemEdit.language" :key="l">{{ l }}</cv-list-item>
            </cv-list>
            <br>
            <!--          <cv-toggle label="Ручная проверка" v-model="problemEdit.manual"/>-->
          </div>
        </div>
        <cv-button-skeleton v-if="problemUpdating"/>
        <cv-button
          v-else :disabled="!isChanged || loading"
          class="finishButton"
          v-on:click="updateProblem">
          Обновить задачу
        </cv-button>

      </div>
      <div class="bx--col-lg-1"></div>
      <div class="bx--col-lg-7 items">
        <h4>cats версия задачи</h4>
        <cv-skeleton-text
          v-if="catsProblemLoading || catsProblem"
          :line-count="6"
          :paragraph="true"
          :width="'80%'"/>
        <CatsProblemComponent v-else :catsProblem="catsProblem"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import CatsProblemComponent from '@/components/EditProblem/CatsProblemComponent.vue';
import Problem from '@/components/lists/ProblemListComponent.vue';
import CatsProblemModel from '@/models/CatsProblemModel';
import ProblemModel from '@/models/ProblemModel';
import { problemStore } from '@/store';
import _ from 'lodash';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { Problem, CatsProblemComponent } })
export default class ProblemEditView extends Vue {
  private store = problemStore;
  @Prop() problemId!: number;
  problem!: ProblemModel;
  problemEdit = { ...this.store.getNewProblem }
  loading = true;
  catsProblemLoading = true;
  catsProblem: CatsProblemModel | null = null;
  notificationKind = 'success';
  notificationText = '';
  showNotification = false;
  problemUpdating = false;

  availableLanguages = [
    { name: 'python', label: 'python', value: 'python' },
    { name: 'c/c++', label: 'c/c++', value: 'c/c++' },
  ];

  get isChanged(): boolean {
    return !_.isEqual(this.problem, this.problemEdit);
  }

  async created() {
    this.loading = true;
    this.problem = await this.store.fetchProblemById(this.problemId);
    this.problemEdit = { ...this.problem }
    this.loading = false;
    this.catsProblem = await this.store.fetchCatsProblemById(this.problem.cats_id)
    this.catsProblemLoading = false;
  }

  updateProblem(): void {
    this.problemUpdating = true;
    const request = this.store.patchProblem(this.problemEdit);
    request.then(response => {
      this.notificationKind = 'success';
      this.notificationText = 'Задача успешно обновлена'
      this.problem = response.data;
      this.problemEdit = { ...this.problem };
    });
    request.catch(error => {
      this.notificationText = `Что-то пошло не так: ${error.message}`;
      this.notificationKind = 'error';
    })
    request.finally(() => {
      this.showNotification = true;
      this.problemUpdating = false;
    });

  }
}
</script>

<style scoped lang="stylus">
.items
  background-color var(--cds-ui-02)

.header
  padding-bottom 1.5rem
  padding-top 1rem

</style>
