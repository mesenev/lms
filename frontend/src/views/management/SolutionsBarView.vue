<template>
  <cv-grid>
    <cv-row class="header">
      <cv-column>
        <cv-list
          :ordered="ordered">
          <cv-list-item v-for="submit in submits"
                        {{}}
          />
        </cv-list>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<script lang="ts">
import SubmitModel from '@/models/SubmitModel';
import {Component, Prop, Vue} from 'vue-property-decorator';
import SubmitStore from '@/store/modules/submit';

@Component({components: {}})
export default class SolutionsBarView extends Vue {
  @Prop() courseId!: number;

  submits_request?: SubmitModel = undefined;
  loading = true;
  store = SubmitStore;

  get to_display() {
    if (this.submits_request)
      return
  }

  async created() {
    this.submits_request = await this.store.fetchSubmitsByCourse({course_id: this.courseId});
    this.loading = false;
  }

}
</script>

<style lang="stylus" scoped>
.table
  width 1rem

</style>
