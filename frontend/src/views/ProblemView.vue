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
            <cv-structured-list
              v-if="submits" class="submit-list"
              condensed selectable @change="changeCurrentSubmit">
              <message-component
              v-for="message in messages"
              :key="message.id"
              :message="message"
              >

              </message-component>
            </cv-structured-list>
            <cv-tile v-else class="submit-list no-submits" kind="standard">
              <h2>Oops</h2>
              <p>Пока ничего не отправлено :(</p>
            </cv-tile>
            <cv-text-input class="searchbar"
            :light="light"
            :label="''"
            :value="''"
            :disabled="false"
            :type="''"
            :password-visible="false"
            :placeholder="'Введите сообщение'"
            v-on:keydown.enter="messageForButton"
            v-model.trim="message">
            </cv-text-input>
          </div>
        </div>
      </cv-column>
      <cv-column v-if="isStaff && !displayCatsPackage">
        <div class="item">
          <cv-structured-list class="student-list" condensed selectable @change="changeStudent">
            <template slot="headings">
              <cv-structured-list-heading class="table-title">Ученики</cv-structured-list-heading>
            </template>
            <template slot="items">
              <cv-structured-list-item
                v-for="student in studentIds"
                :key="student"
                :checked="checkedStudent(student)"
                :value="student.toString()"
                name="student">
                <cv-structured-list-data>
                  <user-component :user-id="student"/>
                </cv-structured-list-data>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
        </div>
      </cv-column>

      <cv-column v-if="displayCatsPackage">
        <cats-package-window></cats-package-window>
      </cv-column>

    </cv-row>
  </div>
</template>

<script lang="ts">
import ProblemDescription from "@/components/ProblemDescription.vue";
import SubmitComponent from '@/components/SubmitComponent.vue';
import MessageComponent from '@/components/MessageComponent.vue';
import SubmitStatus from "@/components/SubmitStatus.vue";
import UserComponent from '@/components/UserComponent.vue';
import SubmitModel from '@/models/SubmitModel';
import problemStore from '@/store/modules/problem';
import submitStore from '@/store/modules/submit';
import userStore from '@/store/modules/user';
import { Component, Prop, Vue } from 'vue-property-decorator';
import LogEventModel from "@/models/LogEventModel";
import CatsPackageWindow from "@/components/CatsPackageWindow.vue";


@Component({ components: { CatsPackageWindow, SubmitComponent, ProblemDescription, SubmitStatus, UserComponent, MessageComponent } })
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

  light = false;

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

  get msgs() {
    const smth = [];
    for (let i = 0; i < 20; i++) {
      const newMsg = {"type": "message", "text": "test", "sender": this.user, "lessonId": 1,
        "courseId": this.courseId, "id":i, "name": "sdfdsfsf"};
      smth.push(newMsg);
    }
    return smth;
  }
  messages: Array<LogEventModel> = this.msgs

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

  async created() {
    if (!this.isStaff && !this.submitId && this.submits)
      this.changeCurrentSubmit(this.submits[this.submits.length - 1].id);
    if (this.submitId)
      this.studentId = this.submits?.find(x => x.id === this.submitId)?.student as number;
    if (!this.isStaff) {
      this.studentId = Number(this.userStore.user.id);
    }
  }

  async mounted() {
    const submits = [...document.getElementsByClassName("submit-list")];
    submits.forEach(element => element.scrollTop = element.scrollHeight);
    const userMessages = [...document.getElementsByTagName("img")];
    userMessages.forEach(element =>
      element.classList.contains("avatar") ? element.src = this.avatarUrl : 0);

    window.addEventListener("keydown", event =>{
      if (event.key == 'Escape'){
        this.visionCatsPackage();
      }
    });
  }

  visionCatsPackage(){
    this.displayCatsPackage = !this.displayCatsPackage;
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

  messageForButton(message: string) {
    console.log(document.getElementsByClassName("searchbar")[0])
    const newMessage: LogEventModel = {"name": "logEvent", "type": "message", "text": message,
      sender: this.user, id: this.messages.length+2,
      lessonId: this.courseId, courseId: this.courseId}
    this.messages.push(newMessage);
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

.submit-list, .student-list
  margin 0
  padding 0
  height 24.55em
  overflow-y scroll
  bottom 0
  list-style-type none
  border-radius 10px
  border-color black
  background-color #609ab6

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


  .bx--label,
  .bx--label--disabled
    display none


.show-problem-link:hover
  cursor pointer

.searchbar
  position relative
  height 2em
  left 0
  width 100%
  margin-left auto
  margin-right auto
  text-align center

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


.bx--list
  list-style-type none


.avatar
  width 2em
  margin-bottom 0.3em

.student
  margin-right 1em

.stuff
  margin-left 1em




.bx--tile.submit-list
  border-left 1em
  padding-left 1em
  margin-left 1em
  box-shadow -1em black


.answer
  text-align right

</style>
