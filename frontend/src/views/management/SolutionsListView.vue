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
                <cv-link :to="row[1]">{{ row[0] }}</cv-link>
              </cv-data-table-cell>


              <cv-data-table-cell>
                <user-component :user-id="row[2]"></user-component>
              </cv-data-table-cell>

              <cv-data-table-cell>
                <submit-status :submit="row[5]"></submit-status>
              </cv-data-table-cell>

              <cv-data-table-cell>
                <cv-tag kind="blue" :label="row[4]"/>
              </cv-data-table-cell>


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
import SubmitStatus from "@/components/SubmitStatus.vue";

@Component({ components: { UserComponent, TrashCan16, Save16, Download16 } })
export default class SolutionsListView extends Vue {
  @Prop() courseId!: number;
  loading = false
  store = SubmitStore;
  submits_request: PaginatedList<SubmitModel> = { count: 0, results: [] };
  pagination_settings?: TablePagination;

  linkRoute(data: SubmitModel) {
    const params = {
      courseId: this.courseId.toString(),
      lessonId: data.lesson.toString(),
      problemId: data.problem.id.toString(),
      submitId: data.id.toString()
    };
    return {
      name: 'ProblemViewWithSubmit', params: { ...params },
    };
  }

  get_data_for_table(submit: SubmitModel) {
    const problem_data: string = submit.problem.name;
    const created_at_data: string = submit.created_at.slice(0, 4) + "."
      + submit.created_at.slice(5, 7) + "." +
      submit.created_at.slice(8, 10) +
      "---" + submit.created_at.slice(11, 19);
    const href_to_submit = this.linkRoute(submit)
    return [problem_data, href_to_submit as unknown as string, submit.student as unknown as string,
      submit.status as unknown as string, created_at_data, submit as unknown as string
    ]
  }

  get to_display() {
    const returned: string[][] = []
    if (!this.submits_request) {
      return []
    }
    this.submits_request.results.forEach(element => {

      returned.push(this.get_data_for_table(element))
    });

    return returned;
  }

  get pagination() {
    return {
      numberOfItems: Math.max(Math.floor((this.submits_request?.count || 0) + 1
        / (this.pagination_settings?.length || 1))),
      pageSizes: [5, 10, 25],
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
