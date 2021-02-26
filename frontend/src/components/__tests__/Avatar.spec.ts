import { shallowMount } from '@vue/test-utils'
import Avatar from '../Avatar.vue'

describe('Avatar.vue', () => {
  test('Если в Avatar.vue был передан url, картинка отрисовывается по этому url', () => {
    const wrapper = shallowMount(Avatar, {
      propsData: { avatar_url: 'test.url'}
    })
    console.log(wrapper.get('img').html())
    expect(wrapper.props('avatar_url')).toBe('test.url')
    const avatar = wrapper.find('img')
  })
  test('Если в Avatar.vue не был передан url, картинка отрисовывается по дефолтному url', () => {
    const wrapper = shallowMount(Avatar, {
      propsData: { avatar_url: ''}
    })
    console.log(wrapper.get('img').html())
    expect(wrapper.props('avatar_url')).toBe('')
  })
})


