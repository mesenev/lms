<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <div class="bx--offset-lg-2 main-title">
        <h1>Демо тест по экономике</h1>
        <div class="info-container">
        <div class="test-info">
          <span>Тест</span>
          <span>
            Макс. балл <strong> 5 </strong>
          </span>
          <span>
            Режим тестирования: <strong>manual</strong>
          </span>
        </div>
      </div>
      </div>
    </div>
    <cv-row class="main-items" justify="center">
      <cv-column :lg="{'span' : 8, 'offset' : 2}">
        <div class="test-container">
          <div class="question-container">
            <h4 class="question-title">Статистическая совокупность - это: </h4>
            <cv-radio-group class="answers" :vertical="true">
              <cv-radio-button name="1" label="множество изучаемых разнородных объектов" value="1" :disabled="flag"/>
              <cv-radio-button name="1" label="множество единиц изучаемого явления" value="2" :disabled="flag"/>
              <cv-radio-button name="1" label="группа зафиксированных случайных событий" value="3" :disabled="flag"/>
            </cv-radio-group>
          </div>
          <div class="question-container">
            <h4 class="question-title">
              Основные стадии экономико-статистического исследования включают:
            </h4>
            <div class="answers-checkbox">
              <cv-checkbox value="1" label="сбор первичных данных" :disabled="flag"/>
              <cv-checkbox value="2" label="статистическая сводка и группировка данных" :disabled="flag"/>
              <cv-checkbox value="3" label="контроль и управление объектами статистического изучения" :disabled="flag"/>
              <cv-checkbox value="4" label="анализ статистических данных" :disabled="flag"/>
            </div>
          </div>
          <div class="question-container">
            <h4 class="question-title">Ряд динамики, характеризующий уровень развития социально-экономического явления на определенные даты времени, называется:</h4>
            <cv-text-input v-model="shorttext" placeholder="Введите ответ" :disabled="flag"/>
          </div>
          <div class="question-container">
            <h4 class="question-title">Дайте понятие экономической статистике:</h4>
            <cv-text-area v-model="longtext" placeholder="Введите ответ" :disabled="flag"/>
          </div>
        </div>
        <div class="submit-container">
          <div class="question-container submit">
            <cv-button @click="submitTest" :disabled="flag">Отправить</cv-button>
          </div>
          <cv-inline-notification
              v-if="showNotification"
              @close="hideNotification"
              :kind="notificationKind"
              :sub-title="notificationText"/>
        </div>
      </cv-column>
    </cv-row>
  </div>
</template>

<script lang="ts">
import NotificationMixinComponent from "@/components/common/NotificationMixinComponent.vue";
import { Component } from "vue-property-decorator";

@Component({components: {}})
export default class TestView extends NotificationMixinComponent {
  flag = false;

  shorttext = '';
  longtext = '';
  submitTest() {
    this.flag = true;
    this.notificationKind = 'success';
    this.notificationText = 'Тест отправлен на проверку.'
    this.showNotification = true;
  }
}
</script>

<style scoped lang="stylus">
h1
  color var(--cds-ui-05)
  font-weight bold

span
  margin-left 0.5rem

.info-container
  display block

.test-info
  color var(--cds-ui-04)
  margin-top 0.5rem

.test-container
  display flex
  flex-direction column
  gap 1rem

.question-container
  background-color var(--cds-ui-01)
  border-radius 5px
  padding 1rem
  width 70%

.question-title
  margin-bottom 0.5rem

.answers
  margin-left 0.5rem

.answers-checkbox
  margin-left 1rem

.cv-text-input
  margin-left 1rem
  width 40%

.cv-text-area
  margin-left 1rem

/deep/ .bx--text-input
  border-radius 5px
  border 1px solid var(--cds-ui-05)

/deep/ .bx--text-area
  border-radius 5px
  border 1px solid var(--cds-ui-05)

.submit-container
  display flex
  gap 1rem
  flex-direction row
  width 60%

.submit
  width fit-content
  margin-top 0.5rem
</style>
