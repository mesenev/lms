<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-10">
        <h1> Задание {{problem.id}}. {{ problem.name }} </h1>
        <h3> Описание:
          {{problem.description}}</h3>
      </div>
      <div class="bx--col-lg-6">
        <cv-inline-notification v-if="problem.completed"
                                kind="success"
                                :title="'Вы успешно сдали задачу!'"
                                @close="close()">
        </cv-inline-notification>
        <cv-inline-notification v-else
                                kind="error"
                                :title="'Ваше решение не сдано, или не верно.'"
                                action-label="Сдать"
                                @close="close()" @action="problem.completed = true">
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

<!--    TODO: notification work + grid and style work pls hlp -->

<script lang="ts">

import ProblemModel from '@/models/ProblemModel';

export default {
  name: 'ProblemView',
  props: {},
  data() {
    return {
      problem: {
        id: 7,
        name: 'Чё тебе надо у меня дома, мент',
        description: 'К джентельмену вломились силовые структуры.'
          + ' Помогите ему выяснить причину их появления и, по возможности,'
          + ' получить компенсацию за поломанное имущество.',
        completed: false,
      } as ProblemModel,
    };
  },
  methods: {},
  computed: {},
};
</script>

<style scoped>

</style>
