<template>
  <transition name="fade" mode="out-in">
    <cv-breadcrumb-item v-if="!loading">
      <router-link :to="{
        name: PageView,
        props: id
      }">
        {{ title }}
      </router-link>
    </cv-breadcrumb-item>
    </transition>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { TutorialModel } from '@/models/TutorialModel';

const errors: { [key: string]: string } = {
  CourseView: 'Текущий курс',
  LessonView: 'Текущий урок',
  ProblemView: 'Текущая проблема',
  MaterialView: 'Текщий материал',
}

@Component
export default class LmsBreadcrumbItem extends Vue {
  @Prop({type: Number, required: true,}) id!: number;
  @Prop({
    type: String,
    required: true,
    validator(value: string): boolean {
      return errors.hasOwnProperty(value);
    }
  }) PageView!: string;
  @Prop({type: Function, required: true}) fetch!: (id: number) => Promise<TutorialModel>;

  title = '';

  loading = true;

  async setTitle() {
    this.loading = true;
    const localStorageKey = `${this.PageView}_${this.id}`;
    if (!localStorage.getItem(localStorageKey)) {
      localStorage.setItem(localStorageKey, (await this.fetch(this.id)).name);
    }
    this.title = localStorage.getItem(localStorageKey) ?? errors[this.PageView];
    this.loading = false;
  }

  async created() {
    await this.setTitle();
  }
}

</script>

<style lang="stylus" scoped>
  .fade-enter-active, .fade-leave-active {
    transition: opacity .1s
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    opacity: 0
  }
</style>
