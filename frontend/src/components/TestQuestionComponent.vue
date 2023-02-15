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
      <div class="answers" id="radio" v-for="answer in answerRadioCount" :key="answer">
        <span>вариант ответа {{ answer }}</span>
        <div class="answer-variant">
          <cv-text-input/>
          <component v-if="answerRadioCount > 1" class="action-btn" :is="closeFilled24" @click="deleteAnswer('radio')"/>
        </div>
      </div>
      <cv-link @click="addAnswer('radio')">Добавить вариант ответа</cv-link>
      <div class="answer-container">
        <cv-dropdown class="answer" placeholder="Выберите верный вариант ответа">
          <cv-dropdown-item value="1">1</cv-dropdown-item>
          <cv-dropdown-item value="2">2</cv-dropdown-item>
        </cv-dropdown>
      </div>
    </div>
    <div class="checkbox-container radio-container" v-if="answerType==='Check'">
      <div class="answers" id="checkbox" v-for="answer in answerCheckboxCount" :key="answer">
        <span>вариант ответа {{ answer }}</span>
        <div class="answer-variant">
          <cv-text-input/>
          <component v-if="answerCheckboxCount > 1" class="action-btn" :is="closeFilled24" @click="deleteAnswer('checkbox')"/>
        </div>
      </div>
      <cv-link @click="addAnswer('checkbox')">Добавить вариант ответа</cv-link>
      <div class="answer-container">
        <cv-multi-select label="Выберите верные варианты ответа" :light="true"/>
      </div>
    </div>
    <span>Сумма баллов</span>
    <div class="question-footer">
      <cv-number-input class="points-input"/>
      <div class="action-btns">
        <component class="action-btn" :is="trashCan24" @click="deleteQuestion"/>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import trashCan24 from "@carbon/icons-vue/lib/trash-can/24"
import closeFilled24 from "@carbon/icons-vue/lib/close--filled/24"

@Component({ components: { trashCan24, closeFilled24 } })
export default class TestQuestionComponent extends Vue {

  answerType = 'Short';
  trashCan24 = trashCan24;
  closeFilled24 = closeFilled24;

  answerRadioCount = 1;
  answerCheckboxCount = 1;

  addAnswer(answerType: string) {
    if (answerType === 'radio') {
      this.answerRadioCount++;
    } else {
      this.answerCheckboxCount++;
    }
  }

  deleteAnswer(answerType: string) {
    if (answerType === 'radio' && this.answerRadioCount > 1) {
      this.answerRadioCount--;
    } else if (this.answerCheckboxCount > 1) {
      this.answerCheckboxCount--;
    }
  }

  deleteQuestion() {
    this.$emit('delete-question');
  }

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

.answer-variant
  display flex
  align-items center
  gap 1rem

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
