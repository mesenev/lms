<template>
  <!-- TODO: nice and clean prop work -->
  <div class="bx--grid">
    <div class="bx--row header">
      <cv-skeleton-text v-if="loading"/>
      <div v-else>
        <h1>Регистрация на курс {{ course.name || '' }}, преподаватель {{ course.author.first_name }}
          {{ course.author.last_name }}.</h1>
      </div>
    </div>
    <div class="bx--row">
      <div class="bx--col-lg-16 items">
        <div>
          <cv-inline-notification
            v-if="showNotification"
            :kind="notificationKind"
            :sub-title="notificationText"
            @close="hideNotification"/>
          <cv-skeleton-text v-if="loading"/>
          <div v-else>
            <h3>Уважаемый {{ firstname }} {{ secondname }}.</h3>
            <div v-if="is_possible">
              <h4>Нажав кнопку вы зарегистрируетесь на выбранный курс!</h4>
              <div>
                <cv-button-skeleton v-if="registrationProcess"/>
                <cv-button v-else v-on:click="registration">Зарегистрироваться</cv-button>
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
import NotificationMixinComponent from '@/components/common/NotificationMixinComponent.vue';
import CourseModel from '@/models/CourseModel';
import UserModel from "@/models/UserModel";
import userStore from "@/store/modules/user";
import axios from 'axios';
import {Component, Prop} from 'vue-property-decorator';


@Component({components: {}})
export default class CourseRegistrationView extends NotificationMixinComponent {
  @Prop({required: true}) linkProp!: string;
  course: CourseModel | null = null;
  user: UserModel | null = null;
  loading = true;
  is_possible = false;
  student_registered = false;
  teacher_registered = false;
  firstname = userStore.user.first_name;
  secondname = userStore.user.last_name
  registrationProcess = false;

  async created() {
    await this.statusSetup();
    this.loading = false;
  }

  async statusSetup() {
    const answer = await axios.get<{
      is_possible: boolean; student_registered: boolean;
      teacher_registered: boolean; course: CourseModel; user: UserModel;
    }>(`/api/check-link/${this.linkProp}/`)
      .then(result => {
        this.is_possible = result.data.is_possible;
        this.student_registered = result.data.student_registered;
        this.teacher_registered = result.data.teacher_registered;
        this.course = result.data.course;
      })
      .catch(error => {
        this.notificationKind = error;
        this.notificationText = `Произошла ошибка при проверке возможности` +
          ` регистрации на курс. ${error.message}`;
        this.showNotification = true;
      })
  }

  async registration() {
    this.registrationProcess = true;
    await axios.get(`/api/course-registration/${this.linkProp}/`)
      .then(result => {
        this.$router.push({
          name: 'CourseView',
          params: { courseId: result.data.courseId },
        })
        this.registrationProcess = false;
      }).catch(error => {
          this.notificationKind = error;
          this.notificationText = `Произошла ошибка при регистрации на курс. ${error.message}`;
          this.showNotification = true;
        },
      )
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
