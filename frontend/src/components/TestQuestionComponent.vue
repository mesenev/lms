<template>
  <div class="question-container">
    <div class="question-header">
      <cv-text-area class="question" placeholder="Вопрос"/>
      <cv-dropdown
        v-model="answerType"
        class="answer-type"
        value="Short"
        placeholder="Тип ответа">
        <cv-dropdown-item value="Short">Короткий ответ</cv-dropdown-item>
        <cv-dropdown-item value="Long">Параграф</cv-dropdown-item>
        <cv-dropdown-item value="Radio">Radio</cv-dropdown-item>
        <cv-dropdown-item value="Check">Checkbox</cv-dropdown-item>
      </cv-dropdown>
    </div>
    <cv-text-input placeholder="Описание (опционально)"/>
    <div class="short-answer" v-if="answerType==='Short'">
      <span>Ответ</span>
      <cv-text-input class="short-answer-input"
                     placeholder="Введите верный ответ"/>
    </div>
    <div class="long-answer" v-if="answerType==='Long'">
      <span>Ответ</span>
      <cv-text-area class="long-answer-input"
                    placeholder="Введите верный ответ"/>
    </div>
    <div class="radio-container" v-if="answerType==='Radio'">
      <span>вариант ответа</span>
      <cv-text-input/>
      <span>вариант ответа</span>
      <cv-text-input/>
      <cv-link>Добавить вариант ответа</cv-link>
      <div class="answer-container">
        <cv-dropdown class="answer" placeholder="Выберите верный вариант ответа">
          <cv-dropdown-item value="1">1</cv-dropdown-item>
          <cv-dropdown-item value="2">2</cv-dropdown-item>
        </cv-dropdown>
      </div>
    </div>
    <div class="checkbox-container radio-container" v-if="answerType==='Check'">
      <span>вариант ответа</span>
      <cv-text-input/>
      <span>вариант ответа</span>
      <cv-text-input/>
      <cv-link>Добавить вариант ответа</cv-link>
      <div class="answer-container">
        <cv-multi-select label="Выберите верные варианты ответа" :light="true"/>
      </div>
    </div>
     <span>Сумма баллов</span>
    <div class="question-footer">
      <cv-number-input class="points-input"/>
      <div class="action-btns">
        <component class="action-btn" :is="trashCan"/>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import trashCan from "@carbon/icons-vue/lib/trash-can/24"

@Component({ components: { trashCan } })
export default class TestQuestionComponent extends Vue {

  answerType = 'Short';
  trashCan = trashCan;

}
</script>

<style scoped lang="stylus">
.question-container
  background var(--cds-ui-01)
  padding 1rem
  border-radius 5px
  margin-top 1rem

.question-header
  display flex
  flex-direction row
  justify-content space-between
  margin-bottom 1rem

.question
  width 50%

/deep/ .bx--label
  display none

.answer-type /deep/ .bx--dropdown__wrapper.bx--list-box__wrapper
  max-width 40%

/deep/ .bx--list-box__field
  display flex

.answer-type
  width 40%
  align-items end

.short-answer
  width 50%
  margin-top 1rem
  margin-bottom 1rem

.long-answer
  margin-top 1rem
  margin-bottom 1rem

.radio-container
  margin-top 1rem
  display flex
  flex-direction column
  gap 0.5rem
  width 50%

.answer-container
  margin-top 1rem
  margin-bottom 1rem

.points-input /deep/ .bx--number
  width 11rem

.question-footer
  display flex

.action-btns
  background var(--cds-ui-02)
  display flex
  gap 1rem
  border-radius 5px
  padding 1rem

.action-btn
  cursor pointer
  transition ease-in-out 0.1s

.action-btn:active
  transform scale(0.9)
</style>
