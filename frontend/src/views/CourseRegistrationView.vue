<template>
  <cv-grid>
    <cv-row class="header">
      <cv-skeleton-text v-if="loading"/>
      <div v-else>
        <h1>регистрация на курс {{ course.name || '' }}</h1>
        <h2>Преподаватель {{ course.author.first_name }} {{ course.author.last_name }}</h2>
      </div>
    </cv-row>
    <cv-row v>
      <cv-column :lg="2"/>

      <cv-column v-if='loading' :lg="12">
        <cv-loading></cv-loading>
      </cv-column>
      <cv-column v-else :lg="12">
        <div class="item">
          <h2>Уважаемый {{ 'username' }}.</h2>
          <div v-if="is_possible" class="text-container">
            Lorem ipsum dolor sit amet,
            consectetur adipisicing elit.
            Assumenda cum est laborum maxime,
            porro quae quas quidem quo similique veniam!
            <br>
            <cv-button>Зарегистрироваться</cv-button>
          </div>
          <!---->
          <div v-if="!is_possible && already_registered" class="text-container">
            Lorem ipsum dolor sit amet,
            consectetur adipisicing elit.
            Assumenda cum est laborum maxime,
            porro quae quas quidem quo similique veniam!
            <br>
            <router-link to="/">
              <cv-button type="ghost">На главную</cv-button>
            </router-link>
          </div>
        </div>
      </cv-column>
      <cv-column :lg="2"/>
    </cv-row>
  </cv-grid>
</template>

<script lang="ts">
import CourseModel from '@/models/CourseModel';
import axios from 'axios';
import {Component, Prop, Vue} from 'vue-property-decorator';
import UserModel from "@/models/UserModel";

@Component({components: {}})
export default class CourseRegistrationView extends Vue {
  @Prop({required: true}) linkProp!: string;
  course: CourseModel | null = null;
  user: UserModel | null = null;
  loading = true;
  is_possible = false;
  already_registered = false;

  async created() {
    await this.statusSetup();
    this.loading = false;
  }

  async statusSetup() {
    const answer = await axios.get<{
      is_possible: boolean; already_registered: boolean; course: CourseModel; user: UserModel;
    }>(`/api/check-link/${this.linkProp}/`)
      .then(result => {
        this.is_possible = result.data.is_possible;
        this.already_registered = result.data.already_registered;
        this.course = result.data.course;
        this.user = result.data.user;
      },)
      .catch(error => {
      console.log('vse poshlo ne po planu rip')
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
