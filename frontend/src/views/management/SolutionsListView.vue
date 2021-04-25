<template>
  <cv-grid>
    <cv-row class="header">
      <h1>Отправленные решения</h1>
    </cv-row>
    <cv-row>
      <cv-column :lg="8" class="items">
        <cv-search
          label="label"
          placeholder="search"
        >
        </cv-search>
        <cv-data-table-skeleton v-if="loading"/>
        <cv-data-table v-else
                       ref="table"
                       :data="to_display"
                       :pagination="{ numberOfItems: submits_request.count, pageSizes: [20, 50, 100] }">
          <template slot="actions">
            <cv-data-table-action>
              <svg alt="Download" aria-label="Download" fill-rule="evenodd" height="16" name="download" role="img"
                   viewBox="0 0 14 16" width="14">
                <title>Download</title>
                <path d="M7.506 11.03l4.137-4.376.727.687-5.363 5.672-5.367-5.67.726-.687 4.14 4.374V0h1v11.03z"></path>
                <path d="M13 15v-2h1v2a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1v-2h1v2h12z"></path>
              </svg>
            </cv-data-table-action>
            <cv-data-table-action>
              <svg alt="Edit" aria-label="Edit" fill-rule="evenodd" height="16" name="edit" role="img"
                   viewBox="0 0 16 16" width="16">
                <title>Edit</title>
                <path
                  d="M7.926 3.38L1.002 9.72V12h2.304l6.926-6.316L7.926 3.38zm.738-.675l2.308 2.304 1.451-1.324-2.308-2.309-1.451 1.329zM.002 9.28L9.439.639a1 1 0 0 1 1.383.03l2.309 2.309a1 1 0 0 1-.034 1.446L3.694 13H.002V9.28zM0 16.013v-1h16v1z"></path>
              </svg>
            </cv-data-table-action>
            <cv-data-table-action>
              <svg alt="Settings" aria-label="Settings" fill-rule="evenodd" height="16" name="settings" role="img"
                   viewBox="0 0 15 16" width="15">
                <title>Settings</title>
                <path
                  d="M7.53 10.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zm0 1a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7z"></path>
                <path
                  d="M6.268 2.636l-.313.093c-.662.198-1.28.52-1.822.946l-.255.2-1.427-.754-1.214 1.735 1.186 1.073-.104.31a5.493 5.493 0 0 0-.198 2.759l.05.274L1 10.33l1.214 1.734 1.06-.56.262.275a5.5 5.5 0 0 0 2.42 1.491l.312.093L6.472 15H8.59l.204-1.636.313-.093a5.494 5.494 0 0 0 2.21-1.28l.26-.248 1.09.576 1.214-1.734-1.08-.977.071-.29a5.514 5.514 0 0 0-.073-2.905l-.091-.302 1.15-1.041-1.214-1.734-1.3.687-.257-.22a5.487 5.487 0 0 0-1.98-1.074l-.313-.093L8.59 1H6.472l-.204 1.636zM5.48.876A1 1 0 0 1 6.472 0H8.59a1 1 0 0 1 .992.876l.124.997a6.486 6.486 0 0 1 1.761.954l.71-.375a1 1 0 0 1 1.286.31l1.215 1.734a1 1 0 0 1-.149 1.316l-.688.622a6.514 6.514 0 0 1 .067 2.828l.644.581a1 1 0 0 1 .148 1.316l-1.214 1.734a1 1 0 0 1-1.287.31l-.464-.245c-.6.508-1.286.905-2.029 1.169l-.124.997A1 1 0 0 1 8.59 16H6.472a1 1 0 0 1-.992-.876l-.125-.997a6.499 6.499 0 0 1-2.274-1.389l-.399.211a1 1 0 0 1-1.287-.31L.181 10.904A1 1 0 0 1 .329 9.59l.764-.69a6.553 6.553 0 0 1 .18-2.662l-.707-.64a1 1 0 0 1-.148-1.315l1.214-1.734a1 1 0 0 1 1.287-.31l.86.454a6.482 6.482 0 0 1 1.576-.819L5.48.876z"></path>
              </svg>
            </cv-data-table-action>
            <cv-button small>Add new</cv-button>
          </template>
          <template slot="batch-actions">
            <cv-button>
              Delete
              <TrashCan16 class="bx--btn__icon"/>
            </cv-button>
            <cv-button>
              Save
              <Save16 class="bx--btn__icon"/>
            </cv-button>
            <cv-button>
              Download
              <Download16 class="bx--btn__icon"/>
            </cv-button>
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

  loading = true;
  store = SubmitStore;
  submits_request?: PaginatedList<SubmitModel> = null;

  get to_display() {
    if (this.submits_request)
      return this.submits_request.results;
    return [];
  }

  async created() {
    this.submits_request = await this.store.fetchSubmitsByCourse({ courseId: this.courseId });
    this.loading = false;
  }

}
</script>

<style lang="stylus" scoped>
.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.items
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

  .bx--structured-list-thead
    display none

.item
  min-height 85px
</style>
