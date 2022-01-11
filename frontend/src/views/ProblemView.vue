<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <div class="main-title">
        <h1 v-if="problem" class=""> {{ problem.name }}</h1>
        <cv-skeleton-text v-else :heading="true" :width="'35%'" class="main-title"/>
        <div class="description-container">
          <cv-link v-if="problem"
                   class="show-problem-link"
                   @click="showProblem">
            Условие задачи
          </cv-link>
          <cv-skeleton-text v-else class="" width="'35%'"/>
          <cv-modal
            :visible="displayProblem"
            class="problem-description-modal"
            close-aria-label="Закрыть"
            size="large"
            @modal-hidden="hideProblem">
            <template slot="title">{{ problem.name }}</template>
            <template slot="content">
              <problem-description :problem="problem"/>
            </template>
          </cv-modal>
        </div>
      </div>
    </div>
    <cv-row>
      <cv-column :lg="7">
        <div class="solution-container item">
          <submit-component
            v-if="problem"
            :is-staff="isStaff" :language-list="problem.language"
            @submit-created="(x) => changeCurrentSubmit(x.id)"
            :submitId="submitId"
            class="solution-container--submit-component"/>
          <cv-loading v-else small/>
          <div class="solution-container--submit-list">
            <log-event-component
              :problemId="problem.id" :studentId="studentId"
              :selected-submit="submitId"
              class="log--event--component"
              @submit-selected="(x) => changeCurrentSubmit(x.id)"
              @cats-answer="(x) => showCatsAnswerModal(x.id)"
            />
          </div>
        </div>
      </cv-column>
      <cv-column v-if="isStaff && !displayCatsPackage">
        <div class="item">
          <cv-structured-list class="student-list" condensed selectable @change="changeStudent">
            <template slot="headings"/>
            <template slot="items">
              <cv-structured-list-item
                class="student-list--item"
                v-for="student in studentIds"
                :key="student"
                :checked="checkedStudent(student)"
                :value="student.toString()"
                name="student">
                <cv-structured-list-data>
                  <user-component :user-id="student" class="student-list--item--user-component"/>
                </cv-structured-list-data>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
        </div>
      </cv-column>

      <cv-column v-if="displayCatsPackage">
        <cats-package-window :submit-id-prop="catsResultSubmitId"/>
      </cv-column>

    </cv-row>
  </div>
</template>

<script lang="ts">
import ProblemDescription from "@/components/ProblemDescription.vue";
import SubmitComponent from '@/components/SubmitComponent.vue';
import LogEventComponent from '@/components/LogEventComponent.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import UserComponent from '@/components/UserComponent.vue';
import SubmitModel from '@/models/SubmitModel';
import problemStore from '@/store/modules/problem';
import submitStore from '@/store/modules/submit';
import userStore from '@/store/modules/user';
import { Component, Prop, Vue } from 'vue-property-decorator';
import CatsPackageWindow from "@/components/CatsPackageWindow.vue";


@Component({
  components: {
    CatsPackageWindow,
    SubmitComponent,
    ProblemDescription,
    SubmitStatus,
    UserComponent,
    LogEventComponent,
  },
})
export default class ProblemView extends Vue {
  @Prop({ required: false, default: null }) submitIdProp!: number | null;
  public submitId = this.submitIdProp;
  public studentId = NaN;

  private problemStore = problemStore;
  private userStore = userStore;
  private submitStore = submitStore;
  private user = this.userStore.user;
  private readonly courseId = Number(this.$route.params.courseId);

  private displayProblem = false;
  private displayCatsPackage = false;
  private catsResultSubmitId: number | null = null;

  get problem() {
    return this.problemStore.currentProblem;
  }

  get studentIds() {
    if (this.problem && this.problem.students)
      return Object.keys(this.problem?.students)
  }

  get submits(): SubmitModel[] {
    return this.submitStore.submits;
  }


  checkedSubmit(submit: SubmitModel): boolean {
    if (!this.submitIdProp)
      return submit.id === Math.max(...this.submits.map(s => s.id));
    return submit.id === this.submitIdProp;
  }

  get userSubmits() {
    return this.submits.filter((x: SubmitModel) => x.student === this.studentId);
  }

  changeCurrentSubmit(id: number): void {
    this.submitId = Number(id);
    if (this.submitIdProp === Number(id))
      return;
    this.$router.push({
      name: 'ProblemViewWithSubmit', params: {
        courseId: this.$route.params.courseId,
        lessonId: this.$route.params.lessonId,
        problemId: this.$route.params.problemId,
        submitId: Number(id).toString(),
      },
    });
  }

  showCatsAnswerModal(id: number): void {
    this.catsResultSubmitId = Number(id);
    this.toggleCatsModal(true);
  }

  get isStaff(): boolean {
    return this.user.staff_for.includes(Number(this.courseId));
  }

  async created() {
    if (!this.isStaff && !this.submitId && this.submits.length)
      this.changeCurrentSubmit(this.submits[this.submits.length - 1].id);
    if (this.submitId)
      this.studentId = this.submits?.find(x => x.id === this.submitId)?.student as number;
    if (!this.isStaff) {
      this.studentId = Number(this.userStore.user.id);
    }
    if (isNaN(this.studentId)) {
      this.studentId = this.userStore.user.id;
    }
  }

  async mounted() {
    window.addEventListener("keydown", event => {
      if (event.key == 'Escape') {
        this.toggleCatsModal(false);
      }
    });
  }

  toggleCatsModal(target: boolean | undefined = undefined) {
    if (typeof target === undefined)
      this.displayCatsPackage = !this.displayCatsPackage;
    else
      this.displayCatsPackage = target as boolean;
  }

  get avatarUrl() {
    if (this.user && this.user.avatar_url)
      return this.user.thumbnail;
    return "https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png";
  }

  checkedStudent(studentId: string): boolean {
    return Number(studentId) === this.studentId;
  }

  showProblem() {
    this.displayProblem = true;
  }


  hideProblem() {
    this.displayProblem = false;
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

.table-title
  margin-left 5rem

.problem-title
  margin-left 2rem

.item
  background-color var(--cds-ui-background)
  padding 1rem

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

.submit-list
  margin 0
  padding 0
  height 24.55em
  overflow-y scroll
  bottom 0
  list-style-type none
  border-radius 10px
  border-color black

.student-list--item--user-component
  padding-left 1rem

.submit-btn, .handlers button
  margin-top 1rem

.submit
  display flex
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)

.problem-solution
  height 100%


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


  .bx--label,
  .bx--label--disabled
    display none


.show-problem-link:hover
  cursor pointer

.message
  width auto
  pagging 100px
  margin 20%

.button
  display: inline-block
  padding: 0.75em
  margin 0.00002em
  color: #fff
  font-size: 0.8em
  text-decoration none
  text-align center
  position: relative
  overflow: hidden
  z-index: 1

  &:after
    content: ''
    position: absolute
    bottom: 0
    left: 0
    width: 100%
    height: 100%
    background-color: gray
    z-index: -2

  &:hover
    color: #fff

    &:before
      width: 100%

.avatar
  width 2em
  margin-bottom 0.3em

.student
  margin-right 1em

.stuff
  margin-left 1em

.answer
  text-align right

</style>
<style lang="stylus">
.student-list--item
  .bx--structured-list-td
    vertical-align middle
</style>
