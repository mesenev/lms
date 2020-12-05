<template>
  <div>
    <!-- TODO ссылка на задачу -->
    <cv-data-table :columns="columns">
      <template slot="data">
        <cv-data-table-row v-for="user in users" :key="user.id">
          <cv-data-table-cell>
            <!-- TODO ссылка на профиль -->
            {{ user.name }}
          </cv-data-table-cell>
          <cv-data-table-cell v-for="(mark, m_) in user.course.marks" :key="m_">
            {{ mark }}
          </cv-data-table-cell>
          <cv-data-table-cell>
            {{ avarage(user.id) }}
          </cv-data-table-cell>
        </cv-data-table-row>
      </template>
    </cv-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { mainStore } from '@/store';

@Component({})
export default class Progress extends Vue {
  name!: 'Progress';

  columns = ['Ученики'].concat(mainStore.getColumns).concat(['Рейтинг']);

  users = mainStore.getUsers;

  avarage(id: number): number {
    const sum = (marks: number[]) => marks.reduce((total, value) => total + value);
    const { marks } = this.users[id].course;
    return sum(marks) / marks.length;
  }
}
</script>

<style lang="stylus">

</style>
