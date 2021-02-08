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
import {Component, Prop, Vue} from "vue-property-decorator";
import {Model} from "@/typings";

export interface BreadcrumbDictionary {
  [id: number]: string;
}

@Component
export default class LmsBreadcrumbItem extends Vue {
  @Prop({ type: Number, required: true, }) id!: number;
  @Prop({ type: String, required: true }) PageView!: string;
  @Prop( { type: Function, required: true }) fetch!: (id: number) => Promise<Model>;

  title = '';

  loading = true;

  async setTitle() {
    this.loading = true;
    if (!localStorage.getItem(this.id.toString())) {
      localStorage.setItem(this.id.toString(), (await this.fetch(this.id)).name);
    }
    this.title = localStorage.getItem(this.id.toString()) ?? '';
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
