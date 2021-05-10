<template>
  <div class="bx--grid">
    <div class="bx--row">
      <div class="bx--col-lg-16 links">
        <div>
          <cv-skeleton-text v-if="loading"/>
          <div v-else>
            <h2>Регистрация на курс {{ course.name || '' }},
              преподаватель курса: {{ course.author.first_name }} {{ course.author.last_name }}.
            </h2>
          </div>
          <cv-inline-notification
            v-if="showNotification"
            :kind="notificationKind"
            :sub-title="notificationText"
            @close="hideNotification"/>
          <div v-if="is_possible">
            <h3>Нажав кнопку вы будете зарегистрируетесь на данный курс.</h3>
            <div class="buttons">
              <cv-button-skeleton v-if="registrationProcess"/>
              <cv-button v-else
                         :icon="Education16"
                         kind="secondary"
                         v-on:click="registration">
                Зарегистрироваться
              </cv-button>
            </div>
          </div>
          <div v-if="!is_possible">
            <div v-if="student_registered" class="warningtxt">
              <h3> Вы уже зарегистрированы на данном курсе как студент. </h3>
            </div>
            <div v-else-if="teacher_registered" class="warningtxt">
              <h3> Вы уже зарегистрированы на данном курсе как преподаватель. </h3>
            </div>
            <div v-else-if="!usages_available" class="warningtxt">
              <h3> Данная ссылка более недействительна. Обратитесь к преподавателю курса.</h3>
            </div>
            <div class="buttons">
              <router-link to="/">
                <cv-button :icon="Home16" kind="secondary"> На главную</cv-button>
              </router-link>
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
import axios from 'axios';
import {Component, Prop} from 'vue-property-decorator';
import Home16 from '@carbon/icons-vue/lib/home/16'
import Education16 from '@carbon/icons-vue/lib/education/16'


@Component({components: {}})
export default class CourseRegistrationView extends NotificationMixinComponent {
  @Prop({required: true}) linkProp!: string;
  course: CourseModel | null = null;
  loading = true;
  is_possible = false;
  student_registered = false;
  usages_available = false;
  teacher_registered = false;
  registrationProcess = false;
  Home16 = Home16;
  Education16 = Education16;

  async created() {
    await this.statusSetup();
    this.loading = false;
  }

  async statusSetup() {
    const answer = await axios.get<{
      is_possible: boolean; usages_available: boolean; student_registered: boolean;
      teacher_registered: boolean; course: CourseModel; user: UserModel;
    }>(`/api/check-link/${this.linkProp}/`)
      .then(result => {
        this.is_possible = result.data.is_possible;
        this.usages_available = result.data.usages_available;
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

.links
  text-align: center
  display: flex
  justify-content: center
  flex-direction: column
  height: 400px
  padding: 20px

.item
  min-height 85px

.buttons
  padding: 20px

.warningtxt
  font-style italic

</style>
