// This is the "store accessor":
// It initializes all the modules using a Vuex plugin (see store/index.ts)
// In here you import all your modules, call getModule on them to turn them
// into the actual stores, and then re-export them.

import CourseModule from '@/store/modules/course';
import LessonModule from '@/store/modules/lesson';
import ProblemModule from "@/store/modules/problem";
import SubmitModule from '@/store/modules/submit';
import UserModule from '@/store/modules/user';
import MaterialModule from "@/store/modules/material";
import { Store } from 'vuex'
import { getModule } from 'vuex-module-decorators';

// Each store is the singleton instance of its module class
// Use these -- they have methods for state/getters/mutations/actions
// (result from getModule(...))
export let userStore: UserModule;
export let problemStore: ProblemModule
export let courseStore: CourseModule;
export let lessonStore: LessonModule;
export let submitStore: SubmitModule;
export let materialStore: MaterialModule;

// initializer plugin: sets up state/getters/mutations/actions for each store
export function initializeStores (store: Store<unknown>): void {
  userStore = getModule(UserModule, store)
  problemStore = getModule(ProblemModule, store)
  courseStore = getModule(CourseModule, store)
  lessonStore = getModule(LessonModule, store)
  submitStore = getModule(SubmitModule, store);
  materialStore = getModule(MaterialModule,store);
}

// for use in 'modules' store init (see store/index.ts), so each module
// appears as an element of the root store's state.
// (This is required!)
export const modules = {
  'problem': ProblemModule,
  'user': UserModule,
  'course': CourseModule,
  'lesson': LessonModule,
  'submit': SubmitModule,
  'material': MaterialModule
}

