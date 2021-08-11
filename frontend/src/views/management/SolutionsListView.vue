<template>
  <cv-grid>
    <cv-row class="header">
      <h1>Отправленные решения </h1>
    </cv-row>
    <cv-row>
      <cv-column :lg="8" class="items">
        <cv-search label="label" placeholder="поиск"/>
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
          <template v-else slot="data">
            <cv-data-table-row v-for="(row, rowIndex) in to_display" :key="`${rowIndex}`" :value="`${rowIndex}`">

              <cv-data-table-cell>
                {{row[0]}}
                <a :href = "row[1]"><svg data-v-65e70dec="" focusable="false" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path data-v-65e70dec="" d="M13,14H3c-0.6,0-1-0.4-1-1V3c0-0.6,0.4-1,1-1h5v1H3v10h10V8h1v5C14,13.6,13.6,14,13,14z"></path><path data-v-65e70dec="" d="M10 1L10 2 13.3 2 9 6.3 9.7 7 14 2.7 14 6 15 6 15 1z"></path></svg></a>
              </cv-data-table-cell>


              <cv-data-table-cell>
                <user-component :user-id="row[2]" ></user-component>
              </cv-data-table-cell>

              <cv-data-table-cell v-if="row[3]==='OK'">
                <cv-tag kind="green" :label="row[3]"/>
              </cv-data-table-cell>
              <cv-data-table-cell v-if="row[3]==='NP'">
                <cv-tag kind="purple" :label="row[3]"/>
              </cv-data-table-cell>

              <cv-data-table-cell><cv-tag kind="blue" :label="row[4]" /></cv-data-table-cell>


          </cv-data-table-row>

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
import UserComponent from "@/components/UserComponent.vue";




@Component({ components: {UserComponent, TrashCan16, Save16, Download16 } })
export default class SolutionsListView extends Vue {
  @Prop() courseId!: number;
  loading = false
  store = SubmitStore;
  submits_request: PaginatedList<SubmitModel> = { count: 0, results: [] };
  pagination_settings?: TablePagination;



  get to_display() {
    const returned: string[][] = []
    if (this.submits_request) {
      this.submits_request.results.forEach(element =>{
        const problem_data: string = element.problem.name;
        const created_at_data: string = element.created_at.slice(0, 4) + "."
          + element.created_at.slice(5, 7) + "." +
          element.created_at.slice(8, 10) +
          "---" + element.created_at.slice(11, 19);

        const href_to_submit: string = "/course/" + this.courseId as unknown as string   + "/lesson/" +
          element.lesson as unknown as string + "/problem/" +
          element.problem.id as unknown as string + "/submit/" +
          element.id as unknown as string;

        returned.push(
          [
            problem_data,
            href_to_submit,
            element.student as unknown as string,
            element.status as unknown as string,
            created_at_data
          ]
        )
      });

      return returned;
    }
    else {
      return [];
    }
  }

  get pagination() {
    return {
      numberOfItems: Math.max(Math.floor((this.submits_request?.count || 0) + 1
        / (this.pagination_settings?.length || 1))),
      pageSizes: [2, 5, 10],
    };
  }

  get columns() {
    return ['Проблема', 'Студент', 'Статус', 'Отправка']
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
