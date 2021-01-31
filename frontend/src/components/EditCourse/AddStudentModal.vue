<template>
  <!--
          @primary-click="addLesson"-->
  <!-- TODO: button disable + pick a person => to a list of course view -->
  <div>
    <cv-button class="change-btn" @click="showModal">
      Добавить пользователя в курс
    </cv-button>
    <cv-modal size="default"
              class="addUser"
              :visible="modalVisible"
              @modal-hidden="modalHidden"
              :primary-button-disabled="!selected.length"
              @secondary-click="() => {}">
      <template slot="label">{{ course.name }}</template>
      <cv-inline-notification
        v-if="showNotification"
        @close="() => showNotification=false"
        kind="error"
        :sub-title="notificationText"
      />
      <template slot="title">
        <h3>Добавить пользователя</h3>
        <cv-content-switcher class="switcher">
          <cv-content-switcher-button content-selector=".content-1" selected>
            Добавить ученика
          </cv-content-switcher-button>
          <cv-content-switcher-button content-selector=".content-2">
            Добавить преподавателя
          </cv-content-switcher-button>
        </cv-content-switcher>
      </template>
      <template slot="content">
        <section class="modal--content">
          <div class="content-1">
            <cv-data-table
              v-if="studentsFetched" :columns="columns"
              :data="studentsList" :rows-selected="selected">
              <template slot="batch-actions">
                <div>
                </div>
              </template>
            </cv-data-table>
            <cv-data-table-skeleton v-else/>
          </div>
          <div class="content-2" hidden>
            <div>
              <cv-structured-list selectable>
                <template slot="items">
                  <cv-data-table v-if="staffFetched" :data="staffList" :columns="columns" :rows-selected="selected">
                  </cv-data-table>
                  <cv-data-table-skeleton v-else/>
                </template>
              </cv-structured-list>
            </div>
          </div>
        </section>
      </template>
      <template slot="primary-button">
        Добавить
      </template>
    </cv-modal>
  </div>
</template>

<script lang="ts">
import CourseModel from '@/models/CourseModel';
import courseStore from '@/store/modules/course';
import axios, { AxiosResponse } from 'axios';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({ components: {} })
export default class EditCourseModal extends Vue {
  @Prop({ required: true }) course!: CourseModel;
  @Prop({ required: true }) courseId!: number;
  modalVisible = false;
  store = courseStore;
  studentsFetched = false;
  staffFetched = false;
  studentsList = [];
  staffList = [];
  studentFilter = '';
  staffFilter = '';
  selected = [];

  notificationKind = 'success'
  showNotification = false;
  notificationText = '';

  columns = [
    "ID",
    "Username",
    "First Name",
    "Last Name",
  ]


  async created() {
    await axios.get(
      `/api/students_for_course/${this.courseId}/`,
    ).catch(error => {
      console.log(error.response);
      this.notificationKind = 'error';
      this.notificationText = `Ошибка получения списка студентов: ${error.response}`;
      this.showNotification = true;
      this.studentsFetched = true;
    }).then(response => {
      this.studentsList = (response as AxiosResponse).data;
      this.studentsFetched = true;
    })
    await axios.get(
      `/api/staff_for_course/${this.courseId}/`,
    ).catch(error => {
      console.log(error.response);
      this.notificationKind = 'error';
      this.notificationText = `Ошибка получения списка преподавателей: ${error.response}`;
      this.showNotification = true;
      this.studentsFetched = true;
    }).then(response => {
      this.staffList = (response as AxiosResponse).data;
      this.staffFetched = true;
    })
  }

  get filteredStudents() {
    if (this.studentFilter)
      return this.studentsList.filter(x => true);
    return this.studentsList;
  }

  returned() {
    console.log(this.selected)
    return this.selected
  }

  get filteredStaff() {
    if (this.staffFilter)
      return this.staffList.filter(x => true);
    return this.staffList;
  }


  showModal() {
    this.modalVisible = true;
    this.showNotification = false;
  }

  modalHidden() {
    this.modalVisible = false;
  }
}
</script>

<style scoped lang="stylus">
.bx--modal-content:focus
  outline none

.lesson_list
  margin-bottom 0

.lesson-card:hover
  border-bottom 1px solid var(--cds-ui-05)

.switcher
  margin-bottom: 5px

.addUser .bx--modal-container
  height 75vh

.addUser .bx--modal-footer
  height 3.5rem

.addUser .bx--btn
  height 3rem
  border none

.addUser .bx--btn--secondary
  background-color var(--cds-hover-secondary)

  &:hover, &:active, &:focus
    outline none
    box-shadow none
    border none

.addUser .bx--btn--primary[disabled = disabled],
.addUser .bx--btn--primary
  background-color var(--cds-ui-05)

.modal--content
  height 500px
</style>
