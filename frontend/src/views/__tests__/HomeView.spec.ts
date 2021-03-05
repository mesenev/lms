import { shallowMount } from '@vue/test-utils'
import HomeView from '../HomeView.vue'

describe('HomeView.vue', () => {
  test('unit-test', () => {
    const wrapper = shallowMount(HomeView, {
      propsData: {}
    })
    console.log(wrapper.html())
  })
})
