<template>
  <cv-grid>
    <cv-row class="header-container">
      <h1 class="main-title">Отправленные решения</h1>
    </cv-row>
    <cv-row>
      <cv-data-table-skeleton style="width: 70%" v-if="createLoading" :columns="4" :rows="5"/>
      <cv-column v-else-if="to_display.length" :lg="8" class="items">
        <cv-search label="label" placeholder="поиск"/>
        <cv-data-table
          ref="table"
          :columns="columns"
          :data="to_display"
          :pagination="pagination"
          :zebra="true"
          @pagination="actionOnPagination">
          <template v-if="loading" v-slot:data>
            <cv-data-table-skeleton/>
          </template>
          <template v-else v-slot:data>
            <cv-data-table-row
              v-for="(row, rowIndex) in to_display"
              :key="`${rowIndex}`"
              :value="`${rowIndex}`">
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
      <empty-list-component v-else class="empty-list" :text="emptyListText" list-of="submits"/>
    </cv-row>
  </cv-grid>
</template>

<script lang="ts" setup>
import type { PaginatedList } from '@/models/PaginatedList';
import type { SubmitModel } from '@/models/SubmitModel';
import useSubmitStore from '@/stores/modules/submit';
import TrashCan16 from '@carbon/icons-vue/es/trash-can/16';
import Save16 from '@carbon/icons-vue/es/save/16';
import Download16 from '@carbon/icons-vue/es/download/16';
import UserComponent from "@/components/UserComponent.vue";
import SubmitStatus from "@/components/SubmitStatus.vue";
import EmptyListComponent from "@/components/lists/EmptyListComponent.vue";
import { ref, type Ref, computed, onMounted } from 'vue';

  const props = defineProps({courseId:{type: Number, required: true}})
  const createLoading: Ref<boolean> = ref(false);
  const emptyListText: Ref<string> = ref('');
  const loading: Ref<boolean> = ref(false);
  const store = useSubmitStore();
  const submits_request: Ref<PaginatedList<SubmitModel>> = ref({ count: 0, results: [] });
  let pagination_settings: TablePagination;

  function linkRoute(data: SubmitModel) {
    const params = {
      courseId: props.courseId.toString(),
      lessonId: data.lesson.toString(),
      problemId: data.problem.id.toString(),
      submitId: data.id.toString()
    };
    return {
      name: 'ProblemViewWithSubmit', params: { ...params },
    };
  }

  function get_data_for_table(submit: SubmitModel) {
    const month_data: { [key: string]: string } = {
      '01': 'января',
      '02': 'февраля',
      '03': 'марта',
      '04': 'апреля',
      '05': 'мая',
      '06': 'июня',
      '07': 'июля',
      '08': 'августа',
      '09': 'сентября',
      '10': 'октября',
      '11': 'ноября',
      '12': 'декабря'
    }
    const problem_data: string = submit.problem.name;
    const created_at_data: string = submit.created_at.slice(11, 16) + " " +
      submit.created_at.slice(8, 10) + " " +
      month_data[submit.created_at.slice(5, 7)];

    const href_to_submit = linkRoute(submit);
    return [problem_data, href_to_submit as unknown as string, submit.student as unknown as string,
      submit.status as unknown as string, created_at_data, submit as unknown as string
    ];
  }

  const to_display = computed(() => {
    const returned: string[][] = []
    if (!submits_request.value) {
      return []
    }
    submits_request.value.results.forEach(element => {
      returned.push(get_data_for_table(element))
    });
    return returned;
  })

  const pagination = computed(() => {
    return {
      numberOfItems: Math.max(Math.floor((submits_request.value?.count || 0) + 1
        / (pagination_settings?.length || 1))),
      pageSizes: [25, 50, 100],
    };
  })

  const columns = computed(() => {
    return ['Проблема', 'Студент', 'Статус', 'Отправка']
  })

  onMounted(async () => {
    createLoading.value = true;
    await actionOnPagination({start: 0, page: 1, length: 1});
    emptyListText.value = 'В данный момент решения отсутствуют';
    createLoading.value = false;
  })

  async function actionOnPagination(object: TablePagination) {
    pagination_settings = { ...object };
    loading.value = true;
    submits_request.value = await store.fetchSubmitsByCourse(
      {
        course_id: props.courseId,
        page: pagination_settings.page,
        page_size: pagination_settings.length,
      },
    );
    loading.value = false;
    return;
  }

interface TablePagination {
  start: number;
  page: number;
  length: number;
}

</script>

<style lang="stylus" scoped>
.header
  color var(--cds-text-01)

/deep/ .bx--search-input
  background-color var(--cds-ui-background)

.empty-list
  margin-left 1.5rem

.items
  background-color var(--cds-ui-01)
  padding var(--cds-spacing-05)

.item
  min-height 85px
</style>
