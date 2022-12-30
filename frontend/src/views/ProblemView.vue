<template>
  <div class="bx--grid">
    <div class="bx--row header-container">
      <div :class="{'bx--offset-lg-1': isStaff, 'bx--offset-lg-2': !isStaff}" class="main-title">
        <h1 v-if="problem" class="">{{ problem.name }}</h1>
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
          <div class="problem-information">
            <span>{{ workName }}</span>
            <span>Дедлайн: <strong>{{ lesson.deadline }}</strong></span>
            <span v-if="lesson.scores[problem.type]">
              Макс. балл <strong>{{ lesson.scores[problem.type] }}</strong>
            </span>
            <span>Режим тестирования: <strong>{{ this.problem.test_mode }}</strong> </span>
          </div>
        </div>
      </div>
    </div>
    <cv-row class="main-items" justify="center">
      <problem-navigation v-if="!isStaff" :lesson-id="problem.lesson"></problem-navigation>
      <cv-column v-if="isStaff && !displayCatsPackage">
        <div class="item">
          <cv-structured-list class="student-list" condensed selectable @change="changeStudent">
            <template slot="headings">
              <cv-structured-list-heading class="pupil-title">Список учеников
              </cv-structured-list-heading>
            </template>
            >
            <template slot="items">
              <cv-structured-list-item
                  v-for="student in studentIds"
                  :key="student"
                  :checked="checkedStudent(student)"
                  :value="student.toString()"
                  class="student-list--item"
                  name="student">
                <cv-structured-list-data>
                  <user-component :user-id="student" class="student-list--item--user-component"/>
                </cv-structured-list-data>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
        </div>
      </cv-column>
      <cv-column :lg="{'span': 8, 'offset': isStaff ? 0 : 2}">
        <div class="solution-container item">
          <submit-component
              v-if="problem"
              :is-staff="isStaff" :language-list="problem.language"
              :submitId="submitId"
              class="solution-container--submit-component"
              @submit-created="(x) => changeCurrentSubmit(x.id)"/>
          <cv-loading v-else small/>
          <div class="solution-container--submit-list">
            <log-event-component
                v-if="!!problem"
                :key="logEventComponentKey"
                :problemId="problem.id" :selected-submit="submitId"
                :studentId="studentId"
                class="log--event--component"
                @submit-selected="(x) => changeCurrentSubmit(x.id)"
                @cats-answer="(x) => showCatsAnswerModal(x.id)"
            />
            <cv-loading v-else></cv-loading>
          </div>
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
import ProblemNavigation from "@/components/ProblemNavigation.vue";
import SubmitComponent from '@/components/SubmitComponent.vue';
import LogEventComponent from '@/components/LogEventComponent.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import UserComponent from '@/components/UserComponent.vue';
import SubmitModel from '@/models/SubmitModel';
import lessonStore from '@/store/modules/lesson';
import problemStore from '@/store/modules/problem';
import submitStore from '@/store/modules/submit';
import userStore from '@/store/modules/user';
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import CatsPackageWindow from "@/components/CatsPackageWindow.vue";


@Component({
  components: {
    CatsPackageWindow,
    SubmitComponent,
    ProblemDescription,
    SubmitStatus,
    UserComponent,
    LogEventComponent,
    ProblemNavigation
  },
})
export default class ProblemView extends Vue {
  @Prop({ required: false, default: null }) submitIdProp!: number | null;
  public submitId = this.submitIdProp;
  public studentId = NaN;

  private lessonStore = lessonStore;
  private problemStore = problemStore;
  private userStore = userStore;
  private submitStore = submitStore;
  private user = this.userStore.user;
  private readonly courseId = Number(this.$route.params.courseId);

  private displayProblem = false;
  private displayCatsPackage = false;
  private catsResultSubmitId: number | null = null;

  private logEventComponentKey = 0;

  get lesson() {
    return this.lessonStore.currentLesson;
  }

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

  get userSubmits() {
    return this.submits.filter((x: SubmitModel) => x.student === this.studentId);
  }

  get workName() {
    if (this.problem?.type === "CW")
      return "Классная работа";
    else if (this.problem?.type === "HW")
      return "Домашняя работа"
    else if (this.problem?.type === "EX")
      return "Дополнительные задания"
  }

  get isStaff(): boolean {
    return this.user.staff_for.includes(Number(this.courseId));
  }

  get avatarUrl() {
    if (this.user && this.user.avatar_url)
      return this.user.thumbnail;
    return "https://www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png";
  }

  get isCompleted(): boolean {
    return !!this.submits.find((submit: SubmitModel) => (
        submit.status === 'OK'
    ));
  }

  @Watch('$route.params.problemId', { immediate: true, deep: true })
  async unUrlChange() {
    const problem = await this.problemStore.fetchProblemById(Number(this.$route.params.problemId));
    this.problemStore.changeCurrentProblem(problem);
    this.recreateLogEventComponent();
  }

  checkedSubmit(submit: SubmitModel): boolean {
    if (!this.submitIdProp)
      return submit.id === Math.max(...this.submits.map(s => s.id));
    return submit.id === this.submitIdProp;
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

  async created() {
    if (this.isStaff && !this.submitId && this.submits.length)
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
    this.recreateLogEventComponent();
  }

  recreateLogEventComponent() {
    this.logEventComponentKey += 1;
  }
}
</script>

<style lang="stylus" scoped>
.main-title
  margin-top 1rem

h1
  color var(--cds-ui-05)
  font-weight bold

.description-container
  display block

.problem-title
  margin-left 2rem

.problem-information
  color var(--cds-ui-04)
  margin-top 1rem

  span
    margin 0 0.5rem

.item
  background-color var(--cds-ui-background)

//padding 1rem

.solution-container
  display flex

  &--submit-component
    margin-bottom 1rem
    flex 59%

  &--submit-list
    margin-bottom 1rem
    flex 40%

  @media (max-width: 767px)
    display block

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

.text-area-teacher textarea:disabled
  cursor pointer
  color #000

.handlers
  button:nth-child(2n)
    margin-left 5px

.code
  .bx--text-area
    height 30em


  .bx--label,
  .bx--label--disabled
    display none


.show-problem-link
  cursor pointer
  padding 0.5em
  border-radius 4px
  background-color var(--cds-field-01)
  color var(--cds-text-01)
  display inline-block
  margin-top 0.5rem

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

.answer
  text-align right

.student-list
  margin-bottom 2rem

  .pupil-title
    padding-left 0.5rem


.problem-description-modal
  .bx--modal-container
    border-radius 5px

aside
  @media (max-width: 1100px)
    display none
</style>
<style lang="stylus">
.student-list--item
  .bx--structured-list-td
    vertical-align middle
</style>
