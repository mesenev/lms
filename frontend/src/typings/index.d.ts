declare module '@carbon/vue/src/index';
declare module '@carbon/*';
declare module '*.scss';

declare module '*.vue' {
  import type { DefineComponent } from 'vue';

  const component: DefineComponent<{}, {}, any>;
  export default component;
}
