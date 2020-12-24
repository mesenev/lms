<template>
  <div class="bx--grid">
    <EditCourseName :course="getCourse"
                    class="bx--col-lg-8 edit__course__props">
    </EditCourseName>
    <EditCourseDescription :course="getCourse"
                           class="bx--col-lg-8 edit__course__props">>
    </EditCourseDescription>
    <EditCourseLessons :course="getCourse"
                       class="bx--col-lg-8 edit__course__props">
    </EditCourseLessons>
  </div>
</template>

<script lang="ts">
import { Prop, Component, Vue } from 'vue-property-decorator';
import { mainStore } from '@/store';
import EditCourseName from '@/components/courseEdit/EditCourseName.vue';
import EditCourseDescription from '@/components/courseEdit/EditCourseDescription.vue';
import EditCourseLessons from '@/components/courseEdit/EditCourseLessons.vue';
import CourseModel from '@/models/CourseModel';

@Component({components: {
  EditCourseLessons,
  EditCourseDescription,
  EditCourseName,
}})
export default class CourseEditView extends Vue {
  @Prop() courseId!: number;

  store = mainStore;

  get getCourse(): CourseModel {
    return this.store.getCourse;
  }
}
</script>

<style lang="stylus">
.edit__course__props
  margin-top 10px
  & .change__btn:not([disabled = disabled])
    background-color var(--cds-ui-05)
  & .change__btn
    margin-top 10px
</style>
