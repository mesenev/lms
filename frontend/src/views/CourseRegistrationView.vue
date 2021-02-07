<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-16">
        <cv-skeleton-text v-if="loading"/>
        <div v-else>
          <h1>Регистрация на курс {{ course.name || '' }}, преподаватель: {{ course.author.first_name }}
            {{ course.author.last_name }}</h1>
        </div>
        <div>
          <cv-skeleton-text v-if="loading"/>
          <div v-else>
            <h3>Уважаемый {{ firstname }} {{ secondname }}.</h3>
            <div v-if="is_possible">
              <h4>Нажав кнопку вы зарегистрируетесь на выбранный курс!</h4>
              <div>
                <router-link :to="{
            name: 'CourseView',
            props: this.$route.params.courseId }">
                  <!-- TODO: router link work + centering this, i guess -->
                  <cv-button>Зарегистрироваться</cv-button>
                </router-link>
              </div>
            </div>
            <div v-if="!is_possible && student_registered || teacher_registered">
              <h4>Данная ссылка недоступна, либо вы уже зарегистрированы на курс.</h4>
              <div>
                <router-link to="/">
                  <cv-button type="ghost">На главную</cv-button>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import CourseModel from '@/models/CourseModel';
import axios from 'axios';
import {Component, Prop, Vue} from 'vue-property-decorator';
import UserModel from "@/models/UserModel";
import userStore from "@/store/modules/user";

@Component({components: {}})
export default class CourseRegistrationView extends Vue {
  @Prop({required: true}) linkProp!: string;
  course: CourseModel | null = null;
  user: UserModel | null = null;
  loading = true;
  is_possible = false;
  student_registered = false;
  teacher_registered = false;
  firstname = userStore.user.first_name;
  secondname = userStore.user.last_name

  async created() {
    await this.statusSetup();
    this.loading = false;
  }

  async statusSetup() {
    const answer = await axios.get<{
      is_possible: boolean; student_registered: boolean; teacher_registered: boolean; course: CourseModel; user: UserModel;
    }>(`/api/check-link/${this.linkProp}/`)
      .then(result => {
        this.is_possible = result.data.is_possible;
        this.student_registered = result.data.student_registered;
        this.teacher_registered = result.data.teacher_registered;
        this.course = result.data.course;
        this.user = result.data.user;
      },)
      .catch(error => {
        console.log('It isn`t right behaviour :(')
      })
  }
}
</script>

<style lang="stylus">
.header
  padding-bottom: 1.5rem
  padding-top: 1rem

.items
  background-color var(--cds-ui-02)
  padding var(--cds-spacing-05)
  min-height 600px

  .bx--structured-list-thead
    display none

.item
  min-height 85px
</style>
