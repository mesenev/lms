<template>
  <cv-grid>
    <cv-row class="header">
      <h1>Отправленные решения</h1>
    </cv-row>
    <cv-row>
      <cv-column :lg="8" class="items">
        <cv-search label="label" placeholder="search"/>
        <cv-data-table
          ref="table"
          :columns="columns"
          :data="to_display"
          :pagination="pagination"
          :zebra="true"
          @pagination="actionOnPagination">
          <template v-if="loading" slot='data'>
            <cv-data-table-skeleton/>
          </template>
        </cv-data-table>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<script lang="ts">
import PaginatedList from '@/models/PaginatedList';
import SubmitModel from '@/models/SubmitModel';
import { Component, Prop, Vue } from 'vue-property-decorator';
import SubmitStore from '@/store/modules/submit';
import TrashCan16 from '@carbon/icons-vue/es/trash-can/16';
import Save16 from '@carbon/icons-vue/es/save/16';
import Download16 from '@carbon/icons-vue/es/download/16';


@Component({ components: { TrashCan16, Save16, Download16 } })
export default class SolutionsListView extends Vue {
  @Prop() courseId!: number;
  loading = false;
  store = SubmitStore;
  submits_request: PaginatedList<SubmitModel> = { count: 0, results: [] };
  pagination_settings?: TablePagination;

  get to_display() {
<<<<<<< HEAD
<<<<<<< HEAD
    let i: number
    const returned: Array<Array<string>> = [["Tom", "Bob", "Alice"]]
    returned.pop()
    if (this.submits_request) {
      for (i = 0 ; i < this.submits_request.results.length; i++){
        const problem_data: string = "ID : " + this.submits_request.results[i].problem.id as unknown as string + " Название : " + this.submits_request.results[i].problem.name
        const created_at_data: string = this.submits_request.results[i].created_at.slice(0, 4) + "." + this.submits_request.results[i].created_at.slice(5, 7) + "." + this.submits_request.results[i].created_at.slice(8, 10) + "---" + this.submits_request.results[i].created_at.slice(11, 19)
        returned.push(
          [
            problem_data,
            this.submits_request.results[i].id as unknown as string,
            this.submits_request.results[i].student as unknown as string,
            this.submits_request.results[i].status as unknown as string,
            created_at_data
          ]
        )
      }

      return returned;
    }
    else {
      return [];
    }
=======
    if (this.submits_request)
      return this.submits_request.results;
    return [];
>>>>>>> parent of bec8744 (Табличку починил)
=======
    if (this.submits_request)
      return this.submits_request.results;
    return [];
>>>>>>> parent of bec8744 (Табличку починил)
  }

  get pagination() {
    return {
      numberOfItems: Math.max(Math.floor((this.submits_request?.count || 0) + 1
        / (this.pagination_settings?.length || 1))),
      pageSizes: [2, 5, 10],
    };
  }

  get columns() {
    return ['Проблема', 'Ссылка на решение', 'Студент', 'Статус', 'Отправка']
  }

  async created() {
    //
  }

  async actionOnPagination(object: TablePagination) {
    this.pagination_settings = { ...object };
    this.loading = true;
    this.submits_request = await this.store.fetchSubmitsByCourse(
      {
        course_id: this.courseId,
        page: this.pagination_settings.page,
        page_size: this.pagination_settings.length,
      },
    );
    this.loading = false;
    return;
  }
}

interface TablePagination {
  start: number;
  page: number;
  length: number;
}

</script>

<style lang="stylus" scoped>
.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.items
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.item
  min-height 85px
</style>
