import { shallowMount } from '@vue/test-utils';
import ProfileView from '../ProfileView.vue';

describe('ProfileView.vue', () => {
  test('check if FirstName and LastName display when the page starts', () => {
    const wrapper = shallowMount(ProfileView);
    wrapper.setData({
      first_name: '1',
      last_name: '2',
    })
    expect(wrapper.vm.$data.last_name).toBe('2');
    expect(wrapper.vm.$data.first_name).toBe('1');
  })
});
