import { shallowMount } from '@vue/test-utils'
import AddCatsModal from '../AddCatsModal.vue'


describe('AddCatsModal.vue', () => {
  test('', () => {
    const wrapper = shallowMount(AddCatsModal)
    expect(wrapper.props('avatar_url')).toBe('test.url')
  })
})
