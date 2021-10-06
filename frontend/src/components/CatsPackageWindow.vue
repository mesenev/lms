<template >
  <div class="cats-package-window">
    <cv-data-table :columns="['Тест','Результат']"
    :data="cats_data"
    >

      <template slot="data">
        <cv-data-table-row v-for="(row, rowIndex) in cats_data" :key="`${rowIndex}`" :value="`${rowIndex}`">
          <cv-data-table-cell>{{ row[0] }}</cv-data-table-cell>
          <cv-data-table-cell>{{ row[1] }}</cv-data-table-cell>
        </cv-data-table-row>
      </template>

    </cv-data-table>

  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class CatsPackageWindow extends Vue {
  cats_data = this.getCatsData;

  get getCatsData(){
    return [['Тест 1', 'ОК'], ['Тест 2', 'НЕ ОК']];
  }
}
</script>


<style lang="stylus">

  .cats-package-window
    height 100%
    background white





</style>

<style lang="stylus" scoped>

</style>
