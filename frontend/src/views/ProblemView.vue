<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-10">
        <br>
        <h3> Задание {{problem.id}}. {{ problem.name }} </h3>
        <h4> Описание: {{problem.description}} </h4>
        <br>
      </div>
      <div class="bx--col-lg-6">
        <cv-inline-notification v-if="problem.completed"
                                kind="success"
                                :title="'Вы успешно сдали задачу!'"
                                @close="close()">
        </cv-inline-notification>
        <cv-inline-notification v-else
                                kind="error"
                                :title="'Ваше решение не сдано, или решено неверно.'"
                                action-label="Сдать"
                                @close="this.close()" @action="problem.completed = true">
        </cv-inline-notification>
      </div>
      <div class="bx--col-lg-10">
        <label>
          <TextArea
            cols="130"
            placeHolder="Сюда кодить надо"
            rows="20">
          </TextArea>
        </label>
        <cv-dropdown
          :placeholder="'Выберите язык программирования'"
          :value="value">
          <cv-dropdown-item value="YoptaScript">YoptaScript</cv-dropdown-item>
          <cv-dropdown-item value="Lolcat">LOLCODE</cv-dropdown-item>
          <cv-dropdown-item value="Brainfuck">Brainfuck</cv-dropdown-item>
        </cv-dropdown>
      </div>
    </div>
  </div>
</template>

<!--    TODO: notification work (close action, animation (?)) -->

<script lang="ts">

import Component from 'vue-class-component';
import Problem from '@/components/Problem.vue';
import Vue from 'vue';
import { mainStore } from '@/store';

@Component({ components: { Problem } })
export default class ProblemView extends Vue {
  private store = mainStore;

  problemsArray = this.store.getProblems;

  get problem() {
    return this.problemsArray[0];
  }
}
</script>
<!--    TODO: solve a problem w/ getting single problem from array -->

<style scoped>

</style>
