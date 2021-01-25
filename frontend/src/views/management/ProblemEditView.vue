<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-10">
        <br>
        <h4>Название</h4>
        <label><input :class="`bx--text-input`" type="text"></label>
        <cv-button
          class="change__btn"
          @click="ChangeProblemName">
          Сменить название
        </cv-button>
        <br>
        <h4>Описание</h4>
        <cv-text-area/>
        <cv-button
          class="change__btn"
          @click="ChangeProblemDescription">
          Сменить описание
        </cv-button>
        <h4>Языки решения</h4>
        <div>
          <br>
          <cv-multi-select
            :options="availableLanguages"
            label="Доступные языки"/>
          <h5>Выбраны сейчас:</h5>
          <cv-list>
            <cv-list-item v-for="l in problemEdit.language" :key="l">{{ l }}</cv-list-item>
          </cv-list>
          <br>
          <cv-button
            class="change__btn"
            @click="ChangeProblemLanguage">
            Изменить
          </cv-button>
        </div>
      </div>
      <div class="bx--col-lg-3">
        <cv-toggle label="Ручная проверка" value="problem.manual"/>
        <cv-button
          class="change__btn"
          @click="ChangeProblemManual">
          Изменить
        </cv-button>
      </div>
      <div class="bx--col-lg-3"></div>
    </div>
  </div>
</template>

<script lang="ts">
import Problem from '@/components/lists/ProblemListComponent.vue';
import ProblemModel from '@/models/ProblemModel';
import { problemStore } from '@/store';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: { Problem } })
export default class ProblemEditView extends Vue {
  private store = problemStore;
  @Prop() problemId!: number;
  problem: ProblemModel | null = null;
  problemEdit = { ...this.store.getNewProblem }
  availableLanguages = [
    { name: 'python', label: 'python', value: 'python' },
    { name: 'c/c++', label: 'c/c++', value: 'c/c++' },
  ];

  async created() {
    this.problem = await this.store.fetchProblemById(this.problemId);
    this.problemEdit = { ...this.problem }
  }

  ChangeProblemName() { //
  }

  ChangeProblemDescription() {
    //
  }

  ChangeProblemManual() {
    //
  }

  ChangeProblemLanguage() {
    //
  }
}
</script>

<style scoped lang="stylus">
</style>
