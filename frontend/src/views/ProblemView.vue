<template>
  <cv-grid class="problem-view">
    <cv-row>
      <h1 v-if="problem">{{ problem.name }}</h1>
      <cv-skeleton-text v-else/>
    </cv-row>
    <cv-row>
      <cv-column :lg="8">
        <div class="item">
          <problem-description v-if="problem" :problem="problem"/>
          <cv-skeleton-text v-else/>
        </div>
      </cv-column>
    </cv-row>
    <cv-row>
      <cv-column :lg="10">
        <div class="solution-container item">
          <submit-component
            v-if="problem"
            :is-staff="isStaff" :language-list="problem.language"
            :submitId="submitId"
            class="solution-container--submit-component"/>
          <cv-loading v-else small/>
          <div class="solution-container--submit-list">
            <cv-structured-list
              v-if="submits" class="submit-list"
              condensed selectable @change="changeCurrentSubmit">
              <template slot="headings">
                <cv-structured-list-heading>id</cv-structured-list-heading>
                <cv-structured-list-heading>Статус</cv-structured-list-heading>
              </template>
              <template slot="items">
                <cv-structured-list-item
                  v-for="submit in userSubmits"
                  :key="submit.id"
                  :checked="checkedSubmit(submit)"
                  :value="submit.id.toString()"
                  name="submit">
                  <cv-structured-list-data>{{ submit.id }}</cv-structured-list-data>
                  <cv-structured-list-data>
                    <submit-status :submit="submit"/>
                  </cv-structured-list-data>
                </cv-structured-list-item>
              </template>
            </cv-structured-list>
            <cv-tile v-else class="submit-list no-submits" kind="standard">
              <h2>Oops</h2>
              <p>Пока ничего не отправлено :(</p>
            </cv-tile>
          </div>
        </div>
      </cv-column>
      <cv-column v-if="isStaff">
        <div class="item">
          <cv-structured-list class="student-list" condensed selectable @change="changeStudent">
            <template slot="headings">
              <cv-structured-list-heading>Ученик</cv-structured-list-heading>
            </template>
            <template slot="items">
              <cv-structured-list-item
                v-for="student in students"
                :key="student.id"
                :checked="checkedStudent(student)"
                :value="student.id.toString()"
                name="student">
                <cv-structured-list-data>
                  <user-component :user="student"/>
                </cv-structured-list-data>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
        </div>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<script lang="ts">
import ProblemDescription from "@/components/ProblemDescription.vue";
import SubmitComponent from '@/components/SubmitComponent.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import UserComponent from '@/components/UserComponent.vue';
import SubmitModel from '@/models/SubmitModel';
import UserModel from '@/models/UserModel';
import problemStore from '@/store/modules/problem';
import submitStore from '@/store/modules/submit';
import userStore from '@/store/modules/user';
import { Component, Prop, Vue } from 'vue-property-decorator';


@Component({ components: { SubmitComponent, ProblemDescription, SubmitStatus, UserComponent } })
export default class ProblemView extends Vue {
  @Prop({ required: false, default: null }) submitIdProp!: number | null;
  public submitId = this.submitIdProp;
  public studentId = NaN;

  private problemStore = problemStore;
  private userStore = userStore;
  private submitStore = submitStore;
  private user = this.userStore.user;
  private readonly courseId = Number(this.$route.params.courseId);

  get problem() {
    return this.problemStore.currentProblem;
  }

  get students() {
    return Object.keys(this.problem?.students).map(x => this.userStore.currentCourseStudents[x]);
  }

  get submits(): SubmitModel[] {
    return this.problem?.submits;
  }

  checkedSubmit(submit: SubmitModel): boolean {
    if (!this.submitIdProp)
      return submit.id === Math.max(...this.submits.map(s => s.id));
    return submit.id === this.submitIdProp;
  }

  get userSubmits() {
    return this.submits.filter((x: SubmitModel) => x.student === this.studentId);
  }

  changeCurrentSubmit(id: number) {
    this.submitId = Number(id);
    if (this.submitIdProp !== Number(id)) {
      this.$router.push({
        name: 'ProblemViewWithSubmit', params: {
          courseId: this.$route.params.courseId,
          lessonId: this.$route.params.lessonId,
          problemId: this.$route.params.problemId,
          submitId: Number(id).toString(),
        },
      })
    }
  }

  get isStaff(): boolean {
    return this.user.staff_for.includes(Number(this.courseId));
  }

  created() {
    if (this.submitId)
      this.studentId = this.submits?.find(x => x.id === this.submitId)?.student as number;
  }

  checkedStudent(student: UserModel): boolean {
    return student.id === this.studentId;
  }

  async changeStudent(id: number) {
    this.studentId = Number(id);
    this.changeCurrentSubmit(this.userSubmits[this.userSubmits.length - 1].id);
  }

  get isCompleted(): boolean {
    return !!this.submits.find((submit: SubmitModel) => (
      submit.status === 'OK'
    ));
  }
}
</script>

<style lang="stylus" scoped>
.item
  background-color var(--cds-ui-background)
  padding 1rem

.bx--row
  margin-bottom 1rem

.solution-container
  display flex

  &--submit-component
    flex 69%

  &--submit-list
    flex 30%

.name
  display flex
  flex-direction row
  justify-content space-between
  align-items center

.submit-list, .student-list
  margin 0
  padding 0

.student-list
  margin-left 1rem

.submit-btn, .handlers button
  margin-top 1rem


.submit
  display flex
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.problem-solution
  height 100%

.no-submits
  width 100%
  padding 0
  margin 0
  background-color inherit

.accepted, .rejected
  transition ease-in-out 0.25s

.accepted
  background-color var(--cds-inverse-support-02)

  &:hover
    background-color: var(--cds-support-02)

.rejected
  background-color var(--cds-inverse-support-01)

  &:hover
    background-color: var(--cds-support-01)

.text-area-student
.text-area-teacher
  border 1px solid black

.text-area-teacher textarea:disabled
  cursor pointer
  color #000

.problem-view
  margin-top: 2rem

.handlers
  button:nth-child(2n)
    margin-left 5px

.code
  .bx--text-area
    height 30em

  //width 45rem

  .bx--label,
  .bx--label--disabled
    display none

</style>
