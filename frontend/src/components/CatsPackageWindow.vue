<template >
  <div class="cats-package-window">
    <cv-data-table :columns="['Тест','Результат']">

      <template slot="data">
        <cv-data-table-row>
          <cv-data-table-cell>1</cv-data-table-cell>
          <cv-data-table-cell>Ошибка компиляции</cv-data-table-cell>
        </cv-data-table-row>
        <cv-data-table-row>
          <cv-data-table-cell>2</cv-data-table-cell>
          <cv-data-table-cell>Отклонено</cv-data-table-cell>
        </cv-data-table-row>
        <cv-data-table-row>
          <cv-data-table-cell>3</cv-data-table-cell>
          <cv-data-table-cell>Превышен лимит времени</cv-data-table-cell>
        </cv-data-table-row>
        <cv-data-table-row>
          <cv-data-table-cell>4</cv-data-table-cell>
          <cv-data-table-cell>Ошибка компиляции</cv-data-table-cell>
        </cv-data-table-row>
        <cv-data-table-row>
          <cv-data-table-cell>5</cv-data-table-cell>
          <cv-data-table-cell>ОК</cv-data-table-cell>
        </cv-data-table-row>
      </template>

    </cv-data-table>

  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class CatsPackageWindow extends Vue {

}
</script>


<style lang="stylus">

  .cats-package-window
    height 100%
    background white





</style>

<style lang="stylus" scoped>

</style>
