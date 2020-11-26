import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators';

@Module export default class Counter2 extends VuexModule {
  count = 0;

  @Mutation
  increment(delta: number) {
    this.count += delta;
  }
  @Mutation
  decrement(delta: number) {
    this.count -= delta;
  }

  @Action({ commit: 'increment' })
  incr() {
    return 5;
  }
  @Action({ commit: 'decrement' })
  decr() {
    return 5;
  }
}
