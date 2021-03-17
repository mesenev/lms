import { shallowMount } from '@vue/test-utils';
import RegistrationView from '../RegistrationView.vue';

describe('RegistrationView.vue', () => {
  test('Проверка работы полей ввода', () => {
    const wrapper = shallowMount(RegistrationView);
    wrapper.setData({
      login: '1',
      first_name: '1',
      last_name: '1',
      email: '1',
      password: '1',
      password_repeat: '1',
    });
    expect(wrapper.vm.$data.login).toBe('1');
    expect(wrapper.vm.$data.first_name).toBe('1');
    expect(wrapper.vm.$data.last_name).toBe('1');
    expect(wrapper.vm.$data.email).toBe('1');
    expect(wrapper.vm.$data.password).toBe('1');
    expect(wrapper.vm.$data.password_repeat).toBe('1');
  });

  test('Methods are rendered', () => {
    const wrapper = shallowMount(RegistrationView, {
      methods: {
        checkEmail: () => {},
        checkLoginAlphabet: () => {},
        checkLoginLen: () => {},
        checkPassword: () => {},
        checkPasswordLen: () => {},
        checkRepeatPassword: () => {},
        canAction: () => {},
        action: () => {},
      },
    });
    expect(wrapper.exists()).toBe(true);
  });

  //TODO: check if action goes with btn click
  jest.mock("RegistrationView", () => ({
    register() {
      return {
        onChange() {
          return true;
        },
      };
    },
  }));
});

