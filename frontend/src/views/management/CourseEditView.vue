<template>
  <div class="bx--grid">
    <div class="bx--col-lg-8">
      <EditCourseName :course="getCourse"
                    class="edit--course-props">
      </EditCourseName>
      <EditCourseDescription :course="getCourse"
                             class="edit--course-props">>
      </EditCourseDescription>
      <EditCourseLessons :course="getCourse"
                         class="edit--course-props">
      </EditCourseLessons>
      <EditCourseModal :course="getCourse"
                       class="edit--course-props">
      </EditCourseModal>
      </div>
  </div>
</template>

<script lang="ts">
import { Prop, Component, Vue } from 'vue-property-decorator';
import { mainStore } from '@/store';
import EditCourseName from '@/components/EditCourse/EditCourseName.vue';
import EditCourseDescription from '@/components/EditCourse/EditCourseDescription.vue';
import EditCourseLessons from '@/components/EditCourse/EditCourseLessons.vue';
import EditCourseModal from '@/components/EditCourse/EditCourseModal.vue';
import CourseModel from '@/models/CourseModel';

@Component({components: {
  EditCourseLessons,
  EditCourseDescription,
  EditCourseName,
  EditCourseModal,
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
.edit--course-props
  margin-top 10px
  .change-btn:not([disabled = disabled])
    background-color var(--cds-ui-05)
  .change-btn
    margin-top 10px
</style>
